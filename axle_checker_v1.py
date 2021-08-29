import time
from datetime import datetime

class presentsChecker:
    def __init__(self, start_entry,stop_entry,start_exit,stop_exit):
        self.start_entry = start_entry
        self.stop_entry = stop_entry
        self.start_exit = start_exit
        self.stop_exit = stop_exit

    def presents_checker(self):
        entries = []
        entries = [self.start_entry,self.stop_entry,self.start_exit,self.stop_exit]

        #start_entry
        if entries == [1,0,0,0] or [1,1,0,0]:
            global start_entry
            start_entry = 'start_entry_{}'.format(get_time())
            #print('start entry entries: ', entries)
            print(start_entry)

        #stop_entry
        if entries == [0,1,0,0] or [0,1,1,0]:
            global stop_entry
            stop_entry = 'stop_entry_{}'.format(get_time())
            #print('stop entry entries: ', entries)
            print(stop_entry)

        #start_exit
        if entries == [0,0,1,0] or [0,0,1,1]:
            global start_exit
            start_exit = 'start_exit_{}'.format(get_time())
            #print('start exit entries: ', entries)
            print(start_exit)

        #stop_exit
        if entries == [0,0,0,1]:
            global stop_exit
            stop_exit = 'stop_exit_{}'.format(get_time())
            #print('stop exit entries: ', entries)
            print(start_entry,stop_entry,start_exit,stop_exit)



def get_time():
    timer = datetime.now()
    #timer = now.strftime("%d_%m_%Y_%H:%M:%S")
    return timer

w = 0
x = 0
y = 0
z = 1

#test run
test = presentsChecker(w,x,y,z)
print(test.presents_checker())
