import pysftp
import os
import time
import ftplib
import gzip
import shutil
#import pathlib
import glob
import fnmatch
import re



myHostname = "10.4.1.30"
myUsername = "fst"
myPassword = "lion1999"

with pysftp.Connection(host=myHostname, username=myUsername, password=myPassword) as sftp:
    print("Connection succesfully stablished ... ")

    # Define the remote path file path
    remoteFilePath = '/tmp/home/data/'
    localFilePath = '/home/rdl-nano2/rdl_mobile_tech/'


    for filename in sftp.listdir(remoteFilePath):
        if fnmatch.fnmatch(filename, '*.pvr'):
            print(filename)
            sftp.get(remoteFilePath + "/" + filename, localFilePath + "/" + filename)


