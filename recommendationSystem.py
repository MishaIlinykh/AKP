import pandas as pd
from datetime import datetime
from scipy.optimize import minimize
import pickle
import json
from models import add_models, predict
#-----------------------------------------------------------------------------------------------------------------------
'''
функция рассчитывает необходимое количесво добавок без учета усвоения и содержания в ферросплаве
'''
def requiredAdditive(dataFrame, bound):
    # val - масса необходимой добавки, без учета усвоения и содержания элемента в ферроспалве
    # X1 - текущее значение
    # X2 - целевое значение
    # M - масса стали в ковше
    val = lambda X1, X2, M: (X2 - X1)*M/100
    for i in bound.index:
        element = bound.loc[i, 'Элемент']
        X1 = dataFrame.loc[0, 'VAL'+ element[0]+element[1:].lower()+'_pr']
        X2 = bound.loc[i, 'Цель']
        M = dataFrame.loc[0, 'm_calk']
        bound.loc[i, 'val'] = val(X1, X2, M)
    # отсеиваем, если значение элемента почти попадает в целевое
    bound = bound[bound['val'] > 3]
    return bound
#-----------------------------------------------------------------------------------------------------------------------
'''
Функция считает вес необходимых добавок для марганца и кремения
Если необходимо легировать марганец, то используеться ферросплав 'MnSi17А'
Затем в случае необходимости легировать кремний, происходит пересчет val для крмения (с учетом добавленного 'MnSi17А')
Если кремения все еще недостточно добавляеться 'FeSi75'.
'''
def alloyingMnSI(bound, ferro, assimilation, library_ferroalloys):
    # val - масса необходимой добавки, без учета усвоения и содержания элемента в ферроспалве
    # X - процентное содержание элемента в ферросплаве
    # Y - коэффицент усвоения
    # m - масса ферросплава
    val = lambda m, X, Y: m * (Y / 100) * (X / 100)
    m = lambda val, X, Y: (val * 100 * 100) / (Y * X)
    if 'MN' in bound['Элемент'].value_counts().index:
        material = library_ferroalloys['Mn'][0]
        # коэффицент усвоения
        Y_Mn = assimilation[assimilation['Описание'] == material]['Mn'].values[0]
        # содержание марганца в ферросплаве
        X_Mn = ferro[ferro['Описание'] == material]['Mn'].values[0]
        # масса необходимой добавки Mn, без учета усвоения и содержания элемента в ферроспалве
        val_Mn = bound.loc[bound[bound['Элемент'] == 'MN'].index[0], 'val']
        # масса необходимой добавки Mn, c учетом усвоения и содержания элемента в ферроспалве
        massa = round(m(val_Mn, X_Mn, Y_Mn) + 0.45)
        # записываем результат
        bound.loc[bound['Элемент'] == 'MN', 'm'] = massa
        bound.loc[bound['Элемент'] == 'MN', 'Ферроматериал'] = material

        # если Si так же нужно легировать, то пересчитываем для него val
        if 'SI' in bound['Элемент'].value_counts().index:
            # коэффицент усвоения
            Y_Si = assimilation[assimilation['Описание'] == material]['Si'].values[0]
            # содержание кремения в ферросплаве
            X_Si = ferro[ferro['Описание'] == material]['Si'].values[0]
            # пересчитываем val для кремения с учетом 'MnSi17А'
            val_Si = val(massa, X_Si, Y_Si)
            # записываем результат
            bound.loc[bound['Элемент'] == 'SI', 'val_new'] = bound.loc[bound[bound['Элемент'] == 'SI'].index[
                                                                           0], 'val'] - val_Si
            # если кремения уже достаточно
            if bound.loc[bound[bound['Элемент'] == 'SI'].index[0], 'val'] < 0:
                bound.loc[bound['Элемент'] == 'SI', 'Ферроматериал'] = material
                return bound

    # если необходимо легировать крмений еще
    if 'SI' in bound['Элемент'].value_counts().index:
        material = library_ferroalloys['Si'][0]
        # коэффицент усвоения
        Y_Si = assimilation[assimilation['Описание'] == material]['Si'].values[0]
        # содержание кремения в ферросплаве
        X_Si = ferro[ferro['Описание'] == material]['Si'].values[0]
        # масса необходимой добавки Si, без учета усвоения и содержания элемента в ферроспалве
        val_Si = bound.loc[bound[bound['Элемент'] == 'SI'].index[0], 'val_new']
        # масса необходимой добавки Si, c учетом усвоения и содержания элемента в ферроспалве
        massa = round(m(val_Si, X_Si, Y_Si) + 0.45)
        # записываем результат
        bound.loc[bound['Элемент'] == 'SI', 'm'] = massa
        bound.loc[bound['Элемент'] == 'SI', 'Ферроматериал'] = material
    return bound
#-----------------------------------------------------------------------------------------------------------------------
'''
Функция считает вес необходимых добавок для всех элементов (кроме марганца и кремения)
Сначала находиться лучший ферроматериал из имеющихся для легирования данного элемента
Лучшим считаеться материал с максимальным коэффицентов X*Y/P
Далее расчитываеться масса необходимой добавки с учетов усвоения и содержания элемента в ферроспалве
'''
def alloying(bound, element, ferro, assimilation, short, material_cods, library_ferroalloys):
    # val - масса необходимой добавки, без учета усвоения и содержания элемента в ферроспалве
    # X - процентное содержание элемента в ферросплаве
    # Y - коэффицент усвоения
    # m - масса ферросплава
    m = lambda val, X, Y: (val*100*100)/(Y*X)
    # датафрейм для сравнения всех материалов
    df = pd.DataFrame(columns=['fer','X', 'Y', 'P', 'X*Y/P'])
    # счетчик (для записи в датафрейм)
    c = 0
    for i in library_ferroalloys[element[0]]:
        # код ферроматериала, чтобы затем найти его цену
        cod = material_cods[material_cods['DESC_C']==i]['MAT_CODE'].values[0]
        # содержание элемента в ферросплаве
        X = ferro[ferro['Описание']==i][element[0][0]+element[0][1:].lower()].values[0]
        # коэффицент усвоения
        Y = assimilation[assimilation['Описание'] == i][element[0][0]+element[0][1:].lower()].values[0]
        # стоимость материала
        P = short[short['Номенклатура|Ном№'] ==cod]['Стоимость'].mean()
        df.loc[c] = [i, X, Y, P, X*Y/P]
        c+=1
    # выбираем лучший ферроматериал для данного элемента
    df = df[df['X*Y/P'] == max(df['X*Y/P'])]
    # название ферроматериала
    material = df['fer'].values[0]
    # содержание элемента в ферросплаве
    X = df['X'].values[0]
    # коэффицент усвоения
    Y = df['Y'].values[0]
    # масса необходимой добавки, без учета усвоения и содержания элемента в ферроспалве

    val = bound.loc[bound[bound['Элемент']==element[0].upper()].index[0], 'val']
    # масса необходимой добавки, c учетом усвоения и содержания элемента в ферроспалве
    massa = round(m(val, X, Y)+0.45)
    # записываем результат
    bound.loc[bound['Элемент']==element[0].upper(), 'm'] = massa
    bound.loc[bound['Элемент']==element[0].upper(), 'Ферроматериал'] = material
    return bound
#-----------------------------------------------------------------------------------------------------------------------
'''
Штрафная функция, минимум которой находим
Увеличивает свое значение на модуль разницы между целевым и предсказнным значением, умноженный на eta
'''
def penaltyFunction(fit_params, all_params, bound, ferro, assimilation, models, columns, eta):
    # присваеваем начальное значени штрафу
    score = 0
    # dataFrame для дальнейшего прогнозирования
    dataFrame = all_params.copy()

    # меняем массу добавок
    bound.reset_index(inplace=True, drop=True)
    for i in bound.index:
        material = bound.loc[i, 'Ферроматериал']
        dataFrame.loc[0, material] = int(dataFrame.loc[0, material]) + fit_params[i]

    # прогнозируем химический состав
    # temp - в данном случаемне нужна, оставил, чтобы не переписывать функция predict
    pred, temp = predict(models, dataFrame, columns, ferro, assimilation, 6)

    # идем по каждому элементу и увеличиваем штрафную функцию если не попали в цель
    for i in bound.index:
        # текущий элемент
        element = bound.loc[i, 'Элемент']
        # прогнозное значение
        pr = pred.loc[0, element]
        # целевое значение
        target = bound.loc[i, 'Цель']
        score += abs(target - pr) * eta
    return score
#-----------------------------------------------------------------------------------------------------------------------
'''
Находим элементы, требующие легирования (значение меньше целевого)
Для каждого элемента находим оптимальный ферросплав и рассчитываем массу добавки этого ферросплава
Эти значения становяться начальным приближением для дальнейшей оптимизации с помощью моделей 
Далее оптимизируем
'''
def additiveRecommendation(DataFrame_test, ferro, assimilation, short, boundaries, material_cods, models, columns):
    # создаем датафрейм, который будут на выходе функции
    recommendation = pd.DataFrame(columns=['Время добавки', 'Код', 'Описание', 'Масса'])

    # если для данного кода марки стали нет требуемых границ, то отправялем пустой датафрейм (ничего не рекомендуем)
    if boundaries[boundaries['Код'] == DataFrame_test.loc[0, 'Код марки стали']].shape[0] < 1:
        return recommendation

    # MAE для элементов на тесте (округлил все в большую сторону)
    # если отсутсвует целевое значение, то стремимся к минимальному+значение погрешности
    library_errors = {'C': 0.008,
                      'MN': 0.0113,
                      'SI': 0.0138,
                      'CR': 0.005,
                      'MO': 0.0016,
                      'V': 0.0017,
                      'NB': 0.00069,
                      'AL': 0.01,
                      'TI': 0.00038,
                      }

    # маетриалы, которыми можно легировать тот или иной химический элемент
    material_C = ['УСМ 03-10мм']
    material_MN = ['MnSi17А']
    material_SI = ['FeSi75', 'MnSi17А']
    material_CR = ['ФХ025']
    material_MO = ['Ферромолбден ФМо 50', 'Ферромолбден ФМо 60']
    material_V = ['FeV-50', 'Лигатура ванадиевая']
    material_NB = ['Лигатура ниобиевая ФНСБ', 'Проволока феррониобиевая']
    material_AL = ['Al проволока (АПВ)']
    material_TI = ['Ферротитан ФТ35', 'Ферротитан ФТ70']

    # последовательность легирования элементов
    library_alloying = {1: ['C'],
                        2: ['Mn', 'Si'],
                        3: ['Cr'],
                        4: ['Mo'],
                        5: ['V'],
                        6: ['Nb'],
                        7: ['Al'],
                        8: ['Ti'],
                        }

    # маетриалы для легирования элементов
    library_ferroalloys = {'C': material_C,
                           'Mn': material_MN,
                           'Si': material_SI,
                           'Cr': material_CR,
                           'Mo': material_MO,
                           'V': material_V,
                           'Nb': material_NB,
                           'Al': material_AL,
                           'Ti': material_TI,
                           }

    # находим граничные значения элементов
    bound = boundaries[boundaries['Код'] == DataFrame_test.loc[0, 'Код марки стали']]
    # берем элементы у которых есть миниммальное значение
    bound = bound[pd.isnull(bound['min']) == False]
    # если нет целевого значения, то берем минимальное и прибавляем среднюю ошибку на тесте
    for i in bound.index:
        if pd.isnull(bound.loc[i, 'Цель']) == True:
            bound.loc[i, 'Цель'] = bound.loc[i, 'min'] + library_errors[bound.loc[i, 'Элемент']]

    # находим элементы по которым необходимо произвести легирование
    for i in bound.index:
        # текущий элемент
        element = bound.loc[i, 'Элемент']
        # целевое значение
        target = bound.loc[i, 'Цель']
        # текущее значение
        real = DataFrame_test.loc[0, 'VAL'+ element[0]+element[1:].lower()+'_pr']
        # сравниваем текущее значение и реальное
        if real > target:
            bound = bound[bound['Элемент'] != element]

    # рассчитываем необходимое колличесво добавок
    bound = requiredAdditive(DataFrame_test, bound)

    # находим оптимальные материалы и вес этих материалов для легирования
    for i in library_alloying.keys():
        # маргане и кремний (отдельно рассматриваем в виду наличия общего ферроматериала MnSi75A)
        if i == 2:
            if 'SI' or 'Mn' in bound['Элемент'].value_counts().index:
                bound = alloyingMnSI(bound, ferro, assimilation, library_ferroalloys)
            # если нет необходимости легировать - пропускаем
            else:
                continue
        # все остальные элементы
        else:
            element = library_alloying[i]
            # если нет необходимости легировать данный элемент - пропускаем
            if bound[bound['Элемент'] == element[0].upper()].shape[0] < 1:
                continue
            bound = alloying(bound, element, ferro, assimilation, short, material_cods, library_ferroalloys)

    # заполняем начальное приближение для оптимизации
    initial_fit_params = []
    for i in bound.index:
        initial_fit_params.append(bound.loc[i, 'm'])

    # чтобы не было отрицальных значений
    cons = ({'type': 'ineq', 'fun': lambda x: x})

    # минимизируем функцию методом 'COBYLA'
    # начальный шаг 'rhobeg': 10
    a = minimize(lambda fit_params:
                 penaltyFunction(fit_params, DataFrame_test, bound, ferro, assimilation, models, columns, 1000),
                 initial_fit_params, method='COBYLA',
                 constraints=cons, options={'rhobeg': 10})

    # записываем в bound (может нужно будет, чтобы тестировать)
    bound.reset_index(inplace=True, drop=True)
    for i in bound.index:
        bound.loc[i, 'm_model'] = a.x[i]
    print(bound[['Ферроматериал','val', 'm', 'm_model']])
    # записываем данные в выходной датафрейм
    time = datetime.now()
    for i in bound.index:
        # текущее время
        recommendation.loc[i, 'Время добавки'] = time
        # код материала
        cod = material_cods[material_cods['DESC_C'] == bound.loc[i, 'Ферроматериал']]['MAT_CODE'].values[0]
        recommendation.loc[i, 'Код'] = cod
        # добавляемый ферроматериал и его масса
        recommendation.loc[i, 'Описание'] = bound.loc[i, 'Ферроматериал']
        recommendation.loc[i, 'Масса'] = round(bound.loc[i, 'm_model'] + 0.45)

    return recommendation
#-----------------------------------------------------------------------------------------------------------------------
