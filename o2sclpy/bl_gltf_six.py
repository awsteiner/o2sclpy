# BG_COLOR
# LIGHT_DIST
# LIGHT_ENERGY
# CAMERA_TYPE
# CAM_DIST
# ORTHO_SCALE
# RES_X
# RES_Y
# N_FRAMES
# N_SIT
# GLTF_PATH
# BLEND_FILE

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
camera_data.type='CAMERA_TYPE'
camera_data.ortho_scale=ORTHO_SCALE
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
bpy.context.collection.objects.link(light1)
light1.location=(LIGHT_DIST+0.5,LIGHT_DIST+0.5,LIGHT_DIST+0.5)

light_data2=bpy.data.lights.new(name='light2', type='POINT')
light_data2.energy=LIGHT_ENERGY
light_data2.shadow_soft_size=0.1
light2=bpy.data.objects.new(name='light2',object_data=light_data2)
bpy.context.collection.objects.link(light2)
light2.location=(LIGHT_DIST+0.5,-LIGHT_DIST+0.5,LIGHT_DIST+0.5)

light_data3=bpy.data.lights.new(name='light3', type='POINT')
light_data3.energy=LIGHT_ENERGY
light_data3.shadow_soft_size=0.1
light3=bpy.data.objects.new(name='light3',object_data=light_data3)
bpy.context.collection.objects.link(light3)
light3.location=(-LIGHT_DIST+0.5,LIGHT_DIST+0.5,LIGHT_DIST+0.5)

light_data4=bpy.data.lights.new(name='light4', type='POINT')
light_data4.energy=LIGHT_ENERGY
light_data4.shadow_soft_size=0.1
light4=bpy.data.objects.new(name='light4',object_data=light_data4)
bpy.context.collection.objects.link(light4)
light4.location=(-LIGHT_DIST+0.5,-LIGHT_DIST+0.5,LIGHT_DIST+0.5)

light_data5=bpy.data.lights.new(name='light5', type='POINT')
light_data5.energy=LIGHT_ENERGY
light_data5.shadow_soft_size=0.1
light5=bpy.data.objects.new(name='light5',object_data=light_data5)
bpy.context.collection.objects.link(light5)
light5.location=(LIGHT_DIST+0.5,LIGHT_DIST+0.5,-LIGHT_DIST+0.5)

light_data6=bpy.data.lights.new(name='light6', type='POINT')
light_data6.energy=LIGHT_ENERGY
light_data6.shadow_soft_size=0.1
light6=bpy.data.objects.new(name='light6',object_data=light_data6)
bpy.context.collection.objects.link(light6)
light6.location=(LIGHT_DIST+0.5,-LIGHT_DIST+0.5,-LIGHT_DIST+0.5)

light_data7=bpy.data.lights.new(name='light7', type='POINT')
light_data7.energy=LIGHT_ENERGY
light_data7.shadow_soft_size=0.1
light7=bpy.data.objects.new(name='light7',object_data=light_data7)
bpy.context.collection.objects.link(light7)
light7.location=(-LIGHT_DIST+0.5,LIGHT_DIST+0.5,-LIGHT_DIST+0.5)

light_data8=bpy.data.lights.new(name='light8', type='POINT')
light_data8.energy=LIGHT_ENERGY
light_data8.shadow_soft_size=0.1
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

# Spherical r, theta (azimuth), phi coordinates
sphx=[[CAM_DIST,numpy.pi/2.0,0],
      [CAM_DIST,0,3.0*numpy.pi/2.0],
      [CAM_DIST,0,0.0]]

for k in range(0,3):
    rt=sphx[k][0]
    thetat=sphx[k][1]
    phit=sphx[k][2]
    xt=rt*numpy.cos(thetat)*numpy.sin(phit)
    yt=rt*numpy.sin(thetat)*numpy.sin(phit)
    zt=rt*numpy.cos(phit)
    print(camx[k][0],xt+0.5)
    print(camx[k][1],yt+0.5)
    print(camx[k][2],zt+0.5)

rotx=[[0,0,0],
      [numpy.pi/2.0,numpy.pi*3.0/2.0,numpy.pi],
      [numpy.pi/2.0,0,numpy.pi/2.0],
      [0,numpy.pi,numpy.pi*3.0/2.0],
      [numpy.pi/2.0,0,0],
      [numpy.pi/2.0,numpy.pi*3.0/2.0,numpy.pi*3.0/2.0]]

for i in range(0,6):

    for j in range(0,N_SIT):

        camx2.append(camx[i])
        rotx2.append(rotx[i])

        print(i,j,camx[i][0],rotx[i][0])

    half_wid=(float(N_FRAMES)-1)/2.0
    a0=1.0/(1.0+numpy.exp(half_wid))
    a1=1.0/(1.0+numpy.exp(-half_wid))
    
    for j in range(0,N_FRAMES):

        dj=float(j)/(float(N_FRAMES)-1)
        a=1.0/(1.0+numpy.exp(-dj+half_wid))
        
        if i<5:
            cam_temp_x=(camx[i][0]+(a-a0)*(a1-a0)*
                        camx[i+1][0])
            cam_temp_y=(camx[i][1]+(a-a0)*(a1-a0)*
                        camx[i+1][1])
            cam_temp_z=(camx[i][2]+(a-a0)*(a1-a0)*
                        camx[i+1][2])
            rot_temp_x=(rotx[i][0]+(a-a0)*(a1-a0)*
                        rotx[i+1][0])
            rot_temp_y=(rotx[i][1]+(a-a0)*(a1-a0)*
                        rotx[i+1][1])
            rot_temp_z=(rotx[i][2]+(a-a0)*(a1-a0)*
                        rotx[i+1][2])
        else:
            cam_temp_x=(camx[i][0]+(a-a0)*(a1-a0)*
                        camx[0][0])
            cam_temp_y=(camx[i][1]+(a-a0)*(a1-a0)*
                        camx[0][1])
            cam_temp_z=(camx[i][2]+(a-a0)*(a1-a0)*
                        camx[0][2])
            rot_temp_x=(rotx[i][0]+(a-a0)*(a1-a0)*
                        rotx[0][0])
            rot_temp_y=(rotx[i][1]+(a-a0)*(a1-a0)*
                        rotx[0][1])
            rot_temp_z=(rotx[i][2]+(a-a0)*(a1-a0)*
                        rotx[0][2])
        print(i,j,a0,dj,a1,cam_temp_x,rot_temp_x)
            
        camx2.append([cam_temp_x,cam_temp_y,cam_temp_z])
        rotx2.append([rot_temp_x,rot_temp_y,rot_temp_z])

# Iterate through the dict, set the locations and render
for i in range(0,6):
    
    # Set the camera location
    camera.location=camx[i]
    camera.rotation_euler=rotx[i]

    if i==0 and 'BLEND_FILE'!='':
        # Save a blend file
        bpy.ops.wm.save_as_mainfile(filepath='BLEND_FILE')
        
    # Assemble the path
    scene.render.filepath='bl_gltf_six_%03d.png' % i
    
    # Perform the render
    bpy.ops.render.render(write_still=True)

    # Save a blend file
    bpy.ops.wm.save_as_mainfile(filepath=
                                ('/Users/awsteiner2/six_%01d.blend' % i))

