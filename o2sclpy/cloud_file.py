# For MD5 hashes
import hashlib

class cloud_file:
    """
    A class to manage downloading files from the internet.

    .. warning:: This class has several potential security issues
                 (even if the md5 sum is verified) and should not be
                 used without due care.
    """
    
    force_subdir=True
    """
    If true, force the same subdirectory structure
    """
    env_var=''
    """
    The environment variable which specifies the data directory
    """
    verbose=1
    """
    The verbosity parameter
    """

    # These are commented out until the code is rewritten to
    # allow for them
    #username=''
    #The HTTP username
    #password=''
    #The HTTP password

    def md5(fname):
        """
        Compute the md5 hash of the specified file. This function
        reads 4k bytes at a time and updates the hash for each
        read in order to prevent from having to read the entire
        file in memory at once.
        """
        hash_md5 = hashlib.md5()
        with open(fname, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()
    
    def download_file(self,filename,url,md5sum,directory):
        """
        This function proceeds in the following way:

        First, if ``directory`` is not then the function tries to find
        the requested directory. If it is not found, then ``mkdir -p``
        is used to create it. If this doesn't work, then a
        ``FileNotFoundError`` exception is thrown.

        The function then looks for the requested file in the
        directory. If the file is found
        and ``md5sum`` is not empty, then it compares it to the MD5
        checksum of the file.

        If the file is not found or if the checksum was specified
        and didn't match, then this function prompts the user
        to proceed before using
        ``urllib.request.urlretrieve()`` to download the file from
        ``url``. Afterwards, the MD5 checksum is checked again. 
        If the file cannot be found or if the checksum doesn't
        match, a ``ConnectionError`` exception is thrown.
        Otherwise, the function was successful, and the full filename 
        (including subdirectory if applicable) is returned.

        This function works similarly to the C++ O\ :sub:`2`\ scl
        function ``o2scl::cloud_file::get_file_hash()``.
        """
        
        # Test for the existence of the directory and create it if
        # necessary
        if directory!='':
            if os.path.isdir(directory)==False:
                if verbose>0:
                    print('Directory '+directory+'not found.')
                    print('Trying to automatically create using "mkdir -p"')
                cmd='mkdir -p '+directory
                ret=os.system(cmd)
                if ret!=0:
                    raise FileNotFoundError('Directory does '+
                                            'not exist and failed to create.')
                
        # The local filename
        full_name=directory+'/'+filename

        # Check the hash
        hash_match=False
        if md5sum=='':
            hash_match=True
        elif os.path.isfile(full_name)==True:
            mhash2=mda5(full_name)
            if md5sum==mhash2:
                hash_match=True
            elif verbose>0:
                print('Hash of file',full_name,'did not match',md5sum)
        elif verbose>0:
            print('Could not find file',full_name)
            
        # Now download the file if it's not already present
        if hash_match==False or os.path.isfile(full_name)==False:
            response=input('Hash did not match or data file '+full_name+
                           ' not found. Download (y/Y/n/N)? ')
            ret=1
            if response=='y' or response=='Y':
                if verbose>0:
                    print('Trying to download:')
                urllib.request.urlretrieve(url,full_name)
                ret=0
            if ret==0:
                mhash2=mda5(full_name)
                if md5sum!=mhash2:
                    raise ConnectionError('Downloaded file but '+
                                          'has does not match.')
            if ret!=0:
                raise ConnectionError('Failed to obtain data file.')
    
        # Return 0 for success
        return 0

