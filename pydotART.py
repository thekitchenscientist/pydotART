# -*- coding: utf-8 -*-
"""
Created on Wed May 26 19:49:15 2021

@author: Stephen Pearson
"""

import numpy as np
import seaborn as sb


## tile dictionary ##
tile_dict = {0:" ",
             1:"■",
        2:"○",
        3:"◔",
        3.1:"◢",
        3.2:"◣",
        3.3:"◸",
        3.4:"◹",
        4:"◖",
        4.1:"C",
        4.2:"∩",
        4.3:"D",
        4.4:"U",
        5:"☆",
        6:"♡"}

## pre-programmed patterns based on DOTS packaging##
pattern = {
   "dot" : np.array([[2]]),

"knot" : np.array([[3.2],
                 [3.4]]),

"left_circle" : np.array([[3.1],
                        [3.4]]),

"right_circle" : np.array([[3.2],
                         [3.3]]),

"circle" : np.array([[3.1,3.2],
                        [3.4,3.3]
                        ]),
"windmill" : np.array([[3.4,3.1],
                        [3.3,3.2]
                        ]),

"fish" : np.array([[3.1,3.2],
                        [3.3,3.4]
                        ]),

"butterfly" : np.array([[3.2,3.1],
                        [3.3,3.4]
                        ]) 
    }

### Configuration ###
# What tiles are avaiable [Colour,Shape,Amount]
palette = np.array([[1,3.,16],
                    [2,3.,16],
                    [3,3.,16],
                    [4,2.,8],
                    [5,2.,4],
                    ])

# Canvas Size and Colour
x=8
y=8
colour=1

# How wide should the untiled border around the edge be?
border=0

# What is the location and size of a central gap [x,y,x_length, y_length]
cutout=np.array([0,0,0,0])

# Where should the tiling start from?
canvas_seed=[0,0]

# Where should the next tile be placed relative to the previous?
translation=np.array([0,0])





### Functions ###
"""
The aim of this function is to encode the configuration, check the combinations
are viable and create the canvas [tile shapes, tile_ID, tile_colour, tile orientation]

"""
def Canvas(x,y,colour=1,border=0,cutout=np.array([0,0,0,0])):
    # check border is not too big
    if border > 0 and (x-2*border < 2 or y-2*border < 2):
        print('Border is too large please choose a smaller value')
        return
    # resize canvas
    x = x - 2 * border
    y = y - 2 * border
    
    # check cutout is not too big
    if cutout[2] > x-2 or cutout[3] > y-2:
        print('Cut out is too large please choose a smaller value')
        return
    
    return([x,y,colour,border,cutout[0]-1,cutout[1]-1,cutout[2],cutout[3],np.zeros((3,x,y)),0])
    

"""
The aim of this function is to check their are enough tiles
"""
def Tile_Check(canvas,canvas_seed,palette,pattern,translation):
    
    
    tesselation = np.floor(pattern)
    # count the available tiles
    tiles = palette[:,2].sum()
    # count the available studs
    studs = canvas[0]*canvas[1] - canvas[6]*canvas[7]
    # if tiles > studs:
    #     return
    tiles_percent = len(np.where(tesselation>0)[0])/tesselation.size
    if tiles*tiles_percent < studs:
        print('Not enough tiles to cover canvas')
    # check next by group and update palette if tiles not used
    # shapes_required = np.unique(tesselation)
    # update_to_palette = np.where(np.in1d(palette[:,1],shapes_required))
    # palette = palette[update_to_palette,:][0]
    # return palette

"""
The aim of this function is to place the tiles for one pass across the canvas
"""
def Pattern(canvas,starting_x,starting_y,pattern,translation,tile_ID,wrap=True):

    x = canvas[0]
    y = canvas[1]
    current_x = starting_x
    current_y = starting_y
    current_solution = canvas[8][0]
    current_positions = canvas[8][1]
    tesselation = np.floor(pattern)

    #iterative over cells, then tiling pattern filling in the grid
    for i in range(0,int(x*y/len(tesselation[0:]))):
        #don't start if there is no room
        if i ==0:
            if current_x+1 <= x-1 and current_positions[current_x+1][current_y] > 0 and len(tesselation[0:])>1:
                print('cant start')
                break
        
        for j in range(0,len(tesselation[0:])):
            if current_y > y-1:
                #print('y')
                break
            for k in range(0,len(tesselation[0])):
                if current_x+j > x-1 and tesselation[j][k] == 0:
                    #print('x')
                    break
                if current_x+j > x-1 and wrap:
                    current_x = 0-j
                    current_y = current_y-k
                    if k>0:
                        current_y += 1
                    #print([current_x,current_y])
                if current_x+j < 0 or current_y+k < 0:
                    #print('outside canvas')
                    continue
                try:
                    if current_positions[current_x+j][current_y+k] > 0:
                        #print('taken')
                        break
                    current_solution[current_x+j][current_y+k] = pattern[j][k]
                    current_positions[current_x+j][current_y+k] = tile_ID                    
                except:
                    print([i,j,k,current_x+j,current_y+k,tesselation[j][k]])
        tile_ID += 1
        current_x += translation[0]           
        current_y += translation[1]
        #stop at edge of canvas
        if current_x == x and current_y == y:
            #print('end')
            break
        
    #remove cut out if specified
    if canvas[6] > 0:
        starting_mask = np.ones((x,y))
        current_x = canvas[4]
        current_y = canvas[5]
        for i in range(0,canvas[6]):
            for j in range(0,canvas[7]):
                starting_mask[current_x+i][current_y+j]=np.NaN
         
        output_solution = np.multiply(current_solution,starting_mask)
    else:
        output_solution = current_solution

    return([output_solution,current_positions,tile_ID])

"""
The aim of this function is to control the tiling passes across the canvas and
return the output pattern
""" 
def Tile_Pattern(canvas,canvas_seed,pattern,translation,fill=True,wrap=True,tile_ID = 1):
    offset_x = canvas_seed[0]
    offset_y = canvas_seed[1]
    tesselation = np.floor(pattern)
    width_x = len(tesselation[:,0])
    width_y = len(tesselation[0,:])

    if fill:
        extent_x = round(x/len(tesselation[:,0]))
        extent_y = round(y/len(tesselation[0,:]))
    else:   
        extent_x = 1
        extent_y = 1
            
    for i in range(0,extent_x):
        for j in range(0,extent_y):                       
            result = Pattern(canvas,offset_x+i*width_x,offset_y+j*width_y,pattern,translation,tile_ID,wrap)
            canvas[8][0] = result[0].copy()
            canvas[8][1] = result[1].copy()
            tile_ID = result[2]      
            if translation[1] > 0 and j > 0:
                break
    canvas[9] =  tile_ID  
    return canvas

"""
The aim of this function is to set the tile colours
colour_mode = 'alternating'
colour_mode = 'sequence'
colour_mode = 'random'
colour_mode = 'pass'
""" 
def Colour_Pattern(tile_pattern,palette,colour_mode):
    colour_seed = 1
    palette_position = 0
    # iterate over tesselations
    number_tesselations = int(np.max(tile_pattern[8][1]))
    current_palette = palette[palette[:,2]>0]

    for i in range (1, number_tesselations+1):
        # skip if number not found
        if ~np.any(tile_pattern[8][1]==i):
            continue
        #i=1
        location = np.where(tile_pattern[8][1]==i)
        # skip if no tile required
        if np.all(np.isnan(tile_pattern[8][0][location])):
            continue
        shapes_required = np.floor(tile_pattern[8][0][location])
        # list of available colours in that shape
        available_palette = current_palette[np.in1d(current_palette[:,1],shapes_required)]
        available_palette = available_palette[available_palette[:][:,2]>0]

        if len(available_palette[:][:,0]) == 0:
            print('No more tiles of shape {} available'.format(shapes_required))
        
        if len(location[0]>0):
            for j in range(0,len(location[0])):
                # shapes_required = np.floor(tile_pattern[8][0][location])
                # # list of available colours in that shape
                # available_palette = current_palette[np.in1d(current_palette[:,1],shapes_required)]
                # available_palette = available_palette[available_palette[:][:,2]>0]

                #change colour if not available       
                if  ~np.any(available_palette[:][:,0] == colour_seed):
                    #print('all gone')
                    colour_seed = available_palette[0,0]
                
                if tile_pattern[8][0][location[0][j]][location[1][j]] >0:
                    tile_pattern[8][2][location[0][j]][location[1][j]] = colour_seed
                    
                    # update inventory (colour, shape)
                    current_shape = shapes_required[j]
                    chosen_tile = np.where((current_palette[:, :-1] == (colour_seed, current_shape)).all(axis=1))
                    current_palette[chosen_tile,2] -=1
        
        # if gaps in numbers change colour
        if colour_mode == 'pass' and ~np.any(tile_pattern[8][1]==i+1):
            palette_position += 1            
            if palette_position > len(available_palette[:,0])-1:
                palette_position = 0
            colour_seed = available_palette[palette_position,0]
        #if different tesselation change colour    
        elif colour_mode == 'alternating':
            if colour_seed == available_palette[palette_position,0]:
                colour_seed = available_palette[palette_position,1]
            else:
                colour_seed = available_palette[palette_position,0]
        elif colour_mode == 'random':
            colour_seed = np.random.randint(1,len(available_palette[:,0])+1)
        #loop over palette in turn
        elif colour_mode == 'sequence': # and ~np.any(tile_pattern[8][1]==i+1):
            palette_position += 1
            if palette_position > len(available_palette[:,0])-1:
                palette_position = 0
            colour_seed = available_palette[palette_position,0]

    
    return tile_pattern

"""
The aim of this function is to count tiles used
""" 
def Count_Tiles(colour_pattern,palette):
    mask = np.isnan(colour_pattern[8][0])
    shapes_used = np.floor(colour_pattern[8][0][~mask])
    colours_used = colour_pattern[8][2][~mask]
    for i in range (0,len(palette[:,0])):
        colour = palette[i,0]
        shape = palette[i,1]
        amount = palette[i,2]
        count = np.where(colours_used==colour)
        if len(count[0]) > amount:
            print("The number of tiles of colour {}, shape {} required is {}. Only {} available.".format(colour,shape,len(count[0]),amount))
        else:
            print("The number of tiles of colour {}, shape {} required is {}/{}.".format(colour,shape,len(count[0]),amount))


"""
The aim of this function is to display the final result along with the tile orientation
""" 
def Plot_Pattern(colour_pattern):
    colours_used = np.where(colour_pattern[8][2]==0,np.NaN,colour_pattern[8][2])
    # replace the numbers for the tile orientation with symbols
    legend = colour_pattern[8][0].copy().tolist()
    for i in range(0, len(legend[:][0])):
        legend[i] = [tile_dict.get(j, j) for j in legend[i]]
    
    sb.heatmap(colours_used,annot=legend, fmt = '', cmap="Pastel2_r")    


### Run Program ###
cutout=np.array([3,3,4,4])
translation = [1,1]

## Knots and Dots Frame ## 
canvas = Canvas(x,y,colour,border,cutout)  

tile_pattern = Tile_Pattern(canvas,[0,0],pattern["knot"],translation,fill=False,wrap=False)

tile_pattern = Tile_Pattern(canvas,[3,0],pattern["knot"],translation,fill=False,wrap=True,tile_ID=tile_pattern[9])

tile_pattern = Tile_Pattern(canvas,[5,0],pattern["knot"],translation,fill=False,wrap=True,tile_ID=tile_pattern[9])

tile_pattern = Tile_Pattern(canvas,[2,0],pattern["dot"],translation,fill=False,wrap=False,tile_ID=tile_pattern[9])

tile_pattern = Tile_Pattern(canvas,[0,1],pattern["dot"],translation,fill=False,wrap=False,tile_ID=tile_pattern[9])

tile_pattern = Tile_Pattern(canvas,[7,0],pattern["knot"],translation,fill=False,wrap=True,tile_ID=tile_pattern[9])

tile_pattern = Tile_Pattern(canvas,[-1,6],pattern["knot"],translation,fill=False,wrap=True,tile_ID=tile_pattern[9])

colour_pattern = Colour_Pattern(tile_pattern,palette,colour_mode = 'pass')
count_tiles = Count_Tiles(colour_pattern,palette)
Plot_Pattern(colour_pattern)

## Knots Frame ## 
# canvas = Canvas(x,y,colour,border,cutout) 
# tile_pattern = Tile_Pattern(canvas,[0,0],pattern["knot"],translation,fill=True,wrap=True)

# colour_pattern = Colour_Pattern(tile_pattern,palette,colour_mode = 'pass')
# count_tiles = Count_Tiles(colour_pattern,palette)
# Plot_Pattern(colour_pattern)

## Circles Frame ##
# canvas = Canvas(x,y,colour,border,cutout) 
# tile_pattern = Tile_Pattern(canvas,[0,0],pattern["circle"],translation=[2,2],fill=True,wrap=True)

# reduced_palette = palette[np.where(palette[:,1]==3)]
# colour_pattern = Colour_Pattern(tile_pattern,reduced_palette,colour_mode = 'random')
# count_tiles = Count_Tiles(colour_pattern,reduced_palette)
# Plot_Pattern(colour_pattern)