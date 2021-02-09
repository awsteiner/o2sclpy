# from https://stackoverflow.com/questions/24277488/in-python-how-to-capture-
# the-stdout-from-a-c-shared-library-to-a-variable
import ctypes
import os
import sys
import threading

# Create pipe and dup2() the write end of it on top of stdout, saving a copy
# of the old stdout
#stdout_fileno = sys.stdout.fileno()

class cap_cout:

    stdout_fileno=1
    captured_stdout = ''
    stdout_pipe=0
    stdout_save=0
    t=0
    
    def drain_pipe(self):
        while True:
            data=os.read(self.stdout_pipe[0],1024)
            if not data:
                break
            self.captured_stdout += str(data,'UTF-8')
        return
        
    def __init__(self):
        self.stdout_save=os.dup(self.stdout_fileno)
        self.stdout_pipe=os.pipe()
        os.dup2(self.stdout_pipe[1],self.stdout_fileno)
        os.close(self.stdout_pipe[1])
        self.t=threading.Thread(target=self.drain_pipe)
        self.t.start()

    def close(self):
        os.close(self.stdout_fileno)
        self.t.join()

        # Clean up the pipe and restore the original stdout
        os.close(self.stdout_pipe[0])
        os.dup2(self.stdout_save,self.stdout_fileno)
        os.close(self.stdout_save)
        print('Contents of std::cout:')
        print(self.captured_stdout)
