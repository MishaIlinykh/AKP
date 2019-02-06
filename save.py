import pandas as pd
import numpy as np
import os, stat
#-----------------------------------------------------------------------------------------------------------------------
def save_for_verification(data, data_him):
    direct = 'C:/Users/Anastasiya.Mittseva/Desktop/AKP/new2_exp/save/' + data.loc[0, 'Номер плавки']
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
def save_for_analysis(data_object, data_him):
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

    dir = 'C:/Users/Anastasiya.Mittseva/Desktop/AKP/new2/save/save_for_analysis.xlsx'
    try:
        df = pd.read_excel(dir)
        # for i in set(df.columns).difference(df_save.columns):
        #     df_save[i] = 0
        # for i in set(df_save.columns).difference(df.columns):
        #     df[i] = 0
        # df_save = df_save[df.columns]
        df = pd.concat([df, df_save])
        df.to_excel(dir)

    except FileNotFoundError:
        df_save.to_excel(dir)
#-----------------------------------------------------------------------------------------------------------------------