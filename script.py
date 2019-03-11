
import os
import shutil
import rawpy
import imageio
from xml.dom import minidom
import json

src = '/Users/leigao/Desktop/vader/bisque-20190303.232959/Yellowbank 2014.11.13'
img_dest = '/Users/leigao/Desktop/vader/bisque-20190303.232959/imageSet'

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




