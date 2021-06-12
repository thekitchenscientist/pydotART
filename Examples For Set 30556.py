# -*- coding: utf-8 -*-
"""
Created on Sat Jun 12 13:07:36 2021

@author: Stephen
https://github.com/thekitchenscientist/pydotART

Sample programs for the 30556 Set
https://rebrickable.com/sets/30556-1/mini-frame/?inventory=1#alt_builds
"""

import pydotART as da

from itertools import combinations_with_replacement
from itertools import permutations, chain
import numpy as np

### Basic Configuration ###
# What tiles are available? [Colour,Shape,Amount]
palette = np.array([[5,3.,16],
                    [323,3.,16],
                    [31,3.,16],
                    [29,2.,8],
                    [14,2.,4],
                    ])
# use with seaborn to get nicer pictures, comment out if exporting to LDraw
palette = np.array([[1,3.,16],
                    [2,3.,16],
                    [3,3.,16],
                    [4,2.,8],
                    [5,2.,4],
                    ])
# Canvas Size and Colour
x=8
y=8
colour=272

# How wide should the untiled border around the edge be?
border=0

# What is the location and size of a central gap [x,y,x_length, y_length]
cutout=np.array([3,3,4,4])

# Where should the tiling start from?
canvas_seed=[0,0]

# Where should the next tile be placed relative to the previous?
translation=np.array([0,0])


## Circles Frame From Polybag ##
canvas = da.Canvas(x,y,colour,border,cutout) 
tile_pattern = da.Spiral_Pattern(canvas,[0,0],da.pattern_dict["circle"],rotate=0)

reduced_palette = palette[np.where(palette[:,1]==3)]
colour_pattern = da.Colour_Pattern(tile_pattern,reduced_palette,colour_mode = 'sequence',tiles_check=True)
count_tiles = da.Count_Tiles(colour_pattern,reduced_palette)
da.Plot_Pattern(colour_pattern)
#da.Ldraw_Pattern(colour_pattern,"Cicles")

## Knots and Dots Frame From Polybag ## 
canvas = da.Canvas(x,y,colour,border,cutout)  
translation = [1,1]
tile_pattern = da.Tile_Pattern(canvas,[0,0],da.pattern_dict["leaf"],translation,fill=False,wrap=False)
tile_pattern = da.Tile_Pattern(canvas,[3,0],da.pattern_dict["leaf"],translation,fill=False,wrap=True,tile_ID=tile_pattern[9])
tile_pattern = da.Tile_Pattern(canvas,[5,0],da.pattern_dict["leaf"],translation,fill=False,wrap=True,tile_ID=tile_pattern[9])
tile_pattern = da.Tile_Pattern(canvas,[2,0],da.pattern_dict["dot"],translation,fill=False,wrap=False,tile_ID=tile_pattern[9])
tile_pattern = da.Tile_Pattern(canvas,[0,1],da.pattern_dict["dot"],translation,fill=False,wrap=False,tile_ID=tile_pattern[9])
tile_pattern = da.Tile_Pattern(canvas,[7,0],da.pattern_dict["leaf"],translation,fill=False,wrap=True,tile_ID=tile_pattern[9])
tile_pattern = da.Tile_Pattern(canvas,[-1,6],da.pattern_dict["leaf"],translation,fill=False,wrap=True,tile_ID=tile_pattern[9])

colour_pattern = da.Colour_Pattern(tile_pattern,palette,colour_mode = 'pass')
count_tiles = da.Count_Tiles(colour_pattern,palette)
da.Plot_Pattern(colour_pattern)
#da.Ldraw_Pattern(colour_pattern,"Knots and Dots")



## Mirrored X Y ##
translation = [0,0]
chosen_pattern = da.pattern_dict["tulip"]
width_x = len(chosen_pattern[:,0])
width_y = len(chosen_pattern[0,:])
canvas = da.Canvas(x,y,colour,border,cutout)

for i in range(0,int(x/width_x),width_x):
    for j in range(0,int(y/width_y),width_y):
            
        if i ==0 and j == 0:
            tile_ID=1
    
        canvas_seed = [i,j]
        tile_pattern = da.Tile_Pattern(canvas,canvas_seed,chosen_pattern,translation=[0,0],fill=False,wrap=False,rotate=0,tile_ID=tile_ID)
        canvas = tile_pattern
        tile_ID=tile_pattern[9]

tile_pattern = da.Mirror_Pattern(tile_pattern,mode=["X","Y"])
colour_pattern = da.Colour_Pattern(tile_pattern,palette,colour_mode = 'pass')
count_tiles = da.Count_Tiles(colour_pattern,palette)
da.Plot_Pattern(colour_pattern)
#da.Ldraw_Pattern(colour_pattern,"Mirrored Tulips")


## Knots Frame ## 
canvas = da.Canvas(x,y,colour,border,cutout) 
tile_pattern = da.Tile_Pattern(canvas,[0,0],da.pattern_dict["leaf"],translation,fill=True,wrap=True)
colour_pattern = da.Colour_Pattern(tile_pattern,palette,colour_mode = 'pass')
count_tiles = da.Count_Tiles(colour_pattern,palette)
da.Plot_Pattern(colour_pattern)
#da.Ldraw_Pattern(colour_pattern,"Knots")


## Scales Frame ##
canvas = da.Canvas(x,y,colour,border,cutout) 
for i in range(0,canvas[0]):
    
    if i ==0:
        tile_ID=1
    
    if i % 2 == 0:
        canvas_seed = [i,0]
    else:        
        canvas_seed = [i,1]
    tile_pattern = da.Tile_Pattern(canvas,canvas_seed,da.pattern_dict["scale"],translation=[0,2],fill=False,wrap=False,rotate=0,tile_ID=tile_ID)
    tile_ID=tile_pattern[9]

reduced_palette = palette[np.where(palette[:,1]==3)]
colour_pattern = da.Colour_Pattern(tile_pattern,reduced_palette,colour_mode = 'pass',tiles_check=True)
count_tiles = da.Count_Tiles(colour_pattern,reduced_palette)
da.Plot_Pattern(colour_pattern)
#da.Ldraw_Pattern(colour_pattern,"Scales")

