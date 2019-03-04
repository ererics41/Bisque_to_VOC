
import os
import shutil
import rawpy
import imageio


src = '/Users/leigao/Desktop/vader/bisque-20190303.232959/Yellowbank 2014.11.13'
img_dest = '/Users/leigao/Desktop/vader/bisque-20190303.232959/imageSet'

src_files = os.listdir(src)
for file_name in src_files:
	full_file_name = os.path.join(src, file_name)
	filename, file_extension = os.path.splitext(full_file_name)
	if (file_extension == '.CR2'):
    	#shutil.copy(full_file_name, img_dest)
		raw = rawpy.imread(full_file_name)
		rgb = raw.postprocess()
		dest = img_dest + filename[len(src)::] + '.jpg'
		print(dest)
		imageio.imsave(dest, rgb)