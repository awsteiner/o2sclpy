#  -------------------------------------------------------------------
#  
#  Copyright (C) 2006-2022, Andrew W. Steiner
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
import os
import threading

class cap_cout:
    """

    Capture ``std::cout`` into a python string in order to 
    output it to a jupyter notebook. One should use
    open() to begin reading ``std::cout`` and then close()
    to stop reading and output the contents using the Python
    print() functions.

    Based on 

    https://stackoverflow.com/questions/24277488/in-python-how-to-
    capture-the-stdout-from-a-c-shared-library-to-a-variable

    and see also 

    https://dzone.com/articles/redirecting-all-kinds-stdout

    """
    
    stdout_fileno=1
    captured_stdout=''
    stdout_pipe=0
    stdout_save=0
    thr=0
    
    def drain_pipe(self):
        """
        Collect the pipe output to ``captured_stdout``
        """
        while True:
            data=os.read(self.stdout_pipe[0],1024)
            if not data:
                break
            self.captured_stdout += str(data,'UTF-8')
        return
        
    def open(self):
        """
        Duplicate stdout and create a new pipe
        """
        self.stdout_save=os.dup(self.stdout_fileno)
        self.stdout_pipe=os.pipe()
        os.dup2(self.stdout_pipe[1],self.stdout_fileno)
        os.close(self.stdout_pipe[1])
        self.thr=threading.Thread(target=self.drain_pipe)
        self.thr.start()
        return

    def close(self):
        """
        Close the pipe and restore the original stdout
        """
        os.close(self.stdout_fileno)
        self.thr.join()

        os.close(self.stdout_pipe[0])
        os.dup2(self.stdout_save,self.stdout_fileno)
        os.close(self.stdout_save)
        print('Contents of std::cout:')
        print(self.captured_stdout)
        return
