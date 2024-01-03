import setuptools

with open("README.md","r") as file_handle:
    long_description=file_handle.read()

setuptools.setup(name='o2sclpy',
                 version='0.929a1',
                 author='Andrew W. Steiner',
                 author_email='awsteiner0@protonmail.com',
                 description='Python extensions for O2scl',
                 long_description=long_description,
                 long_description_content_type="text/markdown",                 
                 url='https://neutronstars.utk.edu/code/o2sclpy',
                 license='GPLv3',
                 packages=['o2sclpy'],
                 install_requires=['numpy','matplotlib>=3.1'],
                 zip_safe=False,scripts=['bin/o2graph'],
                 classifiers=[
                     'Development Status :: 4 - Beta',
                     ('License :: OSI Approved :: '+
                      'GNU General Public License v3 (GPLv3)'),
                     'Programming Language :: Python :: 3 :: Only',
                     'Topic :: Scientific/Engineering'
                 ])
