from xml.dom import minidom

mydoc = minidom.parse('IMG_6020.CR2.xml')

point = mydoc.getElementsByTagName('vertex')
gobject = mydoc.getElementsByTagName('gobject')

labels = []
label_to_id = {"background":0}
rtn_json = {}

for elem in point:
	print(elem.attributes['x'].value, elem.attributes['y'].value)
for elem in gobject:
	className = elem.attributes['type'].value
	#print(className)
	if className == 'Occurrence':
		print('Occurrence found')
	if className not in labels and className != 'Occurrence':
		labels.append(className)

offset = 0
points_list = []
for i in range(len(point)):
	point_dict = {}
	className = gobject[i+offset].attributes['type'].value
	if className == 'Occurrence':
		offset = offset+1
		className = gobject[i+offset].attributes['type'].value
	x = point[i].attributes['x'].value
	y = point[i].attributes['y'].value
	point_dict['x'] = x
	point_dict['y'] = y
	point_dict['cls'] = className
	point_dict['rank'] = -1
	points_list.append(point_dict)


labels.sort()
for i in range(len(labels)):
	label_to_id[labels[i]] = i+1

name = (mydoc.getElementsByTagName('image')[0].attributes['name'].value)
name = name[0:-4]
rtn_json[name] = points_list

print(rtn_json)
