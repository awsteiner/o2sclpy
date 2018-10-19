import setuptools

with open("README.md","r") as file_handle:
    long_description=file_handle.read()

setuptools.setup(name='o2sclpy',
                 version='0.922.1',
                 author='Andrew W. Steiner',
                 author_email='awsteiner@mykolab.com',
                 description='Python extensions for O2scl',
                 long_description=long_description,
                 long_description_content_type="text/markdown",                 
                 url='https://isospin.roam.utk.edu/static/code/o2sclpy',
                 license='GPLv3',
                 packages=['o2sclpy'],
                 install_requires=['h5py','numpy','matplotlib'],
                 zip_safe=False,scripts=['bin/o2graph'],
                 classifiers=[
                     'Development Status :: 4 - Beta',
                     ('License :: OSI Approved :: '+
                      'GNU General Public License v3 (GPLv3)'),
                     'Programming Language :: Python :: 3 :: Only',
                     'Topic :: Scientific/Engineering'
                 ])
