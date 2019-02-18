import pandas as pd
import numpy as np
import os, stat
#-----------------------------------------------------------------------------------------------------------------------
def save_for_verification(data, data_him, dir):
    direct = dir + 'save/' + data.loc[0, 'Номер плавки']
    if os.path.exists(direct) == False:
        os.mkdir(direct)
    data.to_excel(direct + '/all.xls')

    # col = list(data.columns)
    # col.remove('Время')
    # VAL2 = ['VALC2', 'VALSI2', 'VALMN2', 'VALP2', 'VALS2', 'VALAL2', 'VALALS2',
    #    'VALCU2', 'VALCR2', 'VALMO2', 'VALNI2', 'VALV2', 'VALTI2', 'VALNB2',
    #    'VALCA2', 'VALCO2', 'VALPB2', 'VALW2', 'VALCE2', 'VALB2', 'VALAS2',
    #    'VALSN2', 'VALBI2', 'VALZR2', 'VALO2', 'VALN2']
    # df_save = pd.DataFrame(columns = col + VAL2+['Последний замер химии2'])
    # data_him.reset_index(inplace=True, drop=True)
    # for i in range(1, data_him.shape[0]):
    #     for j in VAL2:
    #         df_save.loc[i-1, j[:-1]] = data_him.loc[i-1,j[:-1]]
    #         df_save.loc[i-1, j] = data_him.loc[i, j[:-1]]
    #     df_save.loc[i-1, 'Последний замер химии'] = data_him.loc[i-1, 'Последний замер химии']
    #     df_save.loc[i-1, 'Последний замер химии2'] = data_him.loc[i, 'Последний замер химии']
    #     t = df_save.loc[i-1, 'Последний замер химии2'] - df_save.loc[i-1, 'Последний замер химии']
    #     df_save.loc[i-1, 'time'] = round(t.seconds / 60)
    #
    #     time = df_save.loc[i-1, 'Последний замер химии2']
    #     temp = data[data['Время'] == min(data.Время, key=lambda datetime: abs(time - datetime))]
    #     temp.reset_index(inplace=True, drop=True)
    #     for j in (col[:2] + col[3:5] + col[32:]):
    #         df_save.loc[i-1, j] = temp[0, j]
    #
    # dir = 'C:/Users/Anastasiya.Mittseva/Desktop/AKP/new2/save/save_for_train.xlsx'
    # try:
    #     df = pd.read_excel(dir)
    #     for i in set(df.columns).difference(df_save.columns):
    #         df_save[i] = 0
    #     for i in set(df_save.columns).difference(df.columns):
    #         df[i] = 0
    #     df_save = df_save[df.columns]
    #     df = pd.concat([df, df_save])
    #     df.to_excel(dir)
    #
    # except FileNotFoundError:
    #     df_save.to_excel(dir)
#-----------------------------------------------------------------------------------------------------------------------
def save_for_analysis(data_object, data_him, dir, file_name):
    col = ['Номер плавки', 'Марка стали', 'Время замера', 'Время предсказания',
           'C_real','C_pr', 'SI_real', 'SI_pr', 'MN_real','MN_pr', 'P_real', 'P_pr', 'S_real', 'S_pr',
           'AL_real', 'AL_pr', 'ALS_real', 'ALS_pr', 'CU_real', 'CU_pr', 'CR_real', 'CR_pr',
           'MO_real','MO_pr', 'NI_real', 'NI_pr', 'V_real', 'V_pr', 'TI_real', 'TI_pr',
           'NB_real', 'NB_pr', 'CA_real', 'CA_pr', 'CO_real', 'CO_pr', 'PB_real', 'PB_pr',
           'W_real', 'W_pr', 'CE_real', 'CE_pr', 'B_real', 'B_pr', 'AS_real', 'AS_pr', 'SN_real', 'SN_pr',
           'BI_real', 'BI_pr', 'ZR_real', 'ZR_pr', 'O_real', 'O_pr', 'N_real', 'N_pr']
    df_save = pd.DataFrame(columns = col)

    for i in range(1, data_him.shape[0]):
        time = data_him.loc[i, 'Последний замер химии']
        temp = data_object[data_object['Время'] == min(data_object.Время, key=lambda datetime: abs(time - datetime))]
        temp.reset_index(inplace=True, drop=True)
        df_save.loc[i, 'Номер плавки'] = temp.loc[0, 'Номер плавки']
        df_save.loc[i, 'Марка стали'] = temp.loc[0, 'Марка стали']
        df_save.loc[i, 'Время замера'] = time
        df_save.loc[i, 'Время предсказания'] = temp.loc[0, 'Время']

        for columns in col[4::2]:
            df_save.loc[i, columns] = data_him.loc[i, 'VAL' + columns[:-5]]
        for columns in col[5::2]:
            df_save.loc[i, columns] = temp.loc[0, columns[:-3]]

    dir = dir + '/save/' + file_name+ '.xlsx'
    try:
        df = pd.read_excel(dir)
        df = pd.concat([df, df_save])
        df.to_excel(dir)

    except FileNotFoundError:
        df_save.to_excel(dir)
#-----------------------------------------------------------------------------------------------------------------------
def save_for_analysis_temp(data_object, data_temp, dir):
    col = ['Номер плавки', 'Марка стали', 'Время замера', 'Время предсказания',
           'TEMP_real', 'TEMP_pr']
    df_save = pd.DataFrame(columns=col)

    for i in range(1, data_temp.shape[0]):
        time = data_temp.loc[i, 'Время замера температуры']
        temp = data_object[data_object['Время'] == min(data_object.Время, key=lambda datetime: abs(time - datetime))]
        temp.reset_index(inplace=True, drop=True)
        df_save.loc[i, 'Номер плавки'] = temp.loc[0, 'Номер плавки']
        df_save.loc[i, 'Марка стали'] = temp.loc[0, 'Марка стали']
        df_save.loc[i, 'Время замера'] = time
        df_save.loc[i, 'Время предсказания'] = temp.loc[0, 'Время']
        df_save.loc[i, 'TEMP_real'] = data_temp.loc[i, 'TEMP']
        df_save.loc[i, 'TEMP_pr'] = temp.loc[0, 'TEMP']

    dir = dir + '/save/' + 'save_for_analysis_temp' + '.xlsx'
    try:
        df = pd.read_excel(dir)
        df = pd.concat([df, df_save])
        df.to_excel(dir)

    except FileNotFoundError:
        df_save.to_excel(dir)
#-----------------------------------------------------------------------------------------------------------------------
def __auxiliary_function(additive, fer, el, ferro):
    for i in additive['Описание'].value_counts().index:
        if i == fer:
            continue
        if ferro[ferro['Описание'] == i][el].values[0] > 5:
            return True
    return False
#-----------------------------------------------------------------------------------------------------------------------
def save_assimilation_coef(additive, weight, data_him, ferro, assimilation, dir, flag):
    df = pd.read_excel(dir+'files/assimilation_add.xlsx')
    additive = additive[(additive['Время добавки'] > data_him.loc[flag-2, 'Последний замер химии']) & (additive['Время добавки'] < data_him.loc[flag-1, 'Последний замер химии'])]
    # Химические элементы, для которых расчитываеться коэффицент усвоения
    xim_el =['Nb', 'Mo', 'V', 'Ca', 'Al', 'S',
        'C', 'Si', 'Mn', 'Cr', 'Ti', 'Ni']
    for el in xim_el:
        # Перебираем все добавленные материалы
        for fer in additive['Описание'].value_counts().index:
            # не считаем для шлакообразующих
            if ferro[ferro['Описание'] == fer]['Шлакообразующий'].values[0] == 1:
                continue
            # не считаем если содержание элемента в материале низкое
            if ferro[ferro['Описание'] == fer][el].values[0] < 10:
                continue
            # не считаем если элемент значительно содержиться в другом материале
            if __auxiliary_function(additive, fer, el, ferro) == True:
                continue
            # находим массу добавляемого материала
            m = sum(additive[additive['Описание'] == fer]['Масса'])
            # Рассчитываем коэффицент усвоения
            X1 = data_him.loc[flag-2, 'VAL'+el.upper()]
            X2 = data_him.loc[flag-1, 'VAL'+el.upper()]
            X = ferro[ferro['Описание'] == fer][el].values[0]
            Y = (X2-X1)*weight*100/(m*X)

            # не сохраняем если усвоение сильно отличаеться от табличного
            Y_coef = assimilation[assimilation['Описание'] == fer][el].values[0]
            if abs(Y-Y_coef) > Y*0.2:
                continue
            df.loc[df['Описание'] == fer, el] = Y
            break
    df.to_excel(dir+'files/assimilation_add.xlsx')


