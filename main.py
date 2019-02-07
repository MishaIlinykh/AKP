import pandas as pd
from datetime import datetime
pd.options.display.max_columns = 100
pd.options.display.max_rows = 100
import time
import sys

config = pd.read_csv(r'config.dat', sep='=')
config['Описание'] = pd.core.strings.str_strip(config['Описание'])
config['Значение'] = pd.core.strings.str_strip(config['Значение'])
dir = config[config['Описание'] == 'Путь к проекту']['Значение'].values[0]
sys.path.append(dir+'libraries')
from oz import ToJS, DuctTape
from sortFiles import getTwoLast, delUnnecessaryFiles, delVD
from AddingFromTelegrams import addMelting, addWeightEAL, addMeasurementChemistry, addMainInformation, addWeight
from models import add_models, predict, chemicalCalculation, predict_TEMP
from save import save_for_verification, save_for_analysis

def made_strings(name_dir, titles, mark, material, titles_for_temp, counter):
    all_params = pd.DataFrame(columns=titles)
    for i in titles[34:112:1]:
        all_params.loc[0, i] = 0

    him = pd.DataFrame(columns=titles[2:5:1] + titles[7:33:1] + ['Время начала плавки'])
    temperature = pd.DataFrame(columns=['Номер плавки', 'Время замера температуры', 'TEMP', 'Окисленность', 'Время начала плавки'])
    all_additive = pd.DataFrame(columns=['Время добавки', 'Код', 'Описание', 'Масса'])
    # удаляем файлы из папки VD
    # delVD(name_dir)

    all_params = addMelting(all_params, name_dir, mark, counter)
    all_params = addWeightEAL(all_params, name_dir, counter)
    all_params, flag = addMeasurementChemistry(all_params, name_dir, counter)
    all_params, all_params_chCals, temperature, all_additive, for_temp, flag_temp = addMainInformation(all_params, name_dir, counter, temperature, all_additive, material, titles_for_temp, flag)

    him.loc[0, 'Время начала плавки'] = all_params.loc[0, 'Время начала плавки']
    if flag > 0:
        for i in titles[2:5:1] + titles[7:33:1]:
            him.loc[0, i] = all_params.loc[0, i]

    return all_params, all_params_chCals, him, temperature, all_additive, for_temp, flag, flag_temp

# считываем модели и все необходимые файлы
models = add_models(dir)
mark = pd.read_excel(dir + 'files/mark.xlsx')
material = pd.read_excel(dir + 'files/material.xlsx')
mean_chemical = pd.read_excel(dir+'files/mean_xim.xlsx')
ferro = pd.read_excel(dir+'files/ferro.xlsx')
assimilation = pd.read_excel(dir+'files/assimilation.xlsx')
ferro = ferro.fillna(0)
assimilation = assimilation.fillna(100)

all_titils = ['Время', 'Номер плавки', 'Марка стали', 'Последний замер химии']
for i in models['titles']:
    all_titils.append(i)
all_titils.append('Время начала плавки')
all_titils.append('Код марки стали')

columns = ['Время', 'Номер плавки', 'Марка стали', 'TEMP', 'C', 'SI', 'MN', 'P', 'S', 'AL', 'ALS', 'CU', 'CR',
           'MO','NI', 'V', 'TI', 'NB', 'CA', 'CO', 'PB', 'W', 'CE', 'B', 'AS', 'SN', 'BI','ZR', 'O', 'N',
           'Время начала плавки', 'Код марки стали']

all_object = pd.DataFrame(columns=columns)
all_him = pd.DataFrame(columns=all_titils[2:5:1] + all_titils[7:33:1] + ['Время начала плавки'])
all_strings = pd.DataFrame(columns = all_titils)
melting = ' '
bool_temp = False
counter = 0
dir_name = config[config['Описание'] == 'Путь к телеграммам']['Значение'].values[0]

gT = DuctTape()

while (True):
    # one_object - одна строка, которая учасвует в предсказании
    # him - последний замеры химии
    # all_temp - все замеры температуры
    # all_additive - все добавляемые материалы
    one_object, one_object_chCals, him, all_temp, all_additive, for_temp, flag, flag_temp = made_strings(dir_name, all_titils, mark, material, models['titles_TEMP'], counter)
    counter += 1
    if counter > 10:
        counter  = 0

    if melting != one_object.loc[0, 'Номер плавки']:

        #сохраняем предыдущию плавку для проверки
        if all_strings.shape[0]!=0:
            save_for_verification(all_strings, all_him)
            all_strings = pd.DataFrame(columns=all_titils)

        #сохраняем предыдущую плаку для анализа
        if melting != ' ':
            save_for_analysis(all_object, all_him)

        #создаем новую плавку, обнуляем датафреймы
        melting = one_object.loc[0, 'Номер плавки']
        all_object = pd.DataFrame(columns=columns)
        all_object_chCalc = pd.DataFrame(columns=columns)
        all_him = pd.DataFrame(columns=all_titils[2:5:1] + all_titils[7:33:1] + ['Время начала плавки'])
        bool_temp = False

        #Находим массу металла
        weight = addWeight(dir_name, melting)

    all_strings = pd.concat([all_strings, one_object])
    all_strings.reset_index(inplace=True, drop=True)

    if one_object.loc[0, 'TEMP'] == None:
        one_object.loc[0, 'TEMP'] = mean_chemical[mean_chemical['Марка стали'] == temp.loc[0, 'Марка стали']]['TEMP'].values[0]

    if flag == 0:
        pred = pd.DataFrame(columns=columns)
        pred_chCalc = pd.DataFrame(columns=columns)

    else:
        pred = predict(models, one_object, columns, all_titils)
        pred_chCalc = chemicalCalculation(one_object_chCals, weight, columns, ferro, assimilation)
    if flag_temp > 0:
        pred = predict_TEMP(models, pred, for_temp)
    # для отрисовки граффиков пока нет замеров химии
    if flag == 0:
        for i in columns[0:3] + columns[30:32]:
            pred.loc[0, i] = one_object.loc[0, i]
        for i in columns[4:30]:
            if mean_chemical[mean_chemical['Марка стали'] == pred.loc[0, 'Марка стали']].shape[0] != 0:
                pred.loc[0, i] = mean_chemical[mean_chemical['Марка стали'] == pred.loc[0, 'Марка стали']]['VAL' + i].values[0]
            else:
                pred.loc[0, i] = mean_chemical[mean_chemical['Марка стали'] == 'all_mean']['VAL' + i].values[0]
        if flag_temp==0:
            pred.loc[0, 'TEMP'] = -1

    all_object = pd.concat([all_object, pred])
    all_object['TEMP'] = all_object['TEMP'].astype(int)
    all_object.reset_index(inplace=True, drop=True)
    all_object_chCalc = pd.concat([all_object_chCalc, pred_chCalc])
    all_object_chCalc.reset_index(inplace=True, drop=True)

    if flag > 0:
        all_him = pd.concat([all_him, him])
        all_him = all_him.drop_duplicates()
        all_him.reset_index(inplace=True, drop=True)

    graph = ToJS()
    graph.setNow(one_object.loc[0, 'Время начала плавки'], one_object.loc[0, 'Время'])
    if flag > 0:
        graph.setPoint(all_him)

    if all_temp.shape[0] > 0:
        all_temp['TEMP'] = all_temp['TEMP'].astype(int)
        graph.setTemp(all_temp)

    graph.setLine(all_object)
    all_object_chCalc = all_object_chCalc.fillna(-1)
    if all_object_chCalc.shape[0] > 0:
        all_object_chCalc['TEMP'] = all_object_chCalc['TEMP'].astype(int)
        graph.setLineC(all_object_chCalc)

    if (bool_temp == False) and (flag > 0):
        time_start_him = datetime.now()
        gT.setTime(time_start_him, melting)
        bool_temp = True

    graph.setAdditive(all_additive)
    timeP = gT.getTime(melting)
    if timeP != datetime.strptime('1900-01-01 00:00:00', '%Y-%m-%d %H:%M:%S'):
        graph.setTime(timeP)
    graph.saveJS()

    time.sleep(10)