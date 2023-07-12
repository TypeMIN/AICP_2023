import ctypes
import pathlib




if __name__ == "__main__":
	libname = pathlib.Path().absolute() / "biLouvain/"
	c_lib = ctypes.CDLL(libname)
