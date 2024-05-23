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
import o2sclpy

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
ctype='CAMERA_TYPE'
if ctype[0:3]=='PE:':
    camera_data.type='PERSP'
    camera_data.lens=float(ctype[3:])
elif ctype[0:3]=='OR:':
    camera_data.type='ORTHO'
    camera_data.ortho_scale=float(ctype[3:])
else:
    camera_data.type=ctype
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

# Spherical r, theta (azimuth), phi coordinates shifted
sphx=[o2sclpy.rect_to_spher([camx[i][0]-0.5,
                             camx[i][1]-0.5,
                             camx[i][2]-0.5]) for i in range(0,6)]

# Euler angles for the rotation at each of the six positions
rotx=[[0,0,0],
      [numpy.pi/2.0,-numpy.pi/2.0,numpy.pi],
      [numpy.pi/2.0,0,numpy.pi/2.0],
      [0,numpy.pi,numpy.pi*3.0/2.0],
      [numpy.pi/2.0,0,0],
      [numpy.pi/2.0,numpy.pi*3.0/2.0,numpy.pi*3.0/2.0]]

if False:
    for i in range(0,6):
        print('sphx',sphx[i])
        print('rotx',rotx[i])

sphx2=[]
rotx2=[]
    
for i in range(0,6):

    for j in range(0,N_SIT):

        sphx2.append(sphx[i])
        rotx2.append(rotx[i])

        print(i,j,sphx[i][0],rotx[i][0])

    half_wid=(float(N_FRAMES)-1)/2.0
    a0=1.0/(1.0+numpy.exp(half_wid))
    a1=1.0/(1.0+numpy.exp(-half_wid))
    
    for j in range(0,N_FRAMES):

        dj=float(j)
        a=1.0/(1.0+numpy.exp(-dj+half_wid))
        
        if i<5:
            sph_temp_x=(sphx[i][0]+(a-a0)/(a1-a0)*
                        (sphx[i+1][0]-sphx[i][0]))
            sph_temp_y=(sphx[i][1]+(a-a0)/(a1-a0)*
                        (sphx[i+1][1]-sphx[i][1]))
            sph_temp_z=(sphx[i][2]+(a-a0)/(a1-a0)*
                        (sphx[i+1][2]-sphx[i][2]))
            rot_temp_x=(rotx[i][0]+(a-a0)/(a1-a0)*
                        (rotx[i+1][0]-rotx[i][0]))
            rot_temp_y=(rotx[i][1]+(a-a0)/(a1-a0)*
                        (rotx[i+1][1]-rotx[i][1]))
            rot_temp_z=(rotx[i][2]+(a-a0)/(a1-a0)*
                        (rotx[i+1][2]-rotx[i][2]))
        else:
            sph_temp_x=(sphx[i][0]+(a-a0)/(a1-a0)*
                        (sphx[0][0]-sphx[i][0]))
            sph_temp_y=(sphx[i][1]+(a-a0)/(a1-a0)*
                        (sphx[0][1]-sphx[i][1]))
            sph_temp_z=(sphx[i][2]+(a-a0)/(a1-a0)*
                        (sphx[0][2]-sphx[i][2]))
            rot_temp_x=(rotx[i][0]+(a-a0)/(a1-a0)*
                        (rotx[0][0]-rotx[i][0]))
            rot_temp_y=(rotx[i][1]+(a-a0)/(a1-a0)*
                        (rotx[0][1]-rotx[i][1]))
            rot_temp_z=(rotx[i][2]+(a-a0)/(a1-a0)*
                        (rotx[0][2]-rotx[i][2]))
            
        print('%2d %2d %7.6e %7.6e %7.6e %7.6e %7.6e' %
              (i,j,a0,dj,a,sph_temp_x,rot_temp_x))
            
        sphx2.append([sph_temp_x,sph_temp_y,sph_temp_z])
        rotx2.append([rot_temp_x,rot_temp_y,rot_temp_z])

# Iterate through the dict, set the locations and render
for i in range(0,6):
    
    # Set the camera location
    camera.location=camx[i]
    camera.rotation_euler=rotx[i]

    # Assemble the path
    scene.render.filepath='bl_gltf_six_temp_%03d.png' % i
    
    # Perform the render
    bpy.ops.render.render(write_still=True)

    if True:
        # Save a blend file
        bpy.ops.wm.save_as_mainfile(filepath=
                                    ('/home/awsteiner/six_temp_%01d.blend' % i))

# Iterate through the dict, set the locations and render
for i in range(0,len(sphx2)):

    camx2=o2sclpy.spher_to_rect(sphx2[i])
        
    # Set the camera location
    camera.location=[camx2[0]+0.5,camx2[1]+0.5,camx2[2]+0.5]
    camera.rotation_euler=rotx2[i]

    if i==0 and 'BLEND_FILE'!='':
        # Save a blend file
        bpy.ops.wm.save_as_mainfile(filepath='BLEND_FILE')
        
    # Assemble the path
    scene.render.filepath='bl_gltf_six_%03d.png' % i
    
    # Perform the render
    bpy.ops.render.render(write_still=True)

    if i<15:
        # Save a blend file
        bpy.ops.wm.save_as_mainfile(filepath=
                                    ('/home/awsteiner/six_%03d.blend' % i))

