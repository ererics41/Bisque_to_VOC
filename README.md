# Bisque_to_VOC
There are several scripts in this repository meant to convert a marine science dataset stored on bisque into
another form for reserach purposes. 

bisqueToVOCTop20 - This script looks at only the top 20 classes of the marine science dataset and converts it 
into a format similar to VOC format in order to be compaitible with code found here: https://github.com/jiwoon-ahn/psa.

bisque_to_voc - This script takes a general set of xml files and images and converts it into a VOC like format. 
It starts knowing nothing about the classes and first goes through all XML to discover all possible classes and 
then labels them from 1 to n based on alphabetical order. Once it's found all classes, it converts CR2 images to JPEG 
images an relabels the annotations to match VOC.

bisque_to_json - This script is meant to convert the marine science dataset annotations into a json format consistent
with the point annotation format used in the paper What's the Point, which can be found here:
http://calvin.inf.ed.ac.uk/wp-content/uploads/Publications/bearman16eccv.pdf
