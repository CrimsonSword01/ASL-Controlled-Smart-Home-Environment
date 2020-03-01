import time
from datetime import datetime
current_time = datetime.now()


def logStatus(status, numImgs):
    current_time = str(datetime.now())
    if status == 'opening':  # if program is being opened, document that it's being opened
        file = open('logHistory.txt', 'a')
        file.write('=========================================\n')
        file.write('program opened at: ' + current_time + '\n')
        file.close()
    elif status == 'closing':  # if program is being closed, document that it's being closed
        file = open('logHistory.txt', 'a')
        file.write('program closed at: ' + current_time + ', ' + str(numImgs) +' images recorded'+ '\n')
        file.close()
    elif status == 'clear':
        file = open('logHistory.txt', 'w')
        file.write('program cleared at: ' + current_time + '\n')
        file.close()
    else:
        print('invalid input')
