# BG_COLOR
# LIGHT_DIST
# LIGHT_ENERGY
# GLTF_PATH
# CAM_DIST
# CAMERA_TYPE

import bpy
import os.path
import numpy

# Scene variable
scene=bpy.context.scene

# Delete default objects
for o in scene.objects:
    o.select_set(True)
    print('Deleting default object named "'+o.name+'".')
    bpy.ops.object.delete()

# Set world background to black
scene.world.node_tree.nodes["Background"].inputs[0].default_value=BG_COLOR

# Create camera
camera_data=bpy.data.cameras.new(name='camera')
if CAMERA_TYPE!='':
    # 'PANO', 'PERSP' and 'ORTHO'
    camera_data.type=CAMERA_TYPE
camera=bpy.data.objects.new('camera',camera_data)
scene.collection.objects.link(camera)
camera.rotation_mode='XYZ'

# Set the camera object as the active camera
scene.camera=camera

# Create one light
light_data1=bpy.data.lights.new(name='light1', type='POINT')
light_data1.energy=LIGHT_ENERGY
light1=bpy.data.objects.new(name='light1',object_data=light_data1)
bpy.context.collection.objects.link(light1)
light1.location=(LIGHT_DIST+0.5,LIGHT_DIST+0.5,LIGHT_DIST+0.5)

# Import GLTF file
bpy.ops.import_scene.gltf(filepath='GLTF_PATH')

# Set the camera location
camera.location=[CAM_DIST+0.5,0.5,0.5]
camera.rotation_euler=[numpy.pi/2.0,0,numpy.pi/2.0]


