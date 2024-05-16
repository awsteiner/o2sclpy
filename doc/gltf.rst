GLTF and Blender integration
============================

:ref:`O2sclpy <o2sclpy>`

O2sclpy can write 3D objects to GLTF files and use Blender to perform
some simple renderings of those 3D objects. 

Internally the limits on the volume rendering are always :math:`[0,1]`
for all three axes. The variables ``xlo``, ``xhi``, ``ylo``, ``yhi``,
``zlo``, and ``zhi`` control the limits of the volume in the "user
coordinate system". These can be set manually or if not, they are set
automatically by the first yt-related command. All commands work on
the user coordinate system by default, and then transform their
arguments to :math:`[0,1]` when necessary.

Blender example
---------------

.. include:: ../examples/bl_yaw_mp4.scr
   :literal:

.. raw:: html
	 
   <video width="512" height="512" controls><source src="https://awsteiner.org/code/o2sclpy/_static/yt_tg_multvol.mp4" type="video/mp4"></video>
           
