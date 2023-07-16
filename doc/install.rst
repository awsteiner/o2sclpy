.. _install:

Installation and Requirements
=============================

:ref:`O2sclpy <o2sclpy>`

O₂sclpy requires an installation of the development version of O₂scl.
The release version, O₂sclpy 0.928, requires the O₂scl v0.928 release
from https://github.com/awsteiner/o2scl/releases/tag/v0.928 .

.. and the
   development version, O₂sclpy 0.928a1, requires that the most recent
   version of O₂scl from the master branch on github is installed on your
   machine.

The most recent release version of O₂sclpy can be installed with e.g.
``pip3 install o2sclpy``. If you want to install the development
version (v0.928a1), you can clone the git repository, change directory
to the O₂sclpy directory, and then use e.g. ``pip3 install .`` if you
want to use the pip package manager or ``python3 setup.py install`` to
do a direct installation.

O₂sclpy requires python3 packages `requests
<https://pypi.org/project/requests/>`_, `h5py
<https://www.h5py.org/>`_, `numpy <https://www.numpy.org>`_, and
`matplotlib <https://matplotlib.org>`_. O₂sclpy also assumes LaTeX is
installed on your system.

O₂sclpy dynamically loads the O₂scl libraries using the
:class:`o2sclpy.linker` python class. This class may require some
additional information about your system in order to perform the
dynamic loading properly. See :ref:`Linking with O₂scl <link2>` for
more details.

