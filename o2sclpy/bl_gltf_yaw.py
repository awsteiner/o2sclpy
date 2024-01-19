# BG_COLOR
# LIGHT_DIST
# LIGHT_ENERGY
# GLTF_PATH
# N_FRAMES
# CAM_DIST
# RES_X
# RES_Y
# BLEND_FILE
# CAMERA_TYPE

import bpy
import os.path
import numpy

# Scene variable
scene=bpy.context.scene

scene.render.resolution_x=RES_X
scene.render.resolution_y=RES_Y

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

# Create five lights in a quincunx
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
light5.location=(0.5,0.5,LIGHT_DIST+0.5)

# Import GLTF file
bpy.ops.import_scene.gltf(filepath='GLTF_PATH')

# Iterate through the dict, set the locations and render
for i in range(0,N_FRAMES):

    ang=numpy.pi*2.0/N_FRAMES*i
    x=CAM_DIST*numpy.cos(ang)
    y=CAM_DIST*numpy.sin(ang)
    
    # Set the camera location
    camera.location=[x+0.5,y+0.5,0.5]
    camera.rotation_euler=[numpy.pi/2.0,0,numpy.pi/2.0+ang]

    if i==0 and BLEND_FILE!='':
        # Save a blend file
        bpy.ops.wm.save_as_mainfile(filepath=BLEND_FILE)
    
    # Assemble the path
    scene.render.filepath='bl_gltf_yaw_%03d.png' % i
    
    # Perform the render
    bpy.ops.render.render(write_still=True)

