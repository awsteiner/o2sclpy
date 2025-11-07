.. _install:

Installation and Requirements
=============================

:ref:`O2sclpy <o2sclpy>`

The most recent release version of O₂sclpy can be installed with e.g.
``pip3 install o2sclpy``.

O₂sclpy requires an installation of the development version of O₂scl.
The release version, O₂sclpy 0.932, requires the O₂scl v0.932 release
from https://github.com/awsteiner/o2scl/releases/tag/v0.932 .

O₂sclpy requires python3 packages `numpy <https://www.numpy.org>`_, and
`matplotlib <https://matplotlib.org>`_. O₂sclpy also assumes LaTeX is
installed on your system.

O₂sclpy dynamically loads the O₂scl libraries using the
:class:`o2sclpy.linker` python class. This class may require some
additional information about your system in order to perform the
dynamic loading properly. See :ref:`Linking with O₂scl <link2>` for
more details.

Some O₂sclpy classes and ``o2graph`` commands require other Python
packages, including ``scipy``, ``scikit-learn``, ``tensorflow``,
``yt``, ``cmyt``, ``Pillow``, and ``h5py``. Classes or functions which
generate movies, like the ``o2graph`` command ``mp4``, require the
installation of Blender and ``ffmpeg``.

The ``o2graph`` script created by O₂sclpy sometimes requires modifying
some environment variables to allow O₂sclpy to find the proper OpenMP
library. See the section :ref:`Linking with O₂scl` for more details on
this. On Ubuntu for example, one can address this issue by setting the
environment variable
``O2SCL_ADDL_LIBS=/usr/lib/gcc/x86_64-linux-gnu/13/libgomp.so``.

Because of the complexities of installing O₂scl, O₂sclpy, and all of
the associated dependencies, a Docker tag with a full installation
is provided at
https://hub.docker.com/repository/docker/awsteiner/o2scl/general ,
see e.g. the v0.931_u24.04_py tag for an installation on Ubuntu 24.04.


