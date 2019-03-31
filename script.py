
import os
import shutil
import rawpy
import imageio
from xml.dom import minidom
import json
import tkinter as tk
from tkinter import filedialog

"""root = tk.Tk()
root.withdraw()

src = filedialog.askdirectory()

img_dest = filedialog.askdirectory()
"""

src = '/Users/leigao/Desktop/VisionResearchLab/Bisque_to_VOC/Yellowbank2014.11.13'
img_dest = '/Users/leigao/Desktop/VisionResearchLab/Bisque_to_VOC/imageSet'

src_files = os.listdir(src)

labels = []
label_to_id = {"background":0}
rtn_json = {}

for file_name in src_files:
	full_file_name = os.path.join(src, file_name)
	filename, file_extension = os.path.splitext(full_file_name)
	if (file_extension == '.CR2'):
    	#shutil.copy(full_file_name, img_dest)
		raw = rawpy.imread(full_file_name)
		rgb = raw.postprocess()
		dest = img_dest + filename[len(src)::] + '.jpg'
		#print(dest)
		imageio.imsave(dest, rgb)
	elif (file_extension == '.xml'):
		mydoc = minidom.parse(full_file_name)
		point = mydoc.getElementsByTagName('vertex')
		gobject = mydoc.getElementsByTagName('gobject')
		offset = 0
		points_list = []
		for i in range(len(point)):
			point_dict = {}
			className = gobject[i+offset].attributes['type'].value
			if className == 'Occurrence':
				offset = offset+1
				className = gobject[i+offset].attributes['type'].value
			if className not in labels and className != 'Occurrence':
				labels.append(className)
			x = point[i].attributes['x'].value
			y = point[i].attributes['y'].value
			point_dict['x'] = x
			point_dict['y'] = y
			point_dict['cls'] = className
			point_dict['rank'] = -1
			points_list.append(point_dict)

		name = (mydoc.getElementsByTagName('image')[0].attributes['name'].value)
		name = name[0:-4]
		rtn_json[name] = points_list


labels.sort()
for i in range(len(labels)):
	label_to_id[labels[i]] = i+1

for img in rtn_json.values():
	for point in img:
		point['cls'] = label_to_id[point['cls']]

#print(rtn_json)
with open(img_dest + '/data.json', 'w') as outfile:
    json.dump(rtn_json, outfile)

class_text = open(img_dest+"/Class_Labels.txt", "w")
for i, j in enumerate(labels):
	class_text.write(str(i+1) + ": " + str(j) + "\n")
class_text.close()
