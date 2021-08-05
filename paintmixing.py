# -*- coding: utf-8 -*-
"""
Created on Thurs Aug 05 13:07:36 2021

@author: Stephen
https://github.com/thekitchenscientist/pydotART

Sample programs for the 41935 Set
https://rebrickable.com/sets/41935-1/lots-of-dots/#parts
"""

import pydotART as da
import numpy as np

### Basic Configuration ###
# What tiles are available? [Colour,Shape,Amount]
palette = np.array([[14,1.,36],
                    [14,3.,36],
                    [14,4.,36],
                    [22,1.,36],
                    [22,3.,36],
                    [22,4.,36],
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

colour_mode = 'alternating'

canvas = da.Canvas(x,y,colour,border,cutout)

def Paint_Mixing(canvas,mixing_border = 0.5, mixing_amount = 0.2, tile_ID = 1):
    x = canvas[0]
    y = canvas[1]
    change_over = int(round(y*mixing_border)-1)
    #set up canvas
    canvas[8][0] = 1
    for i in range(0,y):
        if i<=change_over:
            canvas[8][1][:,i] = tile_ID
        else:
            canvas[8][1][:,i] = tile_ID+1

    #flip colours
    flips_allowed = int(round(x*mixing_amount))
    for i in range(0,y):
        flips_taken = 0
        if i<=change_over:
            colour_ID = tile_ID+1
            trigger = (i+1)/y
            flips_allowed += 1 
        elif i==change_over+1:
            colour_ID = tile_ID
            trigger = i/y
        else:
            colour_ID = tile_ID
            trigger = abs(i-y)/y
            flips_allowed -= 1

        for j in range(0,x):
            if np.random.random_sample() < trigger and flips_taken <= flips_allowed:
                canvas[8][1][j,i] = colour_ID
                flips_taken +=1
            if j == x-1 and flips_taken < flips_allowed:
                j=0

    #extend canvas for search
    extended_canvas = np.zeros((x+2,y+2))
    extended_canvas[1:x+1, 1:y+1] = canvas[8][1]
    extended_canvas[:,0] = extended_canvas[:,1]
    extended_canvas[:,y+1] = extended_canvas[:,y]
    extended_canvas[0,:] = extended_canvas[1,:]
    extended_canvas[x+1,:] = extended_canvas[x,:]

    #tidy shapes
    for i in range(1,y+1):
        for j in range(1,x+1):
            above = extended_canvas[j-1,i]
            infront = extended_canvas[j,i+1]
            below = extended_canvas[j+1,i]
            behind = extended_canvas[j,i-1]
            current = extended_canvas[j,i]
            if infront == behind != current and current == above == below:
                canvas[8][0][j-1,i-1] = 1.0
            elif infront == behind == above == below != current:
                if i<=change_over:
                    canvas[8][0][j-1,i-1] = 4.4
                else:
                    canvas[8][0][j-1,i-1] = 4.8
            elif infront == above != current and current == behind == below:
                canvas[8][0][j-1,i-1] = 3.4
            elif infront == below != current and current == behind == above:
                canvas[8][0][j-1,i-1] = 3.6
            elif behind == above != current and current == infront == below:
                canvas[8][0][j-1,i-1] = 3.2
            elif behind == below != current and current == infront == above:
                canvas[8][0][j-1,i-1] = 3.8
            elif infront == above == below != current and current == behind:
                canvas[8][0][j-1,i-1] = 4.8
            elif behind == above == below != current and current == infront:
                canvas[8][0][j-1,i-1] = 4.4
            elif infront == behind == above != current and current == below:
                canvas[8][0][j-1,i-1] = 4.2
            elif infront == behind == below != current and current == above:
                canvas[8][0][j-1,i-1] = 4.6
    return canvas
    
    
canvas = da.Canvas(x*y,x*y,colour,border,cutout)
mixing_border = 0.5
mixing_amount = 0.2
tile_ID = 1
pattern_list = []
for i in range(0,x*y): 
    paint_canvas = da.Canvas(x,y,colour,border,cutout)
    result = Paint_Mixing(paint_canvas,mixing_border, mixing_amount,tile_ID)
    tile_ID +=2
    pattern_list.append(result)
    
canvas = da.Spiral_Pattern_List(canvas,canvas_seed,pattern_list,direction=1,rotate=0,tile_ID = 1)
colour_pattern = da.Colour_Pattern(canvas,palette,colour_mode,tiles_check=False)
da.Ldraw_Pattern(canvas,"random paint mixing "+str(mixing_border)+ " " +str(mixing_amount)+ " " +str(x)+ "x" +str(y)+ " DOTS",add_steps=True)

"""for y in range(6,15):
    x=6
    mixing_border = 0.5
    mixing_amount = 0.2
    canvas = da.Canvas(x,y,colour,border,cutout)
    canvas = Paint_Mixing(canvas,mixing_border, mixing_amount)
    colour_pattern = da.Colour_Pattern(canvas,palette,colour_mode,tiles_check=False)
    da.Ldraw_Pattern(canvas,"random paint mixing "+str(mixing_border)+ " " +str(mixing_amount)+ " " +str(x)+ "x" +str(y)+ " DOTS",add_steps=True)"""
