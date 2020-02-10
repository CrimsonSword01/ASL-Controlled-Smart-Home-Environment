import time
from datetime import datetime
current_time = datetime.now()


def logStatus(status):
    current_time = str(datetime.now())
    if status == 'opening':
        file = open('logHistory.txt', 'a')
        file.write('=========================================\n')
        file.write('program opened at: ' + current_time + '\n')
        file.close()
    elif status == 'img':
        file = open('logHistory.txt', 'a')
        file.write('img taken at: ' + current_time + '\n')
        file.close()
    elif status == 'closing':
        file = open('logHistory.txt', 'a')
        file.write('program closed at: ' + current_time + '\n')
        file.close()
    else:
        print('invalid input')
