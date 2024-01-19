# BG_COLOR
# LIGHT_DIST
# LIGHT_ENERGY
# GLTF_PATH
# N_FRAMES
# CAM_DIST

import bpy
import os.path
import numpy

# Scene variable
scene=bpy.context.scene

scene.render.resolution_x=1024
scene.render.resolution_y=1024
#print(scene.render.resolution_x,
#      scene.render.resolution_y)

# Delete default objects
for o in scene.objects:
    o.select_set(True)
    print('Deleting default object named "'+o.name+'".')
    bpy.ops.object.delete()

# Set world background to black
scene.world.node_tree.nodes["Background"].inputs[0].default_value=BG_COLOR

# Create camera
camera_data=bpy.data.cameras.new(name='camera')
# 'PANO', 'PERSP' and 'ORTHO'
#print(camera_data.type)
camera_data.type='ORTHO'
camera_data.ortho_scale=2.0
camera=bpy.data.objects.new('camera',camera_data)
scene.collection.objects.link(camera)
camera.rotation_mode='XYZ'

# Set the camera object as the active camera
scene.camera=camera

# Create eight lights, one for each octant
light_data1=bpy.data.lights.new(name='light1', type='POINT')
light_data1.energy=LIGHT_ENERGY
light1=bpy.data.objects.new(name='light1',object_data=light_data1)
bpy.context.collection.objects.link(light1)
light1.location=(LIGHT_DIST+0.5,LIGHT_DIST+0.5,LIGHT_DIST+0.5)

light_data2=bpy.data.lights.new(name='light2', type='POINT')
light_data2.energy=LIGHT_ENERGY
light2=bpy.data.objects.new(name='light2',object_data=light_data2)
bpy.context.collection.objects.link(light2)
light2.location=(LIGHT_DIST+0.5,-LIGHT_DIST+0.5,LIGHT_DIST+0.5)

light_data3=bpy.data.lights.new(name='light3', type='POINT')
light_data3.energy=LIGHT_ENERGY
light3=bpy.data.objects.new(name='light3',object_data=light_data3)
bpy.context.collection.objects.link(light3)
light3.location=(-LIGHT_DIST+0.5,LIGHT_DIST+0.5,LIGHT_DIST+0.5)

light_data4=bpy.data.lights.new(name='light4', type='POINT')
light_data4.energy=LIGHT_ENERGY
light4=bpy.data.objects.new(name='light4',object_data=light_data4)
bpy.context.collection.objects.link(light4)
light4.location=(-LIGHT_DIST+0.5,-LIGHT_DIST+0.5,LIGHT_DIST+0.5)

light_data5=bpy.data.lights.new(name='light5', type='POINT')
light_data5.energy=LIGHT_ENERGY
light5=bpy.data.objects.new(name='light5',object_data=light_data5)
bpy.context.collection.objects.link(light5)
light5.location=(LIGHT_DIST+0.5,LIGHT_DIST+0.5,-LIGHT_DIST+0.5)

light_data6=bpy.data.lights.new(name='light6', type='POINT')
light_data6.energy=LIGHT_ENERGY
light6=bpy.data.objects.new(name='light6',object_data=light_data6)
bpy.context.collection.objects.link(light6)
light6.location=(LIGHT_DIST+0.5,-LIGHT_DIST+0.5,-LIGHT_DIST+0.5)

light_data7=bpy.data.lights.new(name='light7', type='POINT')
light_data7.energy=LIGHT_ENERGY
light7=bpy.data.objects.new(name='light7',object_data=light_data7)
bpy.context.collection.objects.link(light7)
light7.location=(-LIGHT_DIST+0.5,LIGHT_DIST+0.5,-LIGHT_DIST+0.5)

light_data8=bpy.data.lights.new(name='light8', type='POINT')
light_data8.energy=LIGHT_ENERGY
light8=bpy.data.objects.new(name='light8',object_data=light_data8)
bpy.context.collection.objects.link(light8)
light8.location=(-LIGHT_DIST+0.5,-LIGHT_DIST+0.5,-LIGHT_DIST+0.5)

# Import GLTF file
bpy.ops.import_scene.gltf(filepath='GLTF_PATH')

# xy, zx, yz, yx, xz, and zy, in that order

camx=[[0.5,0.5,CAM_DIST+0.5],
      [0.5,CAM_DIST+0.5,0.5],
      [CAM_DIST+0.5,0.5,0.5],
      [0.5,0.5,-CAM_DIST+0.5],
      [0.5,-CAM_DIST+0.5,0.5],
      [-CAM_DIST+0.5,0.5,0.5]]

rotx=[[0,0,0],
      [numpy.pi/2.0,numpy.pi*3.0/2.0,numpy.pi],
      [numpy.pi/2.0,0,numpy.pi/2.0],
      [0,numpy.pi,numpy.pi*3.0/2.0],
      [numpy.pi/2.0,0,0],
      [numpy.pi/2.0,numpy.pi*3.0/2.0,numpy.pi*3.0/2.0]]

# Iterate through the dict, set the locations and render
for i in range(0,6):
    
    # Set the camera location
    camera.location=camx[i]
    camera.rotation_euler=rotx[i]

    # Assemble the path
    scene.render.filepath='bl_gltf_six_%01d.png' % i
    
    # Perform the render
    bpy.ops.render.render(write_still=True)

    # Save a blend file
    bpy.ops.wm.save_as_mainfile(filepath=
                                ('/Users/awsteiner2/six_%01d.blend' % i))

