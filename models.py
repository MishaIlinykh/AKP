import pandas as pd
from sklearn.externals import joblib
from sklearn import preprocessing
import pickle
import json
#-----------------------------------------------------------------------------------------------------------------------
def __load_model(name_target, dir):
    if name_target == 'TEMP':
        GB = joblib.load(dir + 'model_GB/GB_' + name_target+'2' + '.pkl')
        titles = joblib.load(dir+'model_GB/titles_TEMP2.json')
        sc = joblib.load(dir + 'model_GB/scaler_TEMP2')
        return GB, titles, sc
    else:
        GB = pickle.load(open(dir+'model_GB/'+name_target+'.sav', 'rb'))
        titles = json.load(open(dir + 'model_GB/titles_' + name_target + '.json', "r"))
        return GB, titles
#-----------------------------------------------------------------------------------------------------------------------
def add_models(dir):
    GB_TEMP2, titles_TEMP, sc_TEMP = __load_model('TEMP', dir)
    GB_VALC, titles_VALC = __load_model('VALC', dir)
    GB_VALSI, titles_VALSI = __load_model('VALSI', dir)
    GB_VALMN, titles_VALMN = __load_model('VALMN', dir)
    GB_VALP, titles_VALP = __load_model('VALP', dir)
    GB_VALS, titles_VALS = __load_model('VALS', dir)
    GB_VALAL, titles_VALAL = __load_model('VALAL', dir)
    GB_VALCU, titles_VALCU = __load_model('VALCU', dir)
    GB_VALCR, titles_VALCR = __load_model('VALCR', dir)
    GB_VALMO, titles_VALMO = __load_model('VALMO', dir)
    GB_VALNI, titles_VALNI = __load_model('VALNI', dir)
    GB_VALV, titles_VALV = __load_model('VALV', dir)
    GB_VALTI, titles_VALTI = __load_model('VALTI', dir)
    GB_VALNB, titles_VALNB = __load_model('VALNB', dir)
    GB_VALCA, titles_VALCA = __load_model('VALCA', dir)

    models = {'VALC2': GB_VALC,  'title_VALC':titles_VALC,
              'VALSI2':GB_VALSI, 'title_VALSI':titles_VALSI,
              'VALMN2':GB_VALMN, 'title_VALMN':titles_VALMN,
              'VALP2':GB_VALP,   'title_VALP':titles_VALP,
              'VALS2':GB_VALS,   'title_VALS':titles_VALS,
              'VALAL2':GB_VALAL, 'title_VALAL':titles_VALAL,
              'VALCU2':GB_VALCU, 'title_VALCU':titles_VALCU,
              'VALCR2':GB_VALCR, 'title_VALCR':titles_VALCR,
              'VALMO2':GB_VALMO, 'title_VALMO':titles_VALMO,
              'VALNI2':GB_VALNI, 'title_VALNI':titles_VALNI,
              'VALV2':GB_VALV,   'title_VALV':titles_VALV,
              'VALTI2':GB_VALTI, 'title_VALTI':titles_VALTI,
              'VALNB2':GB_VALNB, 'title_VALNB':titles_VALNB,
              'VALCA2':GB_VALCA, 'title_VALCA':titles_VALCA,
              'TEMP2': GB_TEMP2, 'titles_TEMP': titles_TEMP, 'sc_TEMP': sc_TEMP}
    return models
#-----------------------------------------------------------------------------------------------------------------------
def __for_crutch():
    # Для каждого химического элемента набор материалов,
    # содержащих данный химический элемент в значительном колличесве

    С = ['Графит искусственный 0,1-2,5 мм2', 'КРС-65 брикеты2', 'УСМ 03-10мм2', 'Кокс 10-30 мм2',
         'C 0,5-2,5 mm2', 'Феррохром высокоуглеродистый2']
    Si = ['MnSi17А2', 'ФХ0252', 'ПП-СК30 проволока2', 'алюминий вторичный АВ 872', 'FeSi65-42', 'Гранулы АВ-872',
          'КРС-65 брикеты2', 'ФС 452', 'Ферротитан ФТ352', 'Лигатура ниобиевая ФНСБ2', 'ФСХ 402', 'ФСХ 402']
    Mn = ['MnSi17А2', 'FeV-502', 'Лигатура ванадиевая2', 'Проволока порошковая ФВд502',
          'Концентрат ванадиевый ВКПЛ-102']

    crutch_mat = {'C': С, 'Si': Si, 'Mn': Mn}
    return  crutch_mat
#-----------------------------------------------------------------------------------------------------------------------
def calculation_val(dataFrame, ferro, assimilation):
    # val = m*(Y/100)*(X/100), где
    # m - масса ферросплава
    # X - процентное содержание элемента в ферросплаве
    # Y - коэффицент усвоения
    # Элементы, для которых есть коэффицент усвоения
    a = ['Nb', 'Mo', 'V', 'Ca', 'Al', 'S', 'C', 'Si', 'Mn', 'Cr',
         'Ti', 'Ni']
    m = 0
    col_mat = []
    for i in dataFrame.columns[7:46]:
        col_mat.append(i)
    for i in dataFrame.columns[120:128]:
        col_mat.append(i)
    for i in dataFrame.columns[134:]:
        col_mat.append(i)

    for col_new in ferro.columns[2:]:
        val = 0
        for col in col_mat:
            if dataFrame.loc[0, col] == 0:
                continue
            m = dataFrame.loc[0, col]
            X = ferro[ferro['Описание']==col][col_new].value_counts().index[0]
            if any(col_new in s for s in a):
                Y = assimilation[assimilation['Описание'] == col][col_new].value_counts().index[0]
                val += (m*X/100)*(Y/100)
            else:
                val += m*X/100
        dataFrame.loc[0, col_new] = val
    for col in col_mat:
        m += dataFrame.loc[0, col]
    dataFrame.loc[0, 'm_dob'] = m
    return dataFrame
#-----------------------------------------------------------------------------------------------------------------------
def calculation_chemical(dataFrame, round_coeff):
    # элементы по которым будет производиться рассчет
    a = ['Mn', 'Nb', 'Mo', 'V', 'Si', 'Ca', 'Al', 'S', 'C', 'Cr',
         'Ti', 'Ni', 'P', 'Cu']

    X2 = lambda val, X1, M: ((val * 100) / M) + X1
    for col in a:
        val = dataFrame.loc[0, col]
        X1 = dataFrame.loc[0, 'VAL' + col.upper()]
        estimated_value_m = dataFrame.loc[0, 'm_calk']
        dataFrame.loc[0, 'VAL' + col + '_pr'] = round(X2(val, X1, estimated_value_m), round_coeff)

    return dataFrame
#-----------------------------------------------------------------------------------------------------------------------
def predict(models, test, columns, ferro, assimilation, round_coeff):

    try:
        test.loc[0, 'АТФ-75Б'] == test.loc[0, 'АТФ-75']
        test = test.drop('АТФ-75', 1)
    except KeyError:
        pass
    # добавляем val для каждого химического эллемента
    test = calculation_val(test, ferro, assimilation)
    # рассчитываем содержание
    if round_coeff == 3:
        test = calculation_chemical(test, 4)
    else:
        test = calculation_chemical(test, 6)
    # формируем датафрейм с химией рассчитанной по модели
    pred = pd.DataFrame(columns=columns)
    for i in columns[:4]+columns[30:31:1]:
        pred.loc[0, i] = test.loc[0,i]

    for i in ['C','SI','MN','P','S','AL','CU','CR','MO','NI','V','TI','NB','CA']:
        test_pred = test.copy()
        try:
            test_pred.loc[0, 'УСМ 03-10мм'] = test_pred.loc[0, 'УСМ 03-10мм'] + test_pred.loc[0, 'УСМ 3-10мм']
        except KeyError:
            pass
        test_pred.loc[0, 'FeSi65-4'] = test_pred.loc[0, 'FeSi65-4'] + test_pred.loc[0, 'FeSi75']
        test_pred.loc[0, 'FeSi75'] =0
        test_pred = test_pred[models['title_VAL'+i]]
        if (i == 'MN'):
            pred_value = round(test.loc[0, 'VAL' + i[0] + i[1].lower() + '_pr'], round_coeff)
        elif (i == 'TI') or (i == 'NI'):
            pred_value = test.loc[0, 'VAL' + i[0] + i[1].lower()+ '_pr']
        else:
            pred_value = round(models['VAL' + i + '2'].predict(test_pred)[0], round_coeff)
        pred.loc[0, i] = pred_value

        # Чтобы не вылезали отрицательные значения
        if pred.loc[0, i] < 0:
            pred.loc[0, i] = 0
    return pred, test
#-----------------------------------------------------------------------------------------------------------------------
def predict_TEMP(models, df, for_temp):
    test_temp = for_temp[models['titles_TEMP']]
    test_temp = models['sc_TEMP'].transform(test_temp)
    df.loc[0, 'TEMP'] = round(models['TEMP2'].predict(test_temp)[0])
    print('TEMP: ', round(models['TEMP2'].predict(test_temp)[0]))
    return df
#-----------------------------------------------------------------------------------------------------------------------