import psutil
import os
import time
while(True):
    l = []
    for process in psutil.process_iter():
        p = process.pid
        name = process.name()
        if name == 'python.exe':
            pr = psutil.Process(p).cmdline()
            l.append(pr[1])
    print(l)
    if 'main.py' not in l:
        os.system('python C:/Users/Mikhail.Ilinykh/Desktop/1/4.2/main.py')
    else:
        print('exist')
