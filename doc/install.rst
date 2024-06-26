.. _install:

Installation and Requirements
=============================

:ref:`O2sclpy <o2sclpy>`

O₂sclpy requires an installation of the development version of O₂scl.
The release version, O₂sclpy 0.929, requires the O₂scl v0.929 release
from https://github.com/awsteiner/o2scl/releases/tag/v0.929 .

.. and the
   development version, O₂sclpy 0.929a1, requires that the most recent
   version of O₂scl from the master branch on github is installed on your
   machine.

The most recent release version of O₂sclpy can be installed with e.g.
``pip3 install o2sclpy``.

.. If you want to install the development
   version (v0.929a1), you can clone the git repository, change directory
   to the O₂sclpy directory, and then use e.g. ``pip3 install .`` if you
   want to use the pip package manager or ``python3 setup.py install`` to
   do a direct installation.

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
``yt``, ``cmyt``, ``Pillow``, ``h5py``, and ``bpy`` (from Blender).
Classes or functions which generate movies, like the ``o2graph``
command ``mp4``, require the installation of ``ffmpeg``.

