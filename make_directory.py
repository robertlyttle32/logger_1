import time
import datetime
import os
import sys
from datetime import datetime
from datetime import timedelta

camera_1_folder = 'camera_1'
camera_2_folder = 'camera_2'
camera_3_folder = 'camera_3'
camera_4_folder = 'camera_4'


STORAGE_DIRECTORY = r'C:\Users\rlyttle\Downloads\MAKE_DIRECTORY'

def make_directory():
    def image_folder_name():
        get_image_time = datetime.now()
        camera_sub_dir = get_image_time.strftime("%Y_%m_%d")
        return camera_sub_dir

    class cameraDirectory: #camera_root_dir, camera_sub_dir
        def __init__(self, x, y):
            self.x = x
            self.y = y

        def getCameraDirectory(self):
            os.chdir(self.x)
            path = (os.getcwd())
            if os.path.exists(self.y):
                pass
            else:
                os.mkdir(os.path.join(path, self.y))
                return


    class imageDirectory: #STORAGE_DIRECTORY, camera_sub_dir
        def __init__(self, x, y):
            self.x = x
            self.y = y

        def getImageDirectory(self):
            os.chdir(STORAGE_DIRECTORY)
            os.chdir(self.x)
            path = (os.getcwd())
            if os.path.exists(self.y):
                pass
            else:
                os.mkdir(os.path.join(path, self.y))
                return

    #test image root directory
    image_directory = cameraDirectory(STORAGE_DIRECTORY, camera_1_folder)
    image_directory.getCameraDirectory()
    image_directory = cameraDirectory(STORAGE_DIRECTORY, camera_2_folder)
    image_directory.getCameraDirectory()
    image_directory = cameraDirectory(STORAGE_DIRECTORY, camera_3_folder)
    image_directory.getCameraDirectory()
    image_directory = cameraDirectory(STORAGE_DIRECTORY, camera_4_folder)
    image_directory.getCameraDirectory()


    #test image sub-directory
    image_sub_directory = imageDirectory(camera_1_folder, image_folder_name())
    image_sub_directory.getImageDirectory()
    #os.chdir(STORAGE_DIRECTORY)
    image_sub_directory = imageDirectory(camera_2_folder, image_folder_name())
    image_sub_directory.getImageDirectory()
    #os.chdir(STORAGE_DIRECTORY)
    image_sub_directory = imageDirectory(camera_3_folder, image_folder_name())
    image_sub_directory.getImageDirectory()
    #os.chdir(STORAGE_DIRECTORY)
    print('STORAGE_DIRECTORY IS: ', STORAGE_DIRECTORY)
    image_sub_directory = imageDirectory(camera_4_folder, image_folder_name())
    image_sub_directory.getImageDirectory()

make_directory()
