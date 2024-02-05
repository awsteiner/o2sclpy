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
# 'PANO', 'PERSP' and 'ORTHO'
camera_data.type='CAMERA_TYPE'
camera=bpy.data.objects.new('camera',camera_data)
scene.collection.objects.link(camera)
camera.rotation_mode='XYZ'

# Set the camera object as the active camera
scene.camera=camera

# Create eight lights, one for each octant
light_data1=bpy.data.lights.new(name='light1', type='POINT')
light_data1.energy=LIGHT_ENERGY
light_data1.shadow_soft_size=0.1
light1=bpy.data.objects.new(name='light1',object_data=light_data1)
light1.location=(LIGHT_DIST+0.5,LIGHT_DIST+0.5,LIGHT_DIST+0.5)
bpy.context.collection.objects.link(light1)

light_data2=bpy.data.lights.new(name='light2', type='POINT')
light_data2.energy=LIGHT_ENERGY
light_data2.shadow_soft_size=0.1
light2=bpy.data.objects.new(name='light2',object_data=light_data2)
light2.location=(LIGHT_DIST+0.5,-LIGHT_DIST+0.5,LIGHT_DIST+0.5)
bpy.context.collection.objects.link(light2)

light_data3=bpy.data.lights.new(name='light3', type='POINT')
light_data3.energy=LIGHT_ENERGY
light_data3.shadow_soft_size=0.1
light3=bpy.data.objects.new(name='light3',object_data=light_data3)
light3.location=(-LIGHT_DIST+0.5,LIGHT_DIST+0.5,LIGHT_DIST+0.5)
bpy.context.collection.objects.link(light3)

light_data4=bpy.data.lights.new(name='light4', type='POINT')
light_data4.energy=LIGHT_ENERGY
light_data4.shadow_soft_size=0.1
light4=bpy.data.objects.new(name='light4',object_data=light_data4)
light4.location=(-LIGHT_DIST+0.5,-LIGHT_DIST+0.5,LIGHT_DIST+0.5)
bpy.context.collection.objects.link(light4)

light_data5=bpy.data.lights.new(name='light5', type='POINT')
light_data5.energy=LIGHT_ENERGY
light_data5.shadow_soft_size=0.1
light5=bpy.data.objects.new(name='light5',object_data=light_data5)
light5.location=(LIGHT_DIST+0.5,LIGHT_DIST+0.5,-LIGHT_DIST+0.5)
bpy.context.collection.objects.link(light5)

light_data6=bpy.data.lights.new(name='light6', type='POINT')
light_data6.energy=LIGHT_ENERGY
light_data6.shadow_soft_size=0.1
light6=bpy.data.objects.new(name='light6',object_data=light_data6)
light6.location=(LIGHT_DIST+0.5,-LIGHT_DIST+0.5,-LIGHT_DIST+0.5)
bpy.context.collection.objects.link(light6)

light_data7=bpy.data.lights.new(name='light7', type='POINT')
light_data7.energy=LIGHT_ENERGY
light_data7.shadow_soft_size=0.1
light7=bpy.data.objects.new(name='light7',object_data=light_data7)
light7.location=(-LIGHT_DIST+0.5,LIGHT_DIST+0.5,-LIGHT_DIST+0.5)
bpy.context.collection.objects.link(light7)

light_data8=bpy.data.lights.new(name='light8', type='POINT')
light_data8.energy=LIGHT_ENERGY
light_data8.shadow_soft_size=0.1
light8=bpy.data.objects.new(name='light8',object_data=light_data8)
light8.location=(-LIGHT_DIST+0.5,-LIGHT_DIST+0.5,-LIGHT_DIST+0.5)
bpy.context.collection.objects.link(light8)

# Import GLTF file
bpy.ops.import_scene.gltf(filepath='GLTF_PATH')

# Set the camera location
camera.location=[CAM_DIST+0.5,0.5,0.5]
camera.rotation_euler=[numpy.pi/2.0,0,numpy.pi/2.0]


