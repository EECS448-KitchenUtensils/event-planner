from datetime import time

def input_list_to_time_list(input_list):
    time_list = []
    for x,input in enumerate(input_list):
        if input != 0 and input != '0':
            time_24 = x // 2
            minutes = 0
            if x % 2 == 1:
                minutes = 30
            time_list.append(time(hour=time_24, minute=minutes))
    return time_list