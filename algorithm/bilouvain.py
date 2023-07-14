import ctypes
import pathlib
import os

def run(input_file):
	input_file =  "../" + input_file
	os.chdir('../algorithm/biLouvain')
	os.system('./biLouvain -i {0} -d " " '.format(input_file))
	return 0
