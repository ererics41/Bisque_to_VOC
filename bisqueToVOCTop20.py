
import os
import shutil
import rawpy
import imageio
#import xml.etree.ElementTree as ET
from lxml import etree as ET
from xml.dom import minidom
import json

classes = {"Substrate - hydriod/bryozoan complex":1, "Rhodophyta - encrusting coralline spp":2, "Cnidaria - Corynactis californica":3, "Arthropoda - barnacles unidentified":4, "Rhodophyta - Rhodymenia spp":5, "Substrate - amphipod tube complex":6, "Rhodophyta - Chondracanthus big blade sp":7, "Cnidaria - Astrangia haimei":8, "Rhodophyta - red turf spp unidentified":9, "Annelida - Phragmatopoma californica":10, "Ectoprocta - peach encrusting bryozoan unidentified":11, "Echinodermata - Strongylocentrotus purpuratus":12, "Echinodermata - Mesocentrotus franciscanus":13, "Ectoprocta - Watersipora subatra":14, "Rhodophyta - Corallina officinalis var chilensis":15, "Echinodermata - Ophiothrix spiculata":16, "Chordata - Trididemnum spp":17, "Ectoprocta - Diaperoforma californica":18, "Rhodophyta - filamentous red spp unidentified":19, "Substrate - Benthic Diatoms":20}

def writeXML(src, ann_dest, img_dest):
    #takes in a source directory that contains bisque xml files, an output directory and a dictionary defining the segmentation classes
    #outputs an xml file in VOC notation with point notation denoted by a point object
    counter = 0
    src_files = os.listdir(src)
    for file_name in src_files:
        full_file_name = os.path.join(src, file_name)
        filename, file_extension = os.path.splitext(full_file_name)
        
        if (file_extension == '.CR2'):
            raw = rawpy.imread(full_file_name)
            rgb = raw.postprocess()
            dest = img_dest + filename[len(src)::] + '.jpg'
            #print(dest)
            imageio.imsave(dest, rgb)
            if counter == 0:
                open("bisque_val_cls.txt", "w").close()
                open("bisque_train_cls.txt", "w").close()
            if counter < 600:
                file = open("bisque_val_cls.txt", "a")
                file.write("/JPEGImages/"+ filename[len(src)::] + '.jpg' +"\n")
                file.close()
            else:
                file = open("bisque_train_cls.txt", "a")
                file.write("/JPEGImages"+ filename[len(src)::] + '.jpg' +"\n")
                file.close()
            counter = counter + 1
            print("counter is ", counter)
        if (file_extension == '.xml'):
            #print(file_name)
            #mydoc is the xml file currently being read from
            mydoc = minidom.parse(full_file_name)
            point = mydoc.getElementsByTagName('vertex')
            gobject = mydoc.getElementsByTagName('gobject')

			# xml file being created
            annotation = ET.Element('annotation')
            folder = ET.SubElement(annotation, 'folder')
            folder.text = 'Bisque'
            file = ET.SubElement(annotation, 'filename')
            file.text = file_name[0:len(file_name)-8] + '.jpg'
            size = ET.SubElement(annotation, 'size')
            width = ET.SubElement(size, 'width')
            width.text = '5496'
            height = ET.SubElement(size, 'height')
            height.text = '3670'
            depth = ET.SubElement(size, 'depth')
            depth.text = '3'
            
            
			# generate the entries of points list by iterating through all points
            for i in range(len(point)):
                className = gobject[i].attributes['type'].value
                if classes.get(className, -1) != -1:
                    x = point[i].attributes['x'].value
                    y = point[i].attributes['y'].value
                    obj = ET.SubElement(annotation, 'object')
                    name = ET.SubElement(obj, 'name')
                    name.text = str(classes[className])
                    point_x = ET.SubElement(obj, 'x')
                    point_x.text = str(x)
                    point_y = ET.SubElement(obj, 'y')
                    point_y.text = str(y)
            current = os.getcwd()
            os.chdir(ann_dest)
            file = open(file_name[0:len(file_name)-8]+".xml", "w")
            out = str(ET.tostring(annotation))
            file.write(out[2:len(out)-1])
            file.close()
            os.chdir(current)



def getClasses(src, dest):
	#a function that takes in the src and destination directories and iterates through all xml docs to find all possible classes
	#a Class_Labels.txt is then generated converting all classes into a number according to the PASCAL VOC class naming convention
	#a dictionary of the names is then returned
	src_files = os.listdir(src)
	labels = []
	label_to_id = {"background":0}

	#traverse and determine all classes 
	for file_name in src_files:
		full_file_name = os.path.join(src, file_name)
		filename, file_extension = os.path.splitext(full_file_name)
		#iterate through all xml docs
		if (file_extension == '.xml'):
			#use minidom to parse the xml document
			mydoc = minidom.parse(full_file_name)
			#find list of classes using 'gobject' tag in xml doc
			gobject = mydoc.getElementsByTagName('gobject')
			for i in range(len(gobject)):
				className = gobject[i].attributes['type'].value
				if className not in labels and className != 'Occurrence':
					labels.append(className)
	#sort list of all classnames and assign them to a corresponding class number
	labels.sort()
	for i in range(len(labels)):
		label_to_id[labels[i]] = i+1

	#write a class.txt file
	class_text = open(img_dest+"/Class_Labels.txt", "w")
	for i, j in enumerate(labels):
		class_text.write(str(i+1) + ": " + str(j) + "\n")
	class_text.close()

	return label_to_id

src = '/Users/eric/Desktop/Bisque_to_VOC/bisque-all/Watersipora-Reef_All'
#src = '/Users/eric/Desktop/Bisque_to_VOC/Yellowbank2014.11.13'
img_dest = '/Users/eric/Desktop/Bisque_to_VOC/Annotations'
img_dest1 = '/Users/eric/Desktop/Bisque_to_VOC/JPEGImages'
writeXML(src, img_dest, img_dest1)







