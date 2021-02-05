#!python3

import os
from helpers import get_root_directory

'''
Writes line in employer specific file saying I have logged in to work.
Arguments: <string> employer name, <datetime.datetime object> work_start_time
Return type: None
'''
def clock_in(employer, work_start_time):
    # find/create employer file
    os.makedirs('work_study', exist_ok=True)
    with open(get_root_directory()+os.path.join('work_study', '{}_hours.txt'.format(employer)), 'a+') as file:
        file.write('Started work: {}\n'.format(work_start_time))

'''
Writes line in employer specific file saying I have logged out of work.
Arguments: <string> employer name, <datetime.datetime object> work_stop_time, <datetime.timedelta object> duration
Return type: None
'''        
def clock_out(employer, work_stop_time, duration):
    # find/create employer file
    os.makedirs('work_study', exist_ok=True)
    with open(get_root_directory()+os.path.join('work_study', '{}_hours.txt'.format(employer)), 'a+') as file:
        file.write('Ended work: {}\n'.format(work_stop_time))
        file.write('Duration: {}\n'.format(duration))
