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
palette = np.array([[22,1.,36],
                    [15,1.,36],
                    [14,2.,36]
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
palette = np.array([[22,1.,36],
                    [15,1.,36],
                    [14,2.,36]
                    ])

#inputs to function
invader_probabilty = 0.5
number_colours = 3
canvas = da.Canvas(width_x,width_y,colour,border,cutout) 

def generate_random_alien(canvas,invader_probabilty = 0.5, number_colours = 3, tile_ID=1):    
    pattern = canvas
    width_x = canvas[0]
    width_y = canvas[1]
    alien = np.random.randint(1,7, size=(int(width_x/2),width_y))
    alien = np.asarray(alien,float)
    alien_mirror = np.array(np.flipud(alien))
    combined_alien = np.vstack((alien,alien_mirror))
    # set shape
    pattern[8][0] = combined_alien
    pattern[8][0][pattern[8][0]<=3]=0
    pattern[8][0][pattern[8][0]>3]=1
    #set tile ID
    pattern[8][1] = combined_alien
    pattern[8][1][pattern[8][1]<=3]=0
    pattern[8][1][pattern[8][1]==4]=tile_ID
    pattern[8][1][pattern[8][1]==5]=tile_ID+1
    pattern[8][1][pattern[8][1]==6]=tile_ID+2
    pattern[9]=tile_ID+3

    return pattern
    
canvas = da.Canvas(width_x*width_y*2,width_x*width_y*2,colour,border,cutout)
pattern_list = []
tile_ID=1
i=0
while i < width_x*2*width_y*2:
    alien_canvas = da.Canvas(width_x,width_y,colour,border,cutout)
    result = generate_random_alien(alien_canvas,invader_probabilty = 0.5, number_colours = 3, tile_ID=tile_ID)
    #check if meets interest critera
    #print(np.sum(result[8][0],axis=0),np.sum(result[8][0],axis=1))
    if len(np.unique(result[8][1])) < 4:
        continue
    elif 0 in np.sum(result[8][0],axis=0):
        continue
    elif 0 in np.sum(result[8][0],axis=1):
        continue
    else:
        tile_ID =result[9]
        pattern_list.append(result)
    i = len(pattern_list)
    
canvas = da.Spiral_Pattern_List(canvas,canvas_seed,pattern_list,direction=1,rotate=0,tile_ID = 1)

palette = np.array([[1,1.,36],
                    [3,1.,36],
                    [4,1.,36],
                    [10,1.,36],
                    [14,1.,36],
                    [15,1.,36],
                    [25,1.,36],
                    [26,1.,36],
                    [31,1.,36],
                    [85,1.,36],
                    [226,1.,36],
                    [272,1.,36],
                    [288,1.,36],
                    [322,1.,36],
                    [323,1.,36],
                    [326,1.,36],
                    [378,1.,36],
                    [353,1.,36]
                    ])
colour_mode = 'random'
colour_pattern = da.Colour_Pattern(canvas,palette,colour_mode,tiles_check=False)

da.Ldraw_Pattern(canvas,"random space invader patterns" +str(width_x)+ "x" +str(width_y)+ " DOTS",add_steps=True)
