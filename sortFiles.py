import os
import time
import datetime
import pandas as pd
#-----------------------------------------------------------------------------------------------------------------------
def __getFileDate(file):
    if os.path.exists(file):
        st = os.stat(file)
        tim = time.localtime(st.st_ctime)
        dt =datetime.datetime(tim.tm_year,tim.tm_mon,tim.tm_mday,tim.tm_hour,tim.tm_min,tim.tm_sec)
    else:
        dt = None
    return dt
#-----------------------------------------------------------------------------------------------------------------------
def __getFileSize(file):
    if os.path.exists(file):
        st = os.stat(file)
        ret = st.st_size
    else:
        ret = None
    return ret
#-----------------------------------------------------------------------------------------------------------------------
def __getListDir(dirPath):
    ret = []
    dirL = []
    if os.path.exists(dirPath):
        ret = os.listdir(dirPath)
        for f in ret:
            if os.path.isfile(os.path.join(dirPath,f)) == False:
                dirL.append(f)
        for f in dirL:
            try:
                ret.remove(f)
            except ValueError:
                pass
    return ret
#-----------------------------------------------------------------------------------------------------------------------
def getListDirAsc(dirPath):
    l = []
    if os.path.exists(dirPath):
        l = __getListDir(dirPath)
        l.sort(key=lambda date:__getFileDate(os.path.join(dirPath,date)))
    return l
#-----------------------------------------------------------------------------------------------------------------------
def getListDirDesc(dirPath):
    l = []
    if os.path.exists(dirPath):
        l = __getListDir(dirPath)
        l.sort(reverse=True,key=lambda date:__getFileDate(os.path.join(dirPath,date)))
    if len(l) > 0:
        try:
            l.pop(0)
            if len(l) > 0:
                l.pop(0)
        except Exception:
            pass
    return l
#-----------------------------------------------------------------------------------------------------------------------
def getTwoLast(dirPath):
    while True:
        try:
            l = []
            r1 = None
            r2 = None
            lin1 = ""
            if os.path.exists(dirPath):
                l = getListDirDesc(dirPath)
                dir0 = []
                for f in l:
                    if __getFileSize(os.path.join(dirPath,f)) == 0:
                        dir0.append(f)
                for f in dir0:
                    try:
                        l.remove(f)
                    except ValueError:
                        pass

                if len(l)>0:
                    r1 = l[0]
                    while True:
                            file = open(os.path.join(dirPath,r1), 'r' )
                            lin1 = file.readline()
                            file.close()
                            break
                        # try:
                        #     file = open(os.path.join(dirPath,r1), 'r' )
                        #     lin1 = file.readline()
                        #     file.close()
                        #     break
                        # except Exception:
                        #     pass
                    l.remove(r1)

                if len(l)>0:
                    for f in l:
                        while True:
                            file = open(os.path.join(dirPath, f), 'r')
                            linTmp = file.readline()
                            file.close()
                            break
                            # try:
                            #     file = open(os.path.join(dirPath,f), 'r' )
                            #     linTmp = file.readline()
                            #     file.close()
                            #     break
                            # except Exception:
                            #     pass
                        if lin1 != linTmp:
                            r2 = f
                            break
            break
        except Exception:
            r1, r2 = getTwoLast(dirPath)
    return r1,r2
#-----------------------------------------------------------------------------------------------------------------------
def delUnnecessaryFiles(dirPath):
    if os.path.exists(dirPath):
        l = getListDirDesc(dirPath)
        f1,f2 = getTwoLast(dirPath)
        if f1 == f1:
            try:
                l.remove(f1)
            except ValueError:
                pass            
        if f2 == f2:
            try:
                l.remove(f2)
            except ValueError:
                pass
        for f in l:
            try:
                os.remove(os.path.join(dirPath,f))
            except Exception:
                pass
#-----------------------------------------------------------------------------------------------------------------------
def open_DF(f):
    while (True):
        if os.access(f, os.R_OK):
            try:
                #print(f)
                with open(f) as file:
                    table = pd.DataFrame(
                        row.replace('|', '$').replace(',', '.').replace(';', '$').replace(' [INF]: ', '$[INF]:$').replace(
                            'closing log file', 'closing$log$file').split('$') for row in file)
                file.close()
                break
            except PermissionError:
                print('PermissionError ' + f)
    return  table
#-----------------------------------------------------------------------------------------------------------------------
def delVD(dirPath):
    list_dir_VD = os.listdir(path=dirPath + '\VD')
    for i in list_dir_VD:
        if os.access(dirPath + '/VD/' + i, os.R_OK):
            try:
                os.remove(dirPath + '/VD/' + i)
            except Exception:
                pass
#-----------------------------------------------------------------------------------------------------------------------