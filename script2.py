from xml.dom import minidom

mydoc = minidom.parse('IMG_6020.CR2.xml')

point = mydoc.getElementsByTagName('vertex')

for elem in point:

	print(elem.attributes['x'].value, elem.attributes['y'].value)