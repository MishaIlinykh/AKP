import pandas as pd
from sklearn.externals import joblib
from sklearn import preprocessing
#-----------------------------------------------------------------------------------------------------------------------
def __load_model(name_target, dir):
    if name_target =='empty':
        sc = joblib.load(dir+'model_GB/scaler_VALC2')
        titles = joblib.load(dir+'model_GB/titles_VALC2.json')
        return sc, titles
    if name_target =='S':
        sc = joblib.load(dir+'model_GB/scaler_VALS2')
        titles = joblib.load(dir+'model_GB/titles_VALS2.json')
        return sc, titles
    if name_target == 'TEMP':
        sc = joblib.load(dir+'model_GB/scaler_TEMP2')
        titles = joblib.load(dir+'model_GB/titles_TEMP2.json')
        return sc, titles
    else:
        GB = joblib.load(dir+'model_GB/GB_'+name_target+'.pkl')
        return GB
#-----------------------------------------------------------------------------------------------------------------------
def add_models(dir):
    sc, titles = __load_model('empty', dir)
    sc_VALS, titles_VALS = __load_model('S', dir)
    sc_TEMP, titles_TEMP = __load_model('TEMP', dir)
    GB_TEMP2 = __load_model('TEMP2', dir)
    GB_VALC = __load_model('VALC2', dir)
    GB_VALSI = __load_model('VALSI2', dir)
    GB_VALMN = __load_model('VALMN2', dir)
    GB_VALP = __load_model('VALP2', dir)
    GB_VALS = __load_model('VALS2', dir)
    GB_VALAL = __load_model('VALAL2', dir)
    GB_VALALS = __load_model('VALALS2', dir)
    GB_VALCU = __load_model('VALCU2', dir)
    GB_VALCR = __load_model('VALCR2', dir)
    GB_VALMO = __load_model('VALMO2', dir)
    GB_VALNI = __load_model('VALNI2', dir)
    GB_VALV = __load_model('VALV2', dir)
    GB_VALTI = __load_model('VALTI2', dir)
    GB_VALNB = __load_model('VALNB2', dir)
    GB_VALCA = __load_model('VALCA2', dir)
    GB_VALCO = __load_model('VALCO2', dir)
    GB_VALPB = __load_model('VALPB2', dir)
    GB_VALW = __load_model('VALW2', dir)
    GB_VALCE = __load_model('VALCE2', dir)
    GB_VALB = __load_model('VALB2', dir)
    GB_VALAS = __load_model('VALAS2', dir)
    GB_VALSN = __load_model('VALSN2', dir)
    GB_VALBI = __load_model('VALBI2', dir)
    GB_VALZR = __load_model('VALZR2', dir)
    GB_VALO = __load_model('VALO2', dir)
    GB_VALN = __load_model('VALN2', dir)
    models = {'TEMP2': GB_TEMP2, 'VALC2': GB_VALC, 'VALSI2':GB_VALSI,
      'VALMN2':GB_VALMN, 'VALP2':GB_VALP, 'VALS2':GB_VALS,
      'VALAL2':GB_VALAL, 'VALALS2':GB_VALALS, 'VALCU2':GB_VALCU,
      'VALCR2':GB_VALCR, 'VALMO2':GB_VALMO, 'VALNI2':GB_VALNI,
      'VALV2':GB_VALV, 'VALTI2':GB_VALTI, 'VALNB2':GB_VALNB,
      'VALCA2':GB_VALCA, 'VALCO2':GB_VALCO, 'VALPB2':GB_VALPB,
      'VALW2':GB_VALW, 'VALCE2':GB_VALCE, 'VALB2':GB_VALB,
      'VALAS2':GB_VALAS, 'VALSN2':GB_VALSN, 'VALBI2':GB_VALBI,
      'VALZR2':GB_VALZR, 'VALO2':GB_VALO, 'VALN2':GB_VALN,
      'titles':titles, 'sc':sc, 'title_VALS':titles_VALS, 'sc_VALS': sc_VALS,
      'sc_TEMP': sc_TEMP, 'titles_TEMP': titles_TEMP}
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
def predict(models, test, columns, all_titils):
    crutch_mat = __for_crutch()
    # Находим массу всех добавок
    m_all, m_C, m_Si, m_Mn = 0, 0, 0, 0

    for i in all_titils[34:112]:
        m_all += test.loc[0, i]
        if i in crutch_mat['C']:
            m_C += test.loc[0, i]
        if i in crutch_mat['Si']:
            m_Si += test.loc[0, i]
        if i in crutch_mat['Mn']:
            m_Mn += test.loc[0, i]

    pred = pd.DataFrame(columns=columns)
    for i in columns[:4]+columns[30:31:1]:
        pred.loc[0, i] = test.loc[0,i]
    test_pred = test[models['titles']]
    test_pred = models['sc'].transform(test_pred)
    test_pred_S = test[models['title_VALS']]
    test_pred_S = models['sc_VALS'].transform(test_pred_S)
    for i in columns[4:30]:
        if i == 'S':
            pred_value = round(models['VAL' + i + '2'].predict(test_pred_S)[0], 3)
            pred.loc[0, i] = pred_value
        elif i !='TEMP':
            pred_value = round(models['VAL'+i+'2'].predict(test_pred)[0], 3)
            if (m_all == 0) and (pred_value > test.loc[0, 'VAL'+i]):
                pred.loc[0, i] = test.loc[0, 'VAL'+i]
            elif (i=='C') and (m_C == 0) and (pred_value > test.loc[0, 'VAL'+i]):
                pred.loc[0, i] = test.loc[0, 'VAL'+i]
            elif (i=='SI') and (m_Si==0) and (pred_value > test.loc[0, 'VAL'+i]):
                pred.loc[0, i] = test.loc[0, 'VAL'+i]
            elif (i =='MN') and (m_Mn==0) and (pred_value > test.loc[0, 'VAL'+i]):
                pred.loc[0, i] = test.loc[0, 'VAL'+i]
            else:
                pred.loc[0, i] = pred_value

            # Чтобы не вылезали отрицательные значения
            if pred.loc[0, i] < 0:
                pred.loc[0, i] = 0
    return pred
#-----------------------------------------------------------------------------------------------------------------------
def predict_TEMP(models, df, for_temp):
    test_temp = for_temp[models['titles_TEMP']]
    test_temp = models['sc_TEMP'].transform(test_temp)
    df.loc[0, 'TEMP'] = round(models['TEMP2'].predict(test_temp)[0])
    print('TEMP: ', round(models['TEMP2'].predict(test_temp)[0]))
    return df
#-----------------------------------------------------------------------------------------------------------------------
def __mass_element_newCoef(ferro, assimilation, assimilation_add, test, element):
    val = 0
    a = ['Nb', 'Mo', 'V', 'Ca', 'Al', 'S',
         'C', 'Si', 'Mn', 'Cr', 'Ti', 'Ni']
    c = []
    for i in test.columns[34:112]:
        c.append(i)
    for i in test.columns[114:]:
        c.append(i)

    for col in c:
        if test.loc[0, col] <= 0:
            continue
        col = col[:-1]
        if ferro[ferro['Описание'] == col]['Шлакообразующий'].values[0] == 1:
            continue
        m = test.loc[0, col + '2']
        X = ferro[ferro['Описание'] == col][element].values[0]
        if X == 0:
            continue
        if any(element in s for s in a):
            if assimilation_add[assimilation_add['Описание'] == col][element].values[0] == -1:
                Y = assimilation[assimilation['Описание'] == col][element].values[0]
            else:
                Y = assimilation_add[assimilation_add['Описание'] == col][element].values[0]
            val += m  * (X/ 100) * (Y / 100)
        else:
            val += m * (X / 100)
    return val
#-----------------------------------------------------------------------------------------------------------------------
def __mass_element(ferro, assimilation, test, element):
    val = 0
    a = ['Nb', 'Mo', 'V', 'Ca', 'Al', 'S',
         'C', 'Si', 'Mn', 'Cr', 'Ti', 'Ni']
    c = []
    for i in test.columns[34:112]:
        c.append(i)
    for i in test.columns[114:]:
        c.append(i)

    for col in c:
        if test.loc[0, col] <= 0:
            continue
        col = col[:-1]
        if ferro[ferro['Описание'] == col]['Шлакообразующий'].values[0] == 1:
            continue
        m = test.loc[0, col + '2']
        X = ferro[ferro['Описание'] == col][element].values[0]
        if X == 0:
            continue
        if any(element in s for s in a):
            Y = assimilation[assimilation['Описание'] == col][element].values[0]
            val += m  * (X/ 100) * (Y / 100)
        else:
            val += m * (X / 100)

    return val
#-----------------------------------------------------------------------------------------------------------------------
def chemicalCalculation(test, weight, columns, ferro, assimilation, assimilation_add, reference):
    # X2 = (Y*m*X) / (M*1,0201*100) + X1
    calculation = pd.DataFrame(columns=columns)
    c = ['C', 'Si', 'Mn', 'Al', 'Cu', 'Cr',
         'Mo', 'Ni', 'V', 'Ti', 'Nb']
    for i in columns[:4]+columns[30:32:1]:
        calculation.loc[0, i] = test.loc[0,i]
    for i in c:
        if reference == 'chCalc_newCoef':
            mass_element = __mass_element_newCoef(ferro, assimilation, assimilation_add, test, i)
        else:
            mass_element = __mass_element(ferro, assimilation, test, i)
        X1 = test.loc[0, 'VAL'+i.upper()]
        calculation.loc[0, i.upper()] = round((mass_element/(weight)*100 + X1), 3)

    return calculation
#-----------------------------------------------------------------------------------------------------------------------