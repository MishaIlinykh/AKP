import pandas as pd
import numpy as np
import datetime
import os
#--------------------------------------------------------------------------
from typing import Any

"""
Инициализация до бесконечного цикла
gT = DuctTape()
В теле цикла
framePlot = ToJS()
модель
framePlot.setLine(df)
температура
framePlot.setTemp(tempD)
химический анализ
framePlot.setPoint(pointD)
добавки
framePlot.setAdditive(addD)
устанавливаем время для номера плавки (по условию)
gT.setTime(datetime.datetime.strptime('2018-12-10 09:57:11', '%Y-%m-%d %H:%M:%S'),df['Номер плавки'][0])
Запрашиваем время по номеру плавки
timeP = gT.getTime(df['Номер плавки'][0])
Если плавка новая, то 1900-01-01 00:00:00
if timeP != datetime.datetime.strptime('1900-01-01 00:00:00', '%Y-%m-%d %H:%M:%S'):
    framePlot.setTime(timeP)
Сохраняем данные перед следующей итерацией
framePlot.saveJS()
"""
#--------------------------------------------------------------------------
class ToJS():
    steelM = pd.DataFrame()
    scY = pd.DataFrame()  # масштаб по Y
    canvasWidth = 525
    steel = ''
    codeSteel = ''
    numPl = ''
    label = []
    limitValues = {}
    scaleValues = {}
    targetValues = {}
    liquidus = 1538
    dataSource = pd.DataFrame()
    dataPoint = pd.DataFrame()
    dataTemp = pd.DataFrame()
    dataAdditive = pd.DataFrame()
    ds_compute = pd.DataFrame()

    startPicTime = -1
    # список отображаемых элементов
    #columnPlot = ['TEMP', 'C', 'SI', 'MN', 'P', 'S', 'AL', 'ALS', 'CU', 'CR', 'MO', 'NI', 'V', 'TI', 'NB', 'CA', 'CO',
    #              'PB', 'W', 'CE', 'B', 'AS', 'SN', 'BI', 'ZR', 'O', 'N']
    columnPlot = ['TEMP','C','SI','MN','P','S','AL','CU','CR','MO','NI','V','TI','NB','CA','CO','W','B','AS','SN','N','Cэ']
    # Тликв=1538-(80∙С+5∙Mn+11∙Si+30∙P+30∙S+1,5∙Cr+4∙Ni+3∙Mo++15∙Ti+15∙Nb+5∙Cu+50∙N+0,8∙Co+W+2∙V)

    liqEl = {'C':80,'SI':11,'MN':5,'P':30,'S':30,'AL':0,'ALS':0,'CU':5,'CR':1.5,'MO':3,'NI':4,'V':2,'TI':15,'NB':15,'CA':0,'CO':0.8,'PB':0,'W':1,'CE':0,'B':0,'AS':0,'SN':0,'BI':0,'ZR':0,'O':0,'N':50,'Cэ':0}

    nowTimeL = []

    # ------------------------------------------------
    def __init__(self):
        #C: / Users / Anastasiya.Mittseva / Desktop / AKP / new2 / libraries /
        self.config = pd.read_csv(r'config.dat', sep ='=')
        self.config['Описание'] = pd.core.strings.str_strip(self.config['Описание'])
        self.config['Значение'] = pd.core.strings.str_strip(self.config['Значение'])

        self.steelM = pd.read_excel(
        self.config[self.config['Описание'] == 'Путь к файлу с кодами марок стали']['Значение'].values[0])
        self.steelM = self.steelM.fillna(-1)

    # -------------------------------------------------------
    def setColumnPlot(self, columnPlot):
        self.columnPlot = columnPlot

    # -------------------------------------------------------
    def setSteel(self, steel, numPl, codeSteel):
        avgMin = [0.2, 0.3, 0.4, 0, 0, 0, -1, 0, 0, 0, 0, 0, 0, 0, -1, -1, -1, -1, -1, -1, 0, -1, -1, -1, 0, 0]
        avgMax = [0.3, 0.4, 0.5, 0.008, 0.004, 0.01, -1, 0.15, 0.1, 0.02, 0.12, 0.01, 0.01, -1, -1, -1, -1, -1, -1, -1,
                  0.008, -1, -1, -1, -1, 0.008]
        if numPl != self.numPl:
            self.numPl = numPl
            self.steel = steel
            self.codeSteel = codeSteel
            # tmp = self.steelM[self.steelM['Сталь']==self.steel]
            tmp = self.steelM[self.steelM['Код'].astype('str') == str(self.codeSteel)]

            self.scY['Элемент'] = pd.Series(self.columnPlot)
            scale = []
            y0 = []
            for i in range(self.scY.shape[0]):
                if self.scY['Элемент'][i] in list(tmp['Элемент']):
                    ttmp = tmp[tmp['Элемент'] == self.scY['Элемент'][i]]
                    ttmp.reset_index(inplace=True, drop=True)

                    tmpMin = ttmp['min'][0]
                    tmpMax = ttmp['max'][0]
                else:
                    tmpMin = -1
                    tmpMax = -1
                """if tmpMax != tmpMin:
                    tmpScY = (400 - 40) / (tmpMax - tmpMin)
                else:
                    tmpScY = 1
                if tmpMin >= 0:
                    tmpY0 = (100 + 400 - 20) + (tmpMin * tmpScY)
                else:
                    tmpY0 = (100 + 400 - 20)"""
                if tmpMax >= 0 and tmpMin >= 0 and tmpMax != tmpMin:
                    tmpScY = (400 - 40) / (tmpMax - tmpMin)
                    tmpY0 = (100 + 400 - 20) + (tmpMin * tmpScY)
                elif tmpMax >= 0 and tmpMin < 0:
                    tmpScY = 1
                    tmpY0 = (100 + 20) + tmpMax
                elif tmpMax < 0 and tmpMin >= 0:
                    tmpScY = 1
                    tmpY0 = (100 + 400 - 20) + tmpMin
                elif tmpMax < 0 and tmpMin < 0:
                    tmpScY = 1
                    tmpY0 = (100 + 400 - 20)
                else:
                    tmpScY = 1
                    tmpY0 = (100 + 400 - 20)

                scale.append(tmpScY)
                y0.append(tmpY0)

                self.limitValues[str(self.scY['Элемент'][i])] = [tmpMin, tmpMax]
                tmpMin_ = tmpMin
                tmpMax_ = tmpMax
                """if tmpMin < 0 and tmpMax < 0 and i > 0:
                    tmpMin_ = avgMin[i - 1]
                    tmpMax_ = avgMax[i - 1]"""

                self.scaleValues[str(self.scY['Элемент'][i])] = [tmpMin, tmpMax, tmpMin_, tmpMax_]

            self.scY['scale'] = pd.Series(scale)
            self.scY['y0'] = pd.Series(y0)
            targetCol = self.columnPlot.copy()
            targetCol.remove('TEMP')

            self.liquidus = 1538
            for j in targetCol:
                ttmp = tmp[tmp['Элемент'] == j]

                ttmp.reset_index(inplace=True, drop=True)
                if ttmp.shape[0] > 0:
                    tmpTarg = ttmp['Цель'][0]
                else:
                    tmpTarg = -1
                self.targetValues[j] = tmpTarg
                if tmpTarg > 0:
                    self.liquidus -= tmpTarg * self.liqEl[j]
            self.liquidus = int(np.around(self.liquidus, decimals=0))

            """if self.dataPoint.shape[0] > 0:
                targetCol = self.columnPlot.copy()
                targetCol.remove('TEMP')
                df = self.dataPoint.copy()

                self.liquidus = 1538
                for j in targetCol:
                    ttmp = df[j][df.shape[0] - 1]
                    if ttmp > 0:
                        tmpTarg = ttmp
                    else:
                        tmpTarg = -1

                    if tmpTarg > 0:
                        self.liquidus -= tmpTarg * self.liqEl[j]
                self.liquidus = int(np.around(self.liquidus, decimals=0))
            print('liqS=', self.liquidus)"""

    # -------------------------------------------------------
    def prepareData(self, tdf):
        df = tdf.copy()
        df['Продолжительность'] = df['Время'] - df['Время начала плавки']
        df['t, сек.'] = df['Продолжительность'].astype(pd.Timedelta).apply(lambda l: l.seconds)
        df['Cэ'] = df['C'] + (df['MN']/6) + ((df['CR']+df['MO']+df['V'])/5) + ((df['NI']+df['CU'])/15)
        df.reset_index(inplace=True, drop=True)
        # print(df['Марка стали'][0])
        self.setSteel(df['Марка стали'][0], df['Номер плавки'][0], df['Код марки стали'][0])

        return df

    # -------------------------------------------------------
    def preparePoint(self, tdf):
        df = tdf.copy()
        df.columns = ['Марка стали', 'Время', 'm',
                      'C', 'SI', 'MN', 'P', 'S', 'AL', 'ALS', 'CU',
                      'CR', 'MO', 'NI', 'V', 'TI', 'NB', 'CA', 'CO', 'PB', 'W',
                      'CE', 'B', 'AS', 'SN', 'BI', 'ZR', 'O', 'N', 'Время начала плавки']
        df['Продолжительность'] = df['Время'] - df['Время начала плавки']
        df['t, сек.'] = df['Продолжительность'].astype(pd.Timedelta).apply(lambda l: l.seconds)
        df['Cэ'] = df['C'] + (df['MN']/6) + ((df['CR']+df['MO']+df['V'])/5) + ((df['NI']+df['CU'])/15)
        df.reset_index(inplace=True, drop=True)

        """targetCol = self.columnPlot.copy()
        targetCol.remove('TEMP')

        if df.shape[0] > 0:
            self.liquidus = 1538
            for j in targetCol:
                ttmp = df[j][df.shape[0] - 1]
                if ttmp > 0:
                    tmpTarg = ttmp
                else:
                    tmpTarg = -1

                if tmpTarg > 0:
                    self.liquidus -= tmpTarg * self.liqEl[j]
            self.liquidus = int(np.around(self.liquidus, decimals=0))
        print('liq=',self.liquidus)"""

        return df

    # -------------------------------------------------------
    def prepareTemp(self, tdf):
        df = tdf.copy()
        df['Продолжительность'] = df['Время замера температуры'] - df['Время начала плавки']
        df['t, сек.'] = df['Продолжительность'].astype(pd.Timedelta).apply(lambda l: l.seconds)
        df.reset_index(inplace=True, drop=True)
        # print(df)
        return df

    # -------------------------------------------------------
    def saveJS(self):
        df = self.dataSource
        df_compute = self.ds_compute
        #um = {'TEMP': '', 'C': '%', 'SI': '%', 'MN': '%', 'P': '%', 'S': '%', 'AL': '%', 'ALS': '%', 'CU': '%',
        #      'CR': '%',
        #      'MO': '%', 'NI': '%', 'V': '%', 'TI': '%', 'NB': '%', 'CA': '%', 'CO': '%', 'PB': '%', 'W': '', 'CE': '%',
        #      'B': '%', 'AS': '%', 'SN': '%', 'BI': '%', 'ZR': '%', 'O': '%', 'N': '%'}
        um = {'TEMP':'', 'C':'%','SI':'%','MN':'%','P':'%','S':'%','AL':'%','CU':'%','CR':'%',
              'MO':'%','NI':'%','V':'%','TI':'%','NB':'%','CA':'%','CO':'%','W':'%',
              'B':'%','AS':'%','SN':'%','N':'%','Cэ':'%'}
        lineStrX = []
        lineStrY = []
        lineStrX_c = []
        lineStrY_c = []
        header = self.columnPlot
        scX = 1  # 2.5
        num = df.shape[0]
        num_c = df_compute.shape[0]
        boxElement = []
        boxElement_c = []

        pointX = []
        pointY = []
        pointXr = []
        pointYr = []

        tempX = []
        tempY = []
        tempYreal = []
        tempXreal = []
        # ---пересчет масштаба--------
        if num > 0:
            for j in header:
                ts = self.scaleValues[j]
                if ts[0] < 0:
                    if ts[2] < 0:
                        ts[2] = df[j][0]
                    if df[j][num - 1] < ts[2]:
                        ts[2] = df[j][num - 1]
                if ts[1] < 0:
                    if ts[3] < 0:
                        ts[3] = df[j][0]
                    if df[j][num - 1] > ts[3]:
                        ts[3] = df[j][num - 1]
                # проверка на отрицательный масштаб (значение больше максимума, а минимума нет)
                if ts[2] > ts[3]:
                    if ts[0] < 0:
                        ts[2] = 0  # ts[3]

                self.scaleValues[j] = ts

                """if ts[3] != ts[2]:
                    tScY = (400 - 40) / (ts[3] - ts[2])
                else:
                    tScY = 1
                if ts[3] >= 0:
                    tY0 = (100 + 400 - 20) + (ts[2] * tScY)
                else:
                    tY0 = (100 + 400 - 20)"""

                if ts[3] >= 0 and ts[2] >= 0 and ts[3] != ts[2]:
                    tScY = (400 - 40) / (ts[3] - ts[2])
                    tY0 = (100 + 400 - 20) + (ts[2] * tScY)
                elif ts[3] >= 0 and ts[2] < 0:
                    tScY = (400 - 40)/10
                    tY0 = (100 + 20) + ts[3]
                elif ts[3] < 0 and ts[2] >= 0:
                    tScY = (400 - 40)/10
                    tY0 = (100 + 400 - 20) + ts[2]
                elif ts[3] < 0 and ts[2] < 0:
                    tScY = (400 - 40)/10
                    tY0 = (100 + 400 - 20)
                else:
                    tScY = (400 - 40)/10
                    tY0 = (100 + 400 - 20)

                ind = self.scY[self.scY['Элемент'] == j].index[0]

                self.scY.iloc[ind, 1] = tScY
                self.scY.iloc[ind, 2] = tY0
        # ---------------------------------------------
        if num_c > 0:
            for j in header:
                ts = self.scaleValues[j]
                if ts[0] < 0:
                    # print('ts: ',ts)
                    # print('df_compute: ',df_compute)
                    if ts[2] < 0:
                        ts[2] = df_compute[j][0]
                    if df_compute[j][num_c - 1] < ts[2]:
                        ts[2] = df_compute[j][num_c - 1]
                if ts[1] < 0:
                    if ts[3] < 0:
                        ts[3] = df_compute[j][0]
                    if df_compute[j][num_c - 1] > ts[3]:
                        ts[3] = df_compute[j][num_c - 1]
                self.scaleValues[j] = ts

                """if ts[3] != ts[2]:
                    tScY = (400 - 40) / (ts[3] - ts[2])
                else:
                    tScY = 1
                if ts[3] >= 0:
                    tY0 = (100 + 400 - 20) + (ts[2] * tScY)
                else:
                    tY0 = (100 + 400 - 20)"""

                if ts[3] >= 0 and ts[2] >= 0 and ts[3] != ts[2]:
                    tScY = (400 - 40) / (ts[3] - ts[2])
                    tY0 = (100 + 400 - 20) + (ts[2] * tScY)
                elif ts[3] >= 0 and ts[2] < 0:
                    tScY = (400 - 40)/10
                    tY0 = (100 + 20) + ts[3]
                elif ts[3] < 0 and ts[2] >= 0:
                    tScY = (400 - 40)/10
                    tY0 = (100 + 400 - 20) + ts[2]
                elif ts[3] < 0 and ts[2] < 0:
                    tScY = (400 - 40)/10
                    tY0 = (100 + 400 - 20)
                else:
                    tScY = (400 - 40)/10
                    tY0 = (100 + 400 - 20)

                ind = self.scY[self.scY['Элемент'] == j].index[0]

                self.scY.iloc[ind, 1] = tScY
                self.scY.iloc[ind, 2] = tY0
        # -----температура по точкам-------------------
        if self.dataTemp.shape[0] > 0:
            ts = self.scaleValues['TEMP']
            for i in range(self.dataTemp.shape[0]):
                y = self.dataTemp['TEMP'][i]
                if y < 3000:
                    if y < ts[2]:
                        ts[2] = y
                    if y > ts[3]:
                        ts[3] = y
                    self.scaleValues['TEMP'] = ts
                    if ts[3] != ts[2]:
                        tScY = (400 - 60) / (ts[3] - ts[2])
                    else:
                        tScY = 1
                    if ts[3] >= 0:
                        tY0 = (100 + 400 - 20) + (ts[2] * tScY)
                    else:
                        tY0 = (100 + 400 - 20)
            ind = self.scY[self.scY['Элемент'] == 'TEMP'].index[0]
            self.scY.iloc[ind, 1] = tScY
            self.scY.iloc[ind, 2] = tY0
        # ----------------------------

        if num > 0:
            x = df['t, сек.'][0]
            lineStrX.append('[' + str(int(np.around(x * scX, decimals=0))))

            timeTmp = str(df['Время'][0])
            k = timeTmp.rfind('.')
            if k > 0:
                timeTmp = timeTmp[:k]

            lineStrX.append('["' + timeTmp + '"')

            timeTmp = str(df['Продолжительность'][0])[7:]
            k = timeTmp.rfind('.')
            if k > 0:
                timeTmp = timeTmp[:k]

            lineStrX.append('["' + timeTmp + '"')

            for j in header:
                tmp = self.scY[self.scY['Элемент'] == j]
                tmp.reset_index(inplace=True, drop=True)
                C0 = tmp['y0'][0]
                scC = tmp['scale'][0]

                y = df[j][0]
                lineStrY.append('[' + str(int(np.around(C0 + (-y * scC), decimals=0))))
                if j == 'TEMP':
                    tarTmp = '-1'
                else:
                    tarTmp = str(self.targetValues[j])
                boxElement.append('["'+um[j]+'",'+str(np.around(y,decimals=4))+','+str(self.limitValues[j][0])+','+str(self.limitValues[j][1])+',0,'+tarTmp+']')
            if num > 1:
                for i in range(1, num):
                    x = df['t, сек.'][i]
                    lineStrX[0] = lineStrX[0] + ',' + str(int(np.around(x * scX, decimals=0)))
                    timeTmp = str(df['Время'][i])
                    k = timeTmp.rfind('.')
                    if k > 0:
                        timeTmp = timeTmp[:k]
                    # print(df['Время'][i], str(df['Время'][i]), timeTmp)
                    lineStrX[1] = lineStrX[1] + ',"' + timeTmp + '"'

                    timeTmp = str(df['Продолжительность'][i])[7:]
                    k = timeTmp.rfind('.')
                    if k > 0:
                        timeTmp = timeTmp[:k]
                    lineStrX[2] = lineStrX[2] + ',"' + timeTmp + '"'

                    k = 0
                    for j in header:
                        tmp = self.scY[self.scY['Элемент'] == j]
                        tmp.reset_index(inplace=True, drop=True)
                        C0 = tmp['y0'][0]
                        scC = tmp['scale'][0]
                        y = df[j][i]
                        lineStrY[k] = lineStrY[k] + ',' + str(int(np.around(C0 + (-y * scC), decimals=0)))

                        warningColor = '0'

                        if y < self.limitValues[j][0] and self.limitValues[j][0] >= 0:
                            warningColor = '1'
                        elif y > self.limitValues[j][1] and self.limitValues[j][1] >= 0:
                            warningColor = '1'
                        if j == 'TEMP':
                            tarTmp = '-1'
                        else:
                            tarTmp = str(self.targetValues[j])
                        boxElement[k] = ('["'+um[j]+'",'+str(np.around(y,decimals=4))+','+str(self.limitValues[j][0])+','+str(self.limitValues[j][1])+','+warningColor+','+tarTmp+']')
                        k = k + 1

        # ----------------------------

        if num_c > 0:
            x = df_compute['t, сек.'][0]
            lineStrX_c.append('[' + str(int(np.around(x * scX, decimals=0))))

            timeTmp = str(df_compute['Время'][0])
            k = timeTmp.rfind('.')
            if k > 0:
                timeTmp = timeTmp[:k]

            lineStrX_c.append('["' + timeTmp + '"')

            timeTmp = str(df_compute['Продолжительность'][0])[7:]
            k = timeTmp.rfind('.')
            if k > 0:
                timeTmp = timeTmp[:k]

            lineStrX_c.append('["' + timeTmp + '"')

            for j in header:
                tmp = self.scY[self.scY['Элемент'] == j]
                tmp.reset_index(inplace=True, drop=True)
                C0 = tmp['y0'][0]
                scC = tmp['scale'][0]

                y = df_compute[j][0]
                lineStrY_c.append('[' + str(int(np.around(C0 + (-y * scC), decimals=0))))
                if j == 'TEMP':
                    tarTmp = '-1'
                else:
                    tarTmp = str(self.targetValues[j])
                boxElement_c.append('["'+um[j]+'",'+str(np.around(y,decimals=4))+','+str(self.limitValues[j][0])+','+str(self.limitValues[j][1])+',0,'+tarTmp+']')
            if num_c > 1:
                for i in range(1, num_c):
                    x = df_compute['t, сек.'][i]
                    lineStrX_c[0] = lineStrX_c[0] + ',' + str(int(np.around(x * scX, decimals=0)))
                    timeTmp = str(df_compute['Время'][i])
                    k = timeTmp.rfind('.')
                    if k > 0:
                        timeTmp = timeTmp[:k]
                    lineStrX_c[1] = lineStrX_c[1] + ',"' + timeTmp + '"'

                    timeTmp = str(df_compute['Продолжительность'][i])[7:]
                    k = timeTmp.rfind('.')
                    if k > 0:
                        timeTmp = timeTmp[:k]
                    lineStrX_c[2] = lineStrX_c[2] + ',"' + timeTmp + '"'

                    k = 0
                    for j in header:
                        tmp = self.scY[self.scY['Элемент'] == j]
                        tmp.reset_index(inplace=True, drop=True)
                        C0 = tmp['y0'][0]
                        scC = tmp['scale'][0]
                        y = df_compute[j][i]
                        lineStrY_c[k] = lineStrY_c[k] + ',' + str(int(np.around(C0 + (-y * scC), decimals=0)))

                        warningColor = '0'

                        if y < self.limitValues[j][0] and self.limitValues[j][0] >= 0:
                            warningColor = '1'
                        elif y > self.limitValues[j][1] and self.limitValues[j][1] >= 0:
                            warningColor = '1'
                        if j == 'TEMP':
                            tarTmp = '-1'
                        else:
                            tarTmp = str(self.targetValues[j])
                        boxElement_c[k] = ('["'+um[j]+'",'+str(np.around(y,decimals=4))+','+str(self.limitValues[j][0])+','+str(self.limitValues[j][1])+','+warningColor+','+tarTmp+']')
                        k = k + 1
        # ----точки------------
        if self.dataPoint.shape[0] > 0:
            for j in header:
                if j != 'TEMP':
                    tmp = self.scY[self.scY['Элемент'] == j]
                    tmp.reset_index(inplace=True, drop=True)
                    C0 = tmp['y0'][0]
                    scC = tmp['scale'][0]
                    y = self.dataPoint[j][0]
                    pointY.append('[' + str(int(np.around(C0 + (-y * scC), decimals=0))))
                    pointYr.append('['+ str(np.around(y, decimals=4)))#str(y))

            for i in range(self.dataPoint.shape[0]):
                x = self.dataPoint['t, сек.'][i]
                pointX.append(str(int(np.around(x * scX, decimals=0))))

                x = self.dataPoint['Время'][i]
                timeTmp = str(x)
                k = timeTmp.rfind('.')
                if k > 0:
                    timeTmp = timeTmp[:k]
                pointXr.append(str(timeTmp))

                k = 0
                for j in header:
                    if j != 'TEMP' and i > 0:
                        tmp = self.scY[self.scY['Элемент'] == j]
                        tmp.reset_index(inplace=True, drop=True)
                        C0 = tmp['y0'][0]
                        scC = tmp['scale'][0]
                        y = self.dataPoint[j][i]
                        pointY[k] = pointY[k] + ',' + str(int(np.around(C0 + (-y * scC), decimals=0)))
                        pointYr[k] = pointYr[k] + ',' + str(np.around(y, decimals=4))#str(y)
                        k = k + 1
        # -------температура------------
        if self.dataTemp.shape[0] > 0:
            tmp = self.scY[self.scY['Элемент'] == 'TEMP']
            tmp.reset_index(inplace=True, drop=True)
            C0 = tmp['y0'][0]
            scC = tmp['scale'][0]

            for i in range(self.dataTemp.shape[0]):
                y = self.dataTemp['TEMP'][i]
                if y < 3000:
                    tempY.append(str(int(np.around(C0 + (-y * scC), decimals=0))))
                    x = self.dataTemp['t, сек.'][i]
                    tempX.append(str(int(np.around(x * scX, decimals=0))))
                    tempYreal.append(str(int(np.around(y, decimals=0))))
                    x = self.dataTemp['Время замера температуры'][i]
                    timeTmp = str(x)
                    k = timeTmp.rfind('.')
                    if k > 0:
                        timeTmp = timeTmp[:k]
                    tempXreal.append(str(timeTmp))

        # -----запись---------
        # ----liquidus-------------------------------------------
        if self.dataPoint.shape[0] > 0:
            tCol = self.columnPlot.copy()
            tCol.remove('TEMP')
            self.liquidus = 1538

            for j in tCol:
                ttmp = self.dataPoint[j][self.dataPoint.shape[0] - 1]
                if ttmp > 0:
                    tmpT = ttmp
                else:
                    tmpT = -1
                if tmpT > 0:
                    self.liquidus -= tmpT * self.liqEl[j]
                self.liquidus = int(np.around(self.liquidus, decimals=0))
            #print(self.liquidus)
        # --------------------------------------------------------
        if df.shape[0] > 0:
            timeTmp = str(df['Время начала плавки'][0])
        elif df_compute.shape[0] > 0:
            timeTmp = str(df_compute['Время начала плавки'][0])
        else:
            timeTmp = 'unknown'
        k = timeTmp.rfind('.')
        if k > 0:
            timeTmp = timeTmp[:k]
        if df.shape[0] > 0:
            tmpStr = 'var steelData = ["' + str(df['Марка стали'][0]) + '","' + df['Номер плавки'][
                0] + '","' + timeTmp + '",' + str(self.liquidus) + '];\n'
        elif df_compute.shape[0] > 0:
            tmpStr = 'var steelData = ["' + str(df_compute['Марка стали'][0]) + '","' + df_compute['Номер плавки'][
                0] + '","' + timeTmp + '",' + str(self.liquidus) + '];\n'
        else:
            tmpStr = 'unknown'

        tmpStr = tmpStr + 'var localData = ['
        if num > 0:
            tmpStr = tmpStr + boxElement[0]
        for j in range(1, len(boxElement)):
            tmpStr = tmpStr + ',' + boxElement[j]
        tmpStr = tmpStr + '];\n'

        tmpStr = tmpStr + 'var localDataC = ['
        if num_c > 0:
            tmpStr = tmpStr + boxElement_c[0]
        for j in range(1, len(boxElement_c)):
            tmpStr = tmpStr + ',' + boxElement_c[j]
        tmpStr = tmpStr + '];\n'

        tmpStr = tmpStr + 'var plotTime = ['
        if num > 0:
            lineStrX[0] = lineStrX[0] + ']'
            lineStrX[1] = lineStrX[1] + ']'
            lineStrX[2] = lineStrX[2] + ']'
            tmpStr = tmpStr + '\n' + lineStrX[0]

            tmpStr = tmpStr + ',\n' + lineStrX[1]
            tmpStr = tmpStr + ',\n' + lineStrX[2] + '\n'
        tmpStr = tmpStr + '];\n'

        tmpStr = tmpStr + 'var plotTimeC = ['
        if num_c > 0:
            lineStrX_c[0] = lineStrX_c[0] + ']'
            lineStrX_c[1] = lineStrX_c[1] + ']'
            lineStrX_c[2] = lineStrX_c[2] + ']'
            tmpStr = tmpStr + '\n' + lineStrX_c[0]

            tmpStr = tmpStr + ',\n' + lineStrX_c[1]
            tmpStr = tmpStr + ',\n' + lineStrX_c[2] + '\n'
        tmpStr = tmpStr + '];\n'

        tmpStr = tmpStr + 'var plotLine = ['
        if num > 0:
            lineStrY[0] = lineStrY[0] + ']'
            tmpStr = tmpStr + '\n' + lineStrY[0]
            for j in range(1, len(lineStrY)):
                lineStrY[j] = lineStrY[j] + ']'
                tmpStr = tmpStr + ',\n' + lineStrY[j]
        tmpStr = tmpStr + '\n];'

        tmpStr = tmpStr + '\nvar plotLineC = ['
        if num_c > 0:
            lineStrY_c[0] = lineStrY_c[0] + ']'
            tmpStr = tmpStr + '\n' + lineStrY_c[0]
            for j in range(1, len(lineStrY_c)):
                lineStrY_c[j] = lineStrY_c[j] + ']'
                tmpStr = tmpStr + ',\n' + lineStrY_c[j]
        tmpStr = tmpStr + '\n];'

        tmpStr = tmpStr + '\nvar timePoint = ['
        if len(pointX) > 0:
            tmpStr = tmpStr + pointX[0]
            for i in range(1, len(pointX)):
                tmpStr = tmpStr + ',' + pointX[i]
        tmpStr = tmpStr + '];\n'
        tmpStr = tmpStr + 'var plotPoint = ['

        if len(pointX) > 0:
            pointY[0] = pointY[0] + ']'
            tmpStr = tmpStr + '\n' + pointY[0]
            for j in range(1, len(pointY)):
                pointY[j] = pointY[j] + ']'
                tmpStr = tmpStr + ',\n' + pointY[j]
        tmpStr = tmpStr + '\n];'

        tmpStr = tmpStr + '\nvar timePointR = ['
        if len(pointXr) > 0:
            tmpStr = tmpStr + '"' + pointXr[0] + '"'
            for i in range(1, len(pointXr)):
                tmpStr = tmpStr + ',"' + pointXr[i] + '"'
        tmpStr = tmpStr + '];\n'
        tmpStr = tmpStr + 'var plotPointR = ['

        if len(pointX) > 0:
            pointYr[0] = pointYr[0] + ']'
            tmpStr = tmpStr + '\n' + pointYr[0]
            for j in range(1, len(pointYr)):
                pointYr[j] = pointYr[j] + ']'
                tmpStr = tmpStr + ',\n' + pointYr[j]
        tmpStr = tmpStr + '\n];'

        tmpStr = tmpStr + '\nvar tempPoint = ['
        if len(tempX) > 0:
            tmpStr = tmpStr + '[' + tempX[0] + ',' + tempY[0] + ',' + tempYreal[0] + ',"' + tempXreal[0] + '"]'

            for i in range(1, len(tempX)):
                tmpStr = tmpStr + ',[' + tempX[i] + ',' + tempY[i] + ',' + tempYreal[i] + ',"' + tempXreal[i] + '"]'
        tmpStr = tmpStr + '];'
        # масштаб
        tmpStr = tmpStr + '\nvar scale = ['
        for j in header:
            tmp = self.scY[self.scY['Элемент'] == j]
            tmp.reset_index(inplace=True, drop=True)
            C0 = tmp['y0'][0]
            scC = tmp['scale'][0]
            tmpStr = tmpStr + '[' + str(scC) + ',' + str(C0) + ']'
            if j != 'Cэ':
                tmpStr = tmpStr + ','
        tmpStr = tmpStr + '];'

        tmpStr = tmpStr + '\nvar startTime = ' + str(int(np.around(self.startPicTime * scX, decimals=0))) + ';'

        tmpStr = tmpStr + '\nvar additive = ['
        if self.dataAdditive.shape[0] > 0:
            x = self.dataAdditive['Время добавки'][0]
            timeTmp = str(x)
            k = timeTmp.rfind('.')
            if k > 0:
                timeTmp = timeTmp[:k]
            tmpStr = tmpStr + '["' + str(self.dataAdditive['Код'][0]) + '","' + self.dataAdditive['Описание'][
                0] + '","' + str(timeTmp) + '",' + str(self.dataAdditive['Масса'][0]) + ']'
            for i in range(1, self.dataAdditive.shape[0]):
                x = self.dataAdditive['Время добавки'][i]
                timeTmp = str(x)
                k = timeTmp.rfind('.')
                if k > 0:
                    timeTmp = timeTmp[:k]
                tmpStr = tmpStr + ',["' + str(self.dataAdditive['Код'][i]) + '","' + self.dataAdditive['Описание'][
                    i] + '","' + str(timeTmp) + '",' + str(self.dataAdditive['Масса'][i]) + ']'
        tmpStr = tmpStr + '];'

        tmpStr = tmpStr + '\nvar nowTime = ["' + self.nowTimeL[1] + '","' + self.nowTimeL[2] + '"];'

        f = open(os.path.join(self.config[self.config['Описание'] == 'Путь к папке с сайтом']['Значение'].values[0],
                              'line.js'), 'w', encoding='utf-8')
        #f = open('web/line.js', 'w', encoding='utf-8')
        f.write(tmpStr)
        f.close()

        """f = open('steelman/line.js', 'w', encoding='utf-8')
        f.write(tmpStr)
        f.close()"""
    # -------------------------------------------------------
    def setLine(self, dataSource):
        self.dataSource = self.prepareData(dataSource)
        # self.saveJS()

    # -------------------------------------------------------
    def setLineC(self, dataSource):
        self.ds_compute = self.prepareData(dataSource)
        # self.saveJS()

    # -------------------------------------------------------
    def setPoint(self, dataPoint):
        self.dataPoint = self.preparePoint(dataPoint)

    # -------------------------------------------------------
    def setTemp(self, dataTemp=pd.DataFrame(
        {'Номер плавки': pd.Series(), 'Время замера температуры': pd.Series(), 'TEMP': pd.Series(),
         'Время начала плавки': pd.Series()})):
        self.dataTemp = self.prepareTemp(dataTemp)

    # -------------------------------------------------------
    def setAdditive(self, dataAdd=pd.DataFrame(
        {'Время добавки': pd.Series(), 'Код': pd.Series(), 'Описание': pd.Series(), 'Масса': pd.Series()})):
        self.dataAdditive = dataAdd.copy()

    # -------------------------------------------------------
    def setTime(self, picTime):
        if self.dataSource.shape[0] > 0:
            startP = self.dataSource['Время начала плавки'][0]
        elif self.ds_compute.shape[0] > 0:
            startP = self.ds_compute['Время начала плавки'][0]
        else:
            startP = picTime
        if picTime == picTime:
            self.startPicTime = (picTime - startP).seconds

    # -------------------------------------------------------
    def setNow(self, startTime, nowTime):
        self.nowTimeL = []
        x = startTime
        timeTmp = str(x)
        k = timeTmp.rfind('.')
        if k > 0:
            timeTmp = timeTmp[:k]
        self.nowTimeL.append(str(timeTmp))
        x = nowTime
        timeTmp = str(x)
        k = timeTmp.rfind('.')
        if k > 0:
            timeTmp = timeTmp[:k]
        self.nowTimeL.append(str(timeTmp))
        timeTmp = str(nowTime - startTime)[7:]
        k = timeTmp.rfind('.')
        if k > 0:
            timeTmp = timeTmp[:k]
        self.nowTimeL.append(timeTmp)
#-------------------------------------------------------------------------------------------------------
class DuctTape():
    #------------------------------------------------
    def __init__(self):
        self.timeP = datetime.datetime.strptime('1900-01-01 00:00:00', '%Y-%m-%d %H:%M:%S')
        self.meltingNumber = 'unknown'
    #-------------------------------------------------------
    def setTime(self,timePic,meltN):
        self.timeP = timePic
        self.meltingNumber = meltN
    #-------------------------------------------------------
    def getTime(self,meltN):
        if meltN != self.meltingNumber:
            self.timeP = datetime.datetime.strptime('1900-01-01 00:00:00', '%Y-%m-%d %H:%M:%S')
        return self.timeP
#------------------------------------------------------------------------------------------------------