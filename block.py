
import os
import shutil
from PIL import Image
import numpy as np
#import xml.etree.ElementTree as ET
from lxml import etree as ET
from xml.dom import minidom
import json
import math

def block_image(src, dest):
    #takes in a source directory that contains bisque xml files, an output directory and a dictionary defining the segmentation classes
    #outputs an xml file in VOC notation with point notation denoted by a point object
    counter = 0
    src_files = os.listdir(src)
    for file_name in src_files:
        full_file_name = os.path.join(src, file_name)
        filename, file_extension = os.path.splitext(full_file_name)
        print(file_name[0:len(file_name)-4])
        if (file_extension == '.jpg'):
            pic = Image.open(full_file_name)
            arr = np.array(pic)
            print(np.shape(arr))
            left = 0
            top = 0
            right = 540
            bottom = 360
            for i in range(0,100):
                left = 540*(i%10)
                top = 360*math.floor(i/10)
                right = left + 540
                bottom = top + 360
                if(i%10 == 9):
                    right = 5496
                if(math.floor(i/10) == 9):
                    bottom = 3670
                cropped = pic.crop((left, top, right, bottom))
                cropped.save(dest+"/"+file_name[0:len(file_name)-4]+file_name[0:len(file_name)-4] + str(i) + ".jpg")
                out = '<annotation><folder>Bisque</folder><filename>IMG_6052.jpg</filename><size><width>5496</width><height>3670</height><depth>3</depth></size><object><name>15</name><x>2678.0</x><y>719.0</y></object><object><name>15</name><x>2649.0</x><y>536.0</y></object><object><name>15</name><x>1546.0</x><y>445.0</y></object><object><name>15</name><x>486.0</x><y>352.0</y></object><object><name>15</name><x>492.0</x><y>514.0</y></object><object><name>2</name><x>3993.0</x><y>1042.0</y></object><object><name>2</name><x>3485.0</x><y>808.0</y></object><object><name>2</name><x>3895.0</x><y>630.0</y></object><object><name>15</name><x>3102.0</x><y>761.0</y></object><object><name>2</name><x>3535.0</x><y>992.0</y></object><object><name>15</name><x>1921.0</x><y>831.0</y></object><object><name>2</name><x>2386.0</x><y>2154.0</y></object><object><name>20</name><x>4302.0</x><y>2660.0</y></object><object><name>2</name><x>4236.0</x><y>2389.0</y></object><object><name>20</name><x>3764.0</x><y>2343.0</y></object><object><name>20</name><x>1164.0</x><y>1735.0</y></object><object><name>20</name><x>1163.0</x><y>1958.0</y></object><object><name>15</name><x>1153.0</x><y>777.0</y></object><object><name>15</name><x>847.0</x><y>393.0</y></object><object><name>11</name><x>1558.0</x><y>1175.0</y></object><object><name>15</name><x>780.0</x><y>1104.0</y></object><object><name>2</name><x>458.0</x><y>1062.0</y></object><object><name>2</name><x>435.0</x><y>1225.0</y></object><object><name>20</name><x>2703.0</x><y>922.0</y></object><object><name>17</name><x>1475.0</x><y>1417.5</y></object><object><name>11</name><x>2294.0</x><y>865.0</y></object></annotation>'
                file = open(dest+str(i)+".xml", "w")
                file.write(out)
                file.close()

#takes in a list of images to stitch back together
def stitch(images){
    img_arr = np.zeros((3670,5496))
    for i in images:
        pic = Image.open(i)
        arr = np.array(pic)
        left = 540*(i%10)
        top = 360*math.floor(i/10)
        right = left + 540
        bottom = top + 360
        if(i%10 == 9):
            right = 5496
        if(math.floor(i/10) == 9):
            bottom = 3670
        img_arr[top:bottom, left:right] = arr

    img = Image.fromarray(img_arr)
    img.show()
}

if __name__ == "__main__":
    import sys
    
    src = sys.argv[1]
    img_dest = sys.argv[2]
    block_image(src, img_dest)







