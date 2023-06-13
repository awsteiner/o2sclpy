#  -------------------------------------------------------------------
#  
#  Copyright (C) 2006-2023, Andrew W. Steiner
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
import h5py
from o2sclpy.utils import get_str_array

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
    filet=0
    """
    File handle
    """
    filename=''
    """
    Current filename
    """

    def is_object_type(self,name,obj):
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

    def read_first_type(self,fname,loc_type):
        """
        Read the first O2scl object of type ``loc_type`` from file 
        named ``fname``
        """
        # We have to delete the previous list, because it
        # may have been generated from a different type
        if self.list_of_dsets!=[]:
            del self.list_of_dsets[:]
        # If a different file has been opened, then close it
        # and open the new file
        if fname!=self.filename and self.filename!='':
            #print('closing',self.filename)
            self.filet.close()
        if fname!=self.filename:
            #print('opening',fname)
            self.filet=h5py.File(fname,'r')
            self.filename=fname
        self.search_type=loc_type
        self.filet.visititems(self.is_object_type)
        if len(self.list_of_dsets)==0:
            str='Could not object of type '+loc_type+' in file '+fname+'.'
            raise RuntimeError(str)
        return self.filet[self.list_of_dsets[0]]

    def read_name_type(self,fname,name):
        """
        Read o2scl object named ``name`` from file named ``fname``
        and return 'object,type'
        """
        # If a different file has been opened, then close it
        # and open the new file
        if fname!=self.filename and self.filename!='':
            #print('closing',self.filename)
            self.filet.close()
        if fname!=self.filename:
            #print('opening',fname)
            self.filet=h5py.File(fname,'r')
            self.filename=fname
        obj=self.filet[name]
        o2scl_type_dset=obj['o2scl_type']
        loc_type=o2scl_type_dset.__getitem__(0)
        return (obj,loc_type)
    
    def read_name(self,fname,name):
        """
        Read O2scl object named ``name`` from file named ``fname``
        and return the 'object,type'
        """
        # If a different file has been opened, then close it
        # and open the new file
        if fname!=self.filename and self.filename!='':
            #print('closing',self.filename)
            self.filet.close()
        if fname!=self.filename:
            #print('opening',fname)
            self.filet=h5py.File(fname,'r')
            self.filename=fname
        obj=self.filet[name]
        o2scl_type_dset=obj['o2scl_type']
        loc_type=o2scl_type_dset.__getitem__(0)
        return (obj,loc_type)
    
    def read_gen(self,fname,name):
        """
        Read non-O2scl object named ``name`` from file named ``fname``
        and return the 'object,type'
        """
        # If a different file has been opened, then close it
        # and open the new file
        if fname!=self.filename and self.filename!='':
            #print('closing',self.filename)
            self.filet.close()
        if fname!=self.filename:
            #print('opening',fname)
            self.filet=h5py.File(fname,'r')
            self.filename=fname
        obj=self.filet[name]
        return obj
    
    def read_type_named(self,fname,loc_type,name):
        """
        Read O2scl object of type ``loc_type`` named ``name`` from file 
        named ``fname``
        """
        # We have to delete the previous list, because it
        # may have been generated from a different type
        if self.list_of_dsets!=[]:
            del self.list_of_dsets[:]
        # If a different file has been opened, then close it
        # and open the new file
        if fname!=self.filename and self.filename!='':
            self.filet.close()
        if fname!=self.filename:
            self.filet=h5py.File(fname,'r')
            self.filename=fname
        self.search_type=loc_type
        self.filet.visititems(self.is_object_type)
        if name in self.list_of_dsets:
            return self.filet[name]
        str='No object of type '+loc_type+' named '+name+' in file '+fname+'.'
        raise RuntimeError(str)
        return

    def table_row_to_dict(self,obj,row):
        """
        Read a row from an O2scl table and convert it to a dictionary
        """
        col_names=obj['col_names']
        col_names2=get_str_array(col_names)
        dct={}
        for i in range(0,len(col_names2)):
            dct[col_names2[i]]=obj['data/'+col_names2[i]][row]
        return dct

    def uniform_grid_to_array(self,obj):
        """
        Convert a uniform grid object to an array
        """
        start=obj["start"][0]
        end=obj["end"][0]
        n_bins=obj["n_bins"][0]
        width=obj["width"][0]
        log=obj["log"][0]    
        arr=[]
        for i in range(0,int(n_bins)+1):
            if i==0:
                arr.append(start)
            elif i==n_bins:
                arr.append(end)
            elif log==1:
                arr.append(pow(width,i)*start)
            else:
                arr.append(i*width+start)
        return arr
    
    def close_file(self):
        """
        Close the HDF5 file
        """
        self.filet.close()
        self.filename=''
        return
    
