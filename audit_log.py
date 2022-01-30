#!/usr/bin/env python3
import csv
import os
from pathlib import Path



def file_format(FILENAME,banner_date,banner_time,banner_lane,banner_dir,banner_length,banner_speed,banner_class,banner_axle,banner_note,pvr_line_number,audit_status,audit_user,comments): # requires 9 objects
#def format_gps():
    #FILENAME = 'TEST.csv'
    if os.path.exists(FILENAME):
        with open(FILENAME, 'a', newline='') as csvfile:
            fieldnames = ['Date', 'Time','Lane','Direction','Length','Speed','Class','Axle','Note','PVR line number','Pass/Fail','Audit User','Comments']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writerow({'Date':banner_date,'Time':banner_time,'Lane':banner_lane,'Direction':banner_dir,'Length':banner_length,'Speed':banner_speed,'Class':banner_class,'Axle':banner_axle,'Note':banner_note,'PVR line number':pvr_line_number,'Pass/Fail':audit_status,'Audit User':audit_user,'Comments':comments})
    else:
        with open(FILENAME, 'a', newline='') as csvfile:
            fieldnames = ['Date', 'Time','Lane','Direction','Length','Speed','Class','Axle','Note','PVR line number','Pass/Fail','Audit User','Comments']
            #fieldnames = ['banner_date', 'banner_time','banner_lane','banner_dir','banner_length','banner_speed','banner_class','banner_axle','banner_note','banner_note','banner_lane_number','comment']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerow({'Date':banner_date,'Time':banner_time,'Lane':banner_lane,'Direction':banner_dir,'Length':banner_length,'Speed':banner_speed,'Class':banner_class,'Axle':banner_axle,'Note':banner_note,'PVR line number':pvr_line_number,'Pass/Fail':audit_status,'Audit User':audit_user,'Comments':comments})


