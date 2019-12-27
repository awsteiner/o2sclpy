#  -------------------------------------------------------------------
#  
#  Copyright (C) 2006-2020, Andrew W. Steiner
#  
#  This file is part of O2sclpy.
#  
#  O2sclpy is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 3 of the License, or
#  (at your option) any later version.
#  
#  O2sclpy is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with O2sclpy. If not, see <http://www.gnu.org/licenses/>.
#  
#  -------------------------------------------------------------------
#

class hdf5_reader:
    """
    Class to read an O2scl object from an HDF5 file. This is
    used by :py:class:`o2sclpy.plotter` to read HDF5 files.
    """

    list_of_dsets=[]
    """
    Data set list used by :py:func:`cloud_file.hdf5_is_object_type`.
    """
    search_type=''
    """
    O2scl type used by :py:func:`cloud_file.hdf5_is_object_type`.
    """

    def hdf5_is_object_type(self,name,obj):
        """
        This is an internal function not intended for use by the end-user.
        If object ``obj`` named ``name`` is of type 'search_type',
        then this function adds that name to 'list_of_dsets'
        """
        # Convert search_type to a bytes object
        search_type_bytes=bytes(self.search_type,'utf-8')
        if isinstance(obj,h5py.Group):
            if 'o2scl_type' in obj.keys():
                o2scl_type_dset=obj['o2scl_type']
                if o2scl_type_dset.__getitem__(0) == search_type_bytes:
                    self.list_of_dsets.append(name)
        return

    def h5read_first_type(self,fname,loc_type):
        """
        Read the first object of type ``loc_type`` from file named ``fname``
        """
        del self.list_of_dsets[:]
        self.search_type=loc_type
        file=h5py.File(fname,'r')
        file.visititems(self.hdf5_is_object_type)
        if len(self.list_of_dsets)==0:
            str='Could not object of type '+loc_type+' in file '+fname+'.'
            raise RuntimeError(str)
        return file[self.list_of_dsets[0]]

    def h5read_name(self,fname,name):
        """
        Read object named ``name`` from file named ``fname``
        """
        file=h5py.File(fname,'r')
        obj=file[name]
        o2scl_type_dset=obj['o2scl_type']
        loc_type=o2scl_type_dset.__getitem__(0)
        return (obj,loc_type)
    
    def h5read_type_named(self,fname,loc_type,name):
        """
        Read object of type ``loc_type`` named ``name`` from file 
        named ``fname``
        """
        del self.list_of_dsets[:]
        self.search_type=loc_type
        file=h5py.File(fname,'r')
        file.visititems(self.hdf5_is_object_type)
        if name in self.list_of_dsets:
            return file[name]
        str='No object of type '+loc_type+' named '+name+' in file '+fname+'.'
        raise RuntimeError(str)
        return

