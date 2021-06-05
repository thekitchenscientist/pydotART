# -*- coding: utf-8 -*-
"""
Created on Wed May 26 19:49:15 2021

@author: Stephen Pearson
"""

import numpy as np
import seaborn as sb

### Configuration ###

# Canvas Size and Colour
x=8
y=8
colour=1

# How wide should the untiled border around the edge be?
border=0

# What is the location and size of a central gap [x,y,x_length, y_length]
cutout=np.array([0,0,0,0])
cutout=np.array([3,3,4,4])

# Where should the tiling start from?
canvas_seed=[0,0]

# What is the pattern you want to tile?
tesselation = np.array([[3],
                        [3],
                        [0]])

pattern = np.array([[3.2],
                        [3.4],
                        [0]])
# Where should the next tile be placed relative to the previous?
translation=np.array([1,1])

# tile dictionary
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


# What tiles are avaiable [Colour,Shape,Amount]
palette = np.array([[1,3,16],
                    [2,3,16],
                    [3,3,16],
                    [4,2,8],
                    [5,2,4],
                    ])

# How should the tiles be coloured?
colour_mode = 'alternating'
#colour_mode = 'sequence'
# colour_mode = 'random'
colour_mode = 'pass'


# ## Unit Test (Circles)
# canvas_seed=[0,-1]
# tesselation = np.array([[3,3],
#                         [3,3]
#                         ])
# #round
# pattern = np.array([[3.1,3.2],
#                         [3.4,3.3]
#                         ])
# #windmill
# pattern = np.array([[3.4,3.1],
#                         [3.3,3.2]
#                         ])
# #fish
# pattern = np.array([[3.1,3.2],
#                         [3.3,3.4]
#                         ])

# #butterfly
# pattern = np.array([[3.2,3.1],
#                         [3.3,3.4]
#                         ])

#translation=np.array([2,2])
#translation=np.array([0,0])
#colour_mode = 'sequence'



### Functions ###
"""
The aim of this function is to encode the configuration, check the combinations
are viable and create
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
    
    return([x,y,colour,border,cutout[0]-1,cutout[1]-1,cutout[2],cutout[3],np.zeros((4,x,y))])
    

"""
The aim of this function is to check their are enough tiles
"""
def Tile_Check(canvas,canvas_seed,palette,tesselation,translation):
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
    shapes_required = np.unique(tesselation)
    update_to_palette = np.where(np.in1d(palette[:,1],shapes_required))
    palette = palette[update_to_palette,:][0]
    return palette

"""
The aim of this function is to place the tiles for one pass across the canvas
"""
def Pattern(canvas,starting_x,starting_y,tesselation,pattern,translation,tile_ID):

    x = canvas[0]
    y = canvas[1]
    current_x = starting_x
    current_y = starting_y
    current_solution = canvas[8][0]
    current_positions = canvas[8][1]
    current_pattern = canvas[8][3]

    #iterative over cells, then tiling pattern filling in the grid
    for i in range(0,int(x*y/len(tesselation[0:]))):
        #don't start if there is no room
        if i ==0:
            if current_positions[current_x+1][current_y] > 0:
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
                if current_x+j > x-1:
                    current_x = 0-j
                    current_y = current_y-k
                    if k>0:
                        current_y += 1
                    #print([current_x,current_y])
                if current_x+j < 0 or current_y+k < 0:
                    print('outside canvas')
                    continue
                try:
                    if current_positions[current_x+j][current_y+k] > 0:
                        print('taken')
                        break
                    current_solution[current_x+j][current_y+k] = tesselation[j][k]
                    current_positions[current_x+j][current_y+k] = tile_ID
                    if tesselation[j][k] > 0:
                        current_pattern[current_x+j][current_y+k] = pattern[j][k]                        
                except:
                    print([i,j,k,current_x+j,current_y+k,tesselation[j][k]])
        tile_ID += 1
        current_x += translation[0]           
        current_y += translation[1]
        #stop at edge of canvas
        if current_x == x and current_y == y:
            print('end')
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
print the output pattern to use
""" 
def Tile_Pattern(canvas,canvas_seed,tesselation,pattern,translation):
    offset_x = canvas_seed[0]
    offset_y = canvas_seed[1]
    # if translation[1] == 0:
    for i in range(0,round(x/len(tesselation[:,0]))):
        for j in range(0,round(y/len(tesselation[0,:]))):                
            if i == 0 and j ==0:
                tile_ID = 1        
            result = Pattern(canvas,offset_x+i*len(tesselation[:,0]),offset_y+j*len(tesselation[0,:]),tesselation,pattern,translation,tile_ID)
            canvas[8][0] = result[0].copy()
            canvas[8][1] = result[1].copy()
            tile_ID = result[2]      
            if translation[1] > 0 and j > 0:
                break
         
    return canvas

"""
The aim of this function is to set the tile colours
""" 
def Colour_Pattern(tile_pattern,palette,colour_mode):
    colour_seed = 1
    palette_size = len(palette[:,0])
    palette_position = 0
    # iterate over tesselations
    number_tesselations = int(np.max(tile_pattern[8][1]))

    for i in range (1, number_tesselations+1):
        # skip if number not found
        if ~np.any(tile_pattern[8][1]==i):
            continue

        location = np.where(tile_pattern[8][1]==i)
        if len(location[0]>0):
            for j in range(0,len(location[0])):
                #change colour seed if not required shape
                if tile_pattern[8][3][location[0][j]][location[1][j]] >0:
                    tile_pattern[8][2][location[0][j]][location[1][j]] = colour_seed
       
        # if gaps in numbers change colour
        if colour_mode == 'pass' and ~np.any(tile_pattern[8][1]==i+1):
            palette_position += 1            
            if palette_position > palette_size-1:
                palette_position = 0
            colour_seed = palette[palette_position,0]
            
        elif colour_mode == 'alternating':
            if colour_seed == 1:
                colour_seed = 2
            else:
                colour_seed = 1
        elif colour_mode == 'random':
            colour_seed = np.random.randint(1,palette_size+1)
        #loop over palette in turn
        elif colour_mode == 'sequence' and ~np.any(tile_pattern[8][1]==i+1):
            palette_position += 1
            if palette_position > palette_size-1:
                palette_position = 0
            colour_seed = palette[palette_position,0]


    return tile_pattern

"""
The aim of this function is to count tiles used
""" 
def Count_Tiles(colour_pattern,palette):
    mask = np.isnan(colour_pattern[8][0])
    shapes_used = colour_pattern[8][0][~mask]
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
    mask = np.isnan(colour_pattern[8][0])
    colours_used = np.where(mask ,np.NaN,colour_pattern[8][2])
    legend = colour_pattern[8][3].copy().tolist()
    for i in range(0, len(legend[:][0])):
        legend[i] = [tile_dict.get(j, j) for j in legend[i]]
    
    sb.heatmap(colours_used,annot=legend, fmt = '', cmap="Pastel2_r")    


### Run Program ###
 
canvas = Canvas(x,y,colour,border,cutout)  
palette = Tile_Check(canvas,canvas_seed,palette,tesselation,translation)
tile_pattern = Tile_Pattern(canvas,canvas_seed,tesselation,pattern,translation)
colour_pattern = Colour_Pattern(tile_pattern,palette,colour_mode)
count_tiles = Count_Tiles(colour_pattern,palette)
Plot_Pattern(colour_pattern)

