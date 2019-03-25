import pandas as pd
from datetime import datetime, timedelta
from libraries.sortFiles import getTwoLast, delUnnecessaryFiles, open_DF
#-----------------------------------------------------------------------------------------------------------------------
def addMelting(dataFrame, name_dir, mark, counter):
    signal_st = 'L2LF03'
    LF_TlgSender, LF_TlgSender_dop = getTwoLast(name_dir + '/LF_OUT')
    tel_grade = open_DF(name_dir + '/LF_OUT/' + LF_TlgSender)

    # при необходимости открываем дополнительный файл
    if tel_grade[tel_grade[3] == signal_st].shape[0] == 0:
        tel_grade_dop = open_DF(name_dir + '/LF_OUT/' + LF_TlgSender_dop)
        tel_grade = tel_grade_dop.copy()

    # удаляем файлы
    # if counter == 0:
    #     delUnnecessaryFiles(name_dir + '/LF_OUT')

    # извлекаем номер плавки, марку стали, время начала плавки
    tel_grade = tel_grade[tel_grade[3] == signal_st]
    tel_grade = tel_grade[tel_grade.index == max(tel_grade.index)]
    tel_grade.reset_index(inplace=True, drop=True)
    melting = tel_grade.iloc[0, 19]
    steel_grade = mark[mark['STEELGRADECODE'] == tel_grade.iloc[0, 21]]['STEELGRADECODEDESC_C'].values[0]
    for i in range(tel_grade.shape[0]):
        time_grade = datetime(int(tel_grade.iloc[i, 11]), int(tel_grade.iloc[i, 12]),
                              int(tel_grade.iloc[i, 13]), int(tel_grade.iloc[i, 14]),
                              int(tel_grade.iloc[i, 15]), int(tel_grade.iloc[i, 16]))
        tel_grade.loc[i, 'data_time'] = time_grade
    time_start = tel_grade.loc[0, 'data_time']
    cod_steel_grade = tel_grade.iloc[0, 21]

    # записываем номер плавки, марку стали, время начала плавки и текущее время
    dataFrame.loc[0, 'Время'] = datetime.now()
    dataFrame.loc[0, 'Время начала плавки'] = time_start
    dataFrame.loc[0, 'Номер плавки'] = melting
    dataFrame.loc[0, 'Марка стали'] = steel_grade
    dataFrame.loc[0, 'Код марки стали'] = cod_steel_grade

    return dataFrame
#-----------------------------------------------------------------------------------------------------------------------
def addWeight(name_dir, melting, counter):
    signal_w = 'EAL270'
    EAF, EAF_dop = getTwoLast(name_dir + '/EAF')
    tel_EAF = open_DF(name_dir + '/EAF/' + EAF)
    tel_EAF = tel_EAF[(tel_EAF[3] == signal_w) & (tel_EAF[19] == melting)]

    # удаляем файлы
    # delUnnecessaryFiles(name_dir + '/EAF')

    # добавляем дополнительный файл
    if EAF_dop != None:
        tel_EAF_dop = open_DF(name_dir + '/EAF/' + EAF_dop)
        tel_EAF_dop = tel_EAF_dop[
            (tel_EAF_dop[3] == signal_w) & (tel_EAF_dop[19] == melting)]
        tel_EAF = pd.concat([tel_EAF_dop, tel_EAF])
    tel_EAF.reset_index(inplace=True, drop=True)
    try:
        bucket_mass = int(tel_EAF.loc[tel_EAF[22]=='11', 23].values[0])
        all_mass = int(tel_EAF.loc[tel_EAF[22]=='12', 23].values[0])
        m = all_mass - bucket_mass
    except IndexError:
        m = 130000

    print('Massa: ', m)
    return m
#-----------------------------------------------------------------------------------------------------------------------
def addWeightEAL(dataFrame, name_dir, counter):
    signal_w = 'EAL260'
    melting = dataFrame.loc[0, 'Номер плавки']
    EAF, EAF_dop = getTwoLast(name_dir + '/EAF')
    tel_EAF = open_DF(name_dir + '/EAF/' + EAF)
    tel_EAF = tel_EAF[(tel_EAF[3] == signal_w)&(tel_EAF[19] == melting)&(tel_EAF[22] == '1000')&(tel_EAF[23] == '9')]

    # добавляем дополнительный файл
    if EAF_dop != None:
        tel_EAF_dop = open_DF(name_dir + '/EAF/' + EAF_dop)
        tel_EAF_dop = tel_EAF_dop[
            (tel_EAF_dop[3] == signal_w) & (tel_EAF_dop[19] == melting) & (tel_EAF_dop[22] == '1000') & (
                    tel_EAF_dop[23] == '9')]
        tel_EAF = pd.concat([tel_EAF_dop, tel_EAF])
    tel_EAF.reset_index(inplace=True, drop=True)

    # удаляем файлы
    # if counter == 0:
    #   delUnnecessaryFiles(name_dir + '/EAF')

    # находим массут добавок на ДСП
    m = 0
    for i in range(tel_EAF.shape[0]):
        st = tel_EAF.iloc[i]
        for j in range(25, 55, 3):
            if (int(st[j]) != 360258) & (int(st[j]) != 140107) & (int(st[j]) != 364301) & (int(st[j]) != 364300):
                m += int(st[j + 1])

    dataFrame.loc[0, 'm'] = m * 0.905

    return dataFrame
#-----------------------------------------------------------------------------------------------------------------------
def addChemistry(dataFrame, name_dir):
    columns_xim = ['VALC', 'VALSI', 'VALMN', 'VALP', 'VALS', 'VALAL', 'VALALS', 'VALCU',
           'VALCR', 'VALMO', 'VALNI', 'VALV', 'VALTI', 'VALNB', 'VALCA', 'VALCO',
           'VALPB', 'VALW', 'VALCE', 'VALB', 'VALAS', 'VALSN', 'VALBI', 'VALZR',
           'VALO', 'VALN']
    columns = ['Марка стали', 'Последний замер химии', 'm'] + columns_xim + ['Время начала плавки']

    him = pd.DataFrame(columns=columns)
    melting = dataFrame.loc[0, 'Номер плавки']
    Lab, Lab_dop = getTwoLast(name_dir + '/LAB')
    tel_chemical = open_DF(name_dir + '/LAB/' + Lab)
    tel_chemical = tel_chemical[(tel_chemical[22] == 'L1') & (tel_chemical[11] == melting + '  ')]

    # добавляем дополнительный файл
    if Lab_dop != None:
        tel_chemical_dop = open_DF(name_dir + '/LAB/' + Lab_dop)
        tel_chemical_dop = tel_chemical_dop[(tel_chemical_dop[22] == 'L1') & (tel_chemical_dop[11] == melting + '  ')]
        tel_chemical = pd.concat([tel_chemical, tel_chemical_dop])
    tel_chemical.reset_index(inplace=True, drop=True)

    xim = {'VALC': 33, 'VALSI': 34, 'VALMN': 35, 'VALP': 36, 'VALS': 37, 'VALAL': 38, 'VALALS': 39, 'VALCU': 40,
           'VALCR': 41, 'VALMO': 42, 'VALNI': 43, 'VALV': 44, 'VALTI': 45, 'VALNB': 46, 'VALCA': 47, 'VALCO': 48,
           'VALPB': 49, 'VALW': 50, 'VALCE': 52, 'VALB': 53, 'VALAS': 54, 'VALSN': 55, 'VALBI': 56, 'VALZR': 58,
           'VALO': 59, 'VALN': 60}

    # проверяем колличесво замеров химии
    flag = tel_chemical.shape[0]
    if flag > 0:
        for i in range(tel_chemical.shape[0]):
            if len(tel_chemical.iloc[i, 13]) < 3:
                time_xim = datetime(int('20' + tel_chemical.iloc[i, 13]), int(tel_chemical.iloc[i, 14]),
                                    int(tel_chemical.iloc[i, 15]), int(tel_chemical.iloc[i, 16]),
                                    int(tel_chemical.iloc[i, 17]), int(tel_chemical.iloc[i, 18]))
            else:
                time_xim = datetime(int(tel_chemical.iloc[i, 13]), int(tel_chemical.iloc[i, 14]),
                                    int(tel_chemical.iloc[i, 15]), int(tel_chemical.iloc[i, 16]),
                                    int(tel_chemical.iloc[i, 17]), int(tel_chemical.iloc[i, 18]))

            tel_chemical.loc[i, 'data_time'] = time_xim
        for i in range(tel_chemical.shape[0]):
            for j in columns_xim:
                him.loc[i, j] = round(float(tel_chemical.iloc[i, xim[j]]), 4)
            him.loc[i, 'Последний замер химии'] = tel_chemical.iloc[i, 74]

    him['Марка стали'] = dataFrame.loc[0, 'Марка стали']
    him.reset_index(inplace=True, drop=True)
    return him, flag
# -----------------------------------------------------------------------------------------------------------------------
def addMeasurementChemistry(dataFrame, name_dir, counter, flag):
    melting = dataFrame.loc[0, 'Номер плавки']
    Lab, Lab_dop = getTwoLast(name_dir + '/LAB')
    tel_chemical = open_DF(name_dir + '/LAB/' + Lab)
    tel_chemical = tel_chemical[(tel_chemical[22] == 'L1') & (tel_chemical[11] == melting + '  ')]

    # добавляем дополнительный файл
    if Lab_dop != None:
        tel_chemical_dop = open_DF(name_dir + '/LAB/' + Lab_dop)
        tel_chemical_dop = tel_chemical_dop[(tel_chemical_dop[22] == 'L1') & (tel_chemical_dop[11] == melting + '  ')]
        tel_chemical = pd.concat([tel_chemical, tel_chemical_dop])
    tel_chemical.reset_index(inplace=True, drop=True)

    # удаляем файлы
    if counter == 0:
        delUnnecessaryFiles(name_dir + '/LAB')

    if flag > 0:
        for i in range(tel_chemical.shape[0]):
            if len(tel_chemical.iloc[i, 13]) < 3:
                time_xim = datetime(int('20' + tel_chemical.iloc[i, 13]), int(tel_chemical.iloc[i, 14]),
                                    int(tel_chemical.iloc[i, 15]), int(tel_chemical.iloc[i, 16]),
                                    int(tel_chemical.iloc[i, 17]), int(tel_chemical.iloc[i, 18]))
            else:
                time_xim = datetime(int(tel_chemical.iloc[i, 13]), int(tel_chemical.iloc[i, 14]),
                                    int(tel_chemical.iloc[i, 15]), int(tel_chemical.iloc[i, 16]),
                                    int(tel_chemical.iloc[i, 17]), int(tel_chemical.iloc[i, 18]))

            tel_chemical.loc[i, 'data_time'] = time_xim

        ind_ch = tel_chemical[tel_chemical['data_time'] == max(tel_chemical['data_time'].value_counts().index)].index[0]

        # чтобы сопоставить столбцы в телеграмме со значением элементов
        xim = {'VALC': 33, 'VALSI': 34, 'VALMN': 35, 'VALP': 36, 'VALS': 37, 'VALAL': 38, 'VALALS': 39, 'VALCU': 40,
               'VALCR': 41, 'VALMO': 42, 'VALNI': 43, 'VALV': 44, 'VALTI': 45, 'VALNB': 46, 'VALCA': 47, 'VALCO': 48,
               'VALPB': 49, 'VALW': 50, 'VALCE': 52, 'VALB': 53, 'VALAS': 54, 'VALSN': 55, 'VALBI': 56, 'VALZR': 58,
               'VALO': 59, 'VALN': 60}
        t = ['VALC','VALSI','VALMN','VALP','VALS','VALAL','VALALS','VALCU','VALCR','VALMO','VALNI','VALV','VALTI',
                  'VALNB','VALCA','VALCO','VALPB','VALW','VALCE','VALB','VALAS','VALSN','VALBI','VALZR','VALO','VALN']
        for x_el in t:
            dataFrame.loc[0, x_el] = round(float(tel_chemical.iloc[ind_ch, xim[x_el]]), 4)
            if dataFrame.loc[0, x_el] < 0:
                dataFrame.loc[0, x_el] = 0

        # время замера химии
        dataFrame.loc[0, 'Последний замер химии'] = tel_chemical.iloc[ind_ch, 74]

        #дельта по времени
        t = dataFrame.iloc[0, 0] - dataFrame.iloc[0, 3]
        dataFrame.loc[0, 'TIME'] = round(t.seconds / 60)

    return dataFrame
#-----------------------------------------------------------------------------------------------------------------------
def addMainInformation(dataFrame, name_dir, counter, temperature, all_additive, material, titles_for_temp, flag):
    signal_t = 'LFL211'
    signal_el = 'LFL223'
    signal_mat = 'LFL260'
    signal_argon = 'LFL226'
    melting = dataFrame.loc[0, 'Номер плавки']
    for_temp = pd.DataFrame(columns=titles_for_temp)
    for i in titles_for_temp[5:]:
        for_temp.loc[0, i] = 0
    LF_TlgReceiver, LF_TlgReceiver_dop = getTwoLast(name_dir + '/LF')
    tel_main = open_DF(name_dir + '/LF/' + LF_TlgReceiver)
    tel_main = tel_main[(tel_main[19] == melting) & (
            (tel_main[3] == signal_t) | (tel_main[3] == signal_mat) | (tel_main[3] == signal_el)
            | (tel_main[3] == signal_argon))]

    # добавляем дополнительный файл
    if LF_TlgReceiver_dop != None:
        tel_main_dop = open_DF(name_dir + '/LF/' + LF_TlgReceiver_dop)
        tel_main_dop = tel_main_dop[(tel_main_dop[19] == melting) & (
                (tel_main_dop[3] == signal_t) | (tel_main_dop[3] == signal_mat) | (tel_main_dop[3] == signal_el)
                | (tel_main_dop[3] == signal_argon))]
        tel_main = pd.concat([tel_main_dop, tel_main])
    tel_main.reset_index(inplace=True, drop=True)

    # удаляем файлы
    # if counter ==0:
    #     delUnnecessaryFiles(name_dir + '/LF')

    # добавляем время в нужном формате
    for i in range(tel_main.shape[0]):
        time_main = datetime(int(tel_main.iloc[i, 11]), int(tel_main.iloc[i, 12]),
                             int(tel_main.iloc[i, 13]), int(tel_main.iloc[i, 14]),
                             int(tel_main.iloc[i, 15]), int(tel_main.iloc[i, 16]))
        tel_main.loc[i, 'data_time'] = time_main

    # заполняем датафрейм с замерами температуры
    temp = tel_main[tel_main[3] == signal_t]
    temp.reset_index(inplace=True, drop=True)
    for i in range(temp.shape[0]):
        if (int(temp.loc[i, 24]) > 3000) or (int(temp.loc[i, 24])<1000):
             continue
        temperature.loc[i, 'Номер плавки'] = melting
        temperature.loc[i, 'Время замера температуры'] = temp.loc[i, 'data_time']
        temperature.loc[i, 'TEMP'] = temp.loc[i, 24]
        temperature.loc[i, 'Время начала плавки'] = dataFrame.loc[0, 'Время начала плавки']
        if temp.loc[i, 23] == '2':
            temperature.loc[i, 'Окисленность'] = int(temp.loc[i, 25])/1000
        else:
            temperature.loc[i, 'Окисленность'] = None

    # заполняем датафрейм для прогнозирования температуры
    flag_temp = temperature.shape[0]
    if flag_temp > 0:
        ind_temp = temperature[temperature['Время замера температуры'] == max(temperature['Время замера температуры'].value_counts().index)].index[0]
        for_temp.loc[0, 'TEMP'] = temperature.loc[ind_temp, 'TEMP']
        for_temp.loc[0, 'Время замера температуры'] = temperature.loc[ind_temp, 'Время замера температуры']
        for_temp.loc[0, 'Время'] = datetime.now()
        t = for_temp.loc[0, 'Время'] - for_temp.loc[0, 'Время замера температуры']
        for_temp.loc[0, 'TIME'] = round(t.seconds / 60)


    # заполняем датафрейм с добавками митериала
    temp = tel_main[(tel_main[3] == signal_mat) & (tel_main[25] == '9')]
    temp.reset_index(inplace=True, drop=True)
    k = 0
    for i in range(temp.shape[0]):
        st = temp.iloc[i]
        for j in range(27, 47, 2):
            if int(st[j]) != 0:
                all_additive.loc[k, 'Время добавки'] = temp.loc[i, 'data_time']
                all_additive.loc[k, 'Код'] = temp.iloc[i][j]
                all_additive.loc[k, 'Описание'] = material[material['MAT_CODE']==int(temp.iloc[i][j])]['DESC_C'].values[0]
                all_additive.loc[k, 'Масса'] = int(st[j + 1])
                k += 1

    # добавляем электроэнерггию для прогнозирования темпеартуры
    if flag_temp > 0:
        temp = tel_main[
            (tel_main[3] == signal_el) & (tel_main['data_time'] > for_temp.loc[0, 'Время замера температуры']) &
            (tel_main['data_time'] < for_temp.loc[0, 'Время'])]
        if len(temp['data_time']) != 0:
            w0 = temp[temp['data_time'] == min(temp['data_time'])][22].values[0]
            w1 = temp[temp['data_time'] == max(temp['data_time'])][22].values[0]
            w = (int(w1) - int(w0)) / 1000
        else:
            w = 0
        for_temp.loc[0, 'W'] = w

    # добавляем расход аргнона для прогнозирования температуры
    if flag_temp > 0:
        temp = tel_main[
            (tel_main[3] == signal_argon) & (tel_main['data_time'] > for_temp.loc[0, 'Время замера температуры']) &
            (tel_main['data_time'] < for_temp.loc[0, 'Время'])]

        if len(temp['data_time']) != 0:
            argon01 = int(temp[temp['data_time'] == min(temp['data_time'])][32].values[0])
            argon02 = int(temp[temp['data_time'] == min(temp['data_time'])][33].values[0])
            argon1 = int(temp[temp['data_time'] == max(temp['data_time'])][32].values[0])
            argon2 = int(temp[temp['data_time'] == max(temp['data_time'])][33].values[0])
            argon = (argon1-argon01+argon2-argon02)/1000

        else:
            argon = 0
        for_temp.loc[0, 'ARGONAM_IN'] = argon
        print('Argon: ', argon)

    # добавляем добавки материалов для прогнозирования температуры
    if flag_temp > 0:
        temp = tel_main[
            (tel_main[3] == signal_mat) & (tel_main['data_time'] > for_temp.loc[0, 'Время замера температуры']) & (
                    tel_main[25] == '9')]
        temp.reset_index(inplace=True, drop=True)
        for i in range(temp.shape[0]):
            st = temp.iloc[i]
            for j in range(27, 47, 2):
                if int(st[j]) != 0:
                    mat = material[material['MAT_CODE'] == int(temp.iloc[i][j])]['DESC_C'].value_counts().index[0]
                    try:
                        for_temp.loc[0, mat] += int(st[j + 1])
                    except KeyError:
                        try:
                            mat = \
                                material[material['MAT_CODE'] == int(temp.iloc[i][j])][
                                    'DESC_C_dop'].value_counts().index[
                                    0]
                            for_temp.loc[0, mat] += int(st[j + 1])
                        except IndexError:
                            for_temp[mat] = int(st[j + 1])

    if flag > 0 and tel_main.shape[0] > 0:

        # добавляем температуру
        temp = tel_main[(tel_main[3] == signal_t) & (tel_main['data_time'] <= dataFrame.loc[0, 'Последний замер химии'])]
        try:
            while (True):
                t = temp[temp['data_time'] == max(temp['data_time'].value_counts().index)].iloc[0, 24]
                if (int(t) > 3000) or (int(t) < 1000):
                    temp = temp.drop(temp[temp['data_time'] == max(temp['data_time'].value_counts().index)].index)
                else:
                    dataFrame.loc[0, 'TEMP'] = t
                    break
        except ValueError:
            dataFrame.loc[0, 'TEMP'] = '1580'

        # добавляем электроэнерггию
        temp = tel_main[(tel_main[3] == signal_el) & (tel_main['data_time'] > dataFrame.loc[0, 'Последний замер химии']) &
            (tel_main['data_time'] < dataFrame.loc[0, 'Время'])]
        if len(temp['data_time']) != 0:
            w0 = temp[temp['data_time'] == min(temp['data_time'])][22].values[0]
            w1 = temp[temp['data_time'] == max(temp['data_time'])][22].values[0]
            w = (int(w1) - int(w0)) / 1000
        else:
            w = 0
        dataFrame.loc[0, 'W'] = w

        # добавляем добавки материалов
        temp = tel_main[
            (tel_main[3] == signal_mat) & (tel_main['data_time'] > (dataFrame.loc[0, 'Последний замер химии'] - timedelta(minutes=3))) & (
                        tel_main[25] == '9')]

        temp.reset_index(inplace=True, drop=True)
        for i in range(temp.shape[0]):
            st = temp.iloc[i]
            for j in range(27, 47, 2):
                if int(st[j]) != 0:
                    mat = material[material['MAT_CODE'] == int(temp.iloc[i][j])]['DESC_C'].value_counts().index[0]
                    try:
                        dataFrame.loc[0, mat] += int(st[j + 1])
                    except KeyError:
                        dataFrame[mat] = int(st[j + 1])

    return dataFrame, temperature, all_additive, for_temp, flag_temp
#-----------------------------------------------------------------------------------------------------------------------