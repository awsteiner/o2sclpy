from base import *

class shared_ptr_table_units(table_units):
    """
    Python interface for class :ref:`table<> <o2scl:table<>>`.
    """

    _ptr=0
    _dll=0
    sp_ptr=0

    def __init__(self,dll):
        """
        Init function for shared pointer. We don't actually create
        an object here, we just set the pointers to zero.
        """

        self.sp_ptr=0
        self._dll=dll
        self._ptr=0
        return

    def __del__(self):
        """
        Delete function for shared pointer. We delete the 
        shared pointer only if its non-zero.
        """

        if self.sp_ptr!=0:
            f=self._dll.o2scl_free_shared_ptr_table_units
            f.argtypes=[ctypes.c_void_p]
            f(self.sp_ptr)
        return

    def __set_ptr(self):
        """
        Create a table pointer from the shared pointer
        """
        f=self._dll.o2scl_shared_ptr_table_units_ptr
        f.restype=ctypes.c_void_p
        self._ptr=f()

class tov_solve:
    """
    """
    
    _ptr=0
    _dll=0

    def __init__(self,dll):
        """
        Init function for class tov_solve .
        """

        f=dll.o2scl_create_tov_solve
        f.restype=ctypes.c_void_p
        f.argtypes=[]
        self._ptr=f()
        self._dll=dll
        return

    def __del__(self):
        """
        Delete function for class tov_solve .
        """

        f=self._dll.o2scl_free_tov_solve
        f.argtypes=[ctypes.c_void_p]
        f(self._ptr)
        return

    def get_results(self):
        """
        """
        sptu=shared_ptr_table_units()
        f=self._dll.o2scl_tov_solve_get_results
        f.restypes=[ctypes.c_void_p]
        sptu.sp_ptr=f(self._ptr)
        sptu.__set_ptr()
        return sptu
        
