#Author: Robert Lyttle
#Date: 10/20/21
#Description: download files matching extenstion
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



myHostname = "hostname/ip"
myUsername = "Username"
myPassword = "Password"

with pysftp.Connection(host=myHostname, username=myUsername, password=myPassword) as sftp:
    print("Connection succesfully stablished ... ")

    # Define the remote path file path
    remoteFilePath = '/tmp/home/data/'
    localFilePath = '/home/rdl-nano2/rdl_mobile_tech/'


    for filename in sftp.listdir(remoteFilePath):
        if fnmatch.fnmatch(filename, '*.pvr'):
            print(filename)
            sftp.get(remoteFilePath + "/" + filename, localFilePath + "/" + filename)


