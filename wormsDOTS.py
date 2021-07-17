# -*- coding: utf-8 -*-
"""
Created on Sat Jul 17 13:07:36 2021

@author: Stephen
https://github.com/thekitchenscientist/pydotART

Sample programs for the 41935 Set
https://rebrickable.com/sets/41935-1/lots-of-dots/#parts
"""

import pydotART as da

from itertools import combinations_with_replacement
from itertools import permutations, chain
import numpy as np

### Basic Configuration ###
# What tiles are available? [Colour,Shape,Amount]
palette = np.array([[15,1.,36],
                    [15,3.,36],
                    [15,4.,36],
                    [4,1.,36],
                    [4,3.,36],
                    [4,4.,36],
                    [212,2.,36]
                    ])

# Canvas Size and Colour
x=6
y=6
colour=15

# How wide should the untiled border around the edge be?
border=0

# What is the location and size of a central gap [x,y,x_length, y_length]
cutout=np.array([0,0,0,0])

# Where should the tiling start from?
canvas_seed=[0,0]

# Where should the next tile be placed relative to the previous?
translation=np.array([0,0])

width_x = 6
width_y = 6

colour = 15
colour_mode = 'random'
canvas_seed = [0,0]
border=0
cutout=np.array([0,0,0,0])

#inputs to function
max_worm_length = 3
canvas = da.Canvas(width_x,width_y,colour,border,cutout) 
starting_x = 0
starting_y = 0
tile_ID = 1

#generate sequence based on width X and width Y
down_sequence = [1]*width_y
along_sequence = [1]*width_x
down_sequence[0] = along_sequence[0] = 3.0
down_sequence[-1] = along_sequence[-1] = 3.0
    
def generate_worm(canvas,starting_y = 0,max_worm_length=1000,tile_ID=1):
    
    pattern = canvas
    width_x = canvas[0]
    width_y = canvas[1]
    sequence = [1]*width_x
    sequence[0] = sequence[-1] = 3.0
    worm_length = 0

    #check can start
    for i in range(0,width_y):
        if starting_y >= width_y:
            #print('no space')
            return pattern
        slice_y = pattern[8][0][:,starting_y]
        if np.sum(slice_y) == 0:
                break
        elif starting_y < width_y:
            starting_y += 1

    current_xy= [0,starting_y]
        
    #loop over all rows
    for k in range (0,canvas[1]):
        if worm_length >= max_worm_length:
            break
        if worm_length < max_worm_length:    
            for tile_shape in sequence:
                #need to choose to add .2/.8 or .4/.6 to tile on start
                tile_modifier = 0.0
                if current_xy[0] == 0:
                    tile_modifier =  0.4
                elif current_xy[0] == width_x-1:
                    tile_modifier =  0.8

                if worm_length == 0:
                    pattern[8][0][current_xy[0]][current_xy[1]] = 4.2
                else:
                    pattern[8][0][current_xy[0]][current_xy[1]] = tile_shape + tile_modifier
                pattern[8][1][current_xy[0]][current_xy[1]] = tile_ID
                worm_length+=1
                if worm_length >= max_worm_length:
                    if current_xy[0] == 0:
                        tile_modifier =  0.8
                    else:
                        tile_modifier =  0.6                    
                    pattern[8][0][current_xy[0]][current_xy[1]] = 4 + tile_modifier
                    break
                current_xy[0]+=1
            
            # next row
            current_xy[1]+=1

            if current_xy[0] >= width_x:
                current_xy[0]=width_x-1
        if worm_length >= max_worm_length or current_xy[0] < 0  or current_xy[1] < 0 or current_xy[0] >=width_x  or current_xy[1] >=width_y:
            break
   
        #carry on back
        if worm_length < max_worm_length:
            for tile_shape in reversed(sequence):
                
                tile_modifier = 0.0
                if current_xy[0] == 0:
                    tile_modifier =  0.2
                elif current_xy[0] == width_x-1:
                    tile_modifier =  0.6
                pattern[8][0][current_xy[0]][current_xy[1]] = tile_shape + tile_modifier
                pattern[8][1][current_xy[0]][current_xy[1]] = tile_ID
                worm_length+=1
                if worm_length >= max_worm_length:
                    if current_xy[0] == width_x-1:
                        tile_modifier =  0.8
                    else:
                        tile_modifier =  0.2                        
                    pattern[8][0][current_xy[0]][current_xy[1]] = 4 + tile_modifier
                    break
                current_xy[0]-=1
                
            # next row
            current_xy[1]+=1

            if current_xy[0] < 0:
                current_xy[0]=0

        if worm_length >= max_worm_length or current_xy[0] < 0  or current_xy[1] < 0 or current_xy[0] >=width_x  or current_xy[1] >=width_y:
            break
    pattern[9] =  tile_ID               
    return pattern


#loop here to keep starting worms till no space left
#increment tile_ID each time
def fill_with_worms(worm_canvas,starting_y,max_worm_length,tile_ID):
    for j in range (0,width_y):
        worm_canvas = generate_worm(worm_canvas,starting_y=j,max_worm_length=max_worm_length,tile_ID=tile_ID)
        tile_ID =worm_canvas[9]
        tile_ID +=1
    #fill in remainder with circles
    worm_canvas[8][0][np.where(worm_canvas[8][0]==0)]=2
    worm_canvas[8][1][np.where(worm_canvas[8][1]==0)]=tile_ID
    return worm_canvas

def fill_with_worm(worm_canvas,starting_y,max_worm_length,tile_ID):
    worm_canvas = generate_worm(worm_canvas,starting_y=0,max_worm_length=max_worm_length,tile_ID=tile_ID)
    tile_ID =worm_canvas[9]
    tile_ID +=1
    #fill in remainder with circles
    worm_canvas[8][0][np.where(worm_canvas[8][0]==0)]=2
    worm_canvas[8][1][np.where(worm_canvas[8][1]==0)]=tile_ID
    return worm_canvas

canvas = da.Canvas(width_x*width_y,width_x*width_y,colour,border,cutout)
pattern_list = []
for i in range(width_x,width_x*width_y+1): 
    worm_canvas = da.Canvas(width_x,width_y,colour,border,cutout)
    starting_y = 0
    result = fill_with_worms(worm_canvas,starting_y,i,tile_ID)
    tile_ID =result[9]
    tile_ID +=1
    pattern_list.append(result)
    
canvas = da.Spiral_Pattern_List(canvas,canvas_seed,pattern_list,direction=1,rotate=0,tile_ID = 1)

palette = np.array([[22,1.,36],
                    [15,1.,36],
                    [14,2.,36]
                    ])
colour_mode = 'sequence'
colour_pattern = da.Colour_Pattern(canvas,palette,colour_mode,tiles_check=False)

da.Ldraw_Pattern(canvas,"unique worms patterns" +str(width_x)+ "x" +str(width_y)+ " DOTS",add_steps=True)