# -*- coding: utf-8 -*-
"""
Created on Wed May 26 19:49:15 2021

@author: Stephen Pearson
https://github.com/thekitchenscientist/pydotART

This code is designed to produce viable pattens using LEGO® DOTS™. 

You need to supply the area to cover, the available DOTS and a sub-pattern.
There are different functions available to apply that pattern to the canvas.

Outputs can be a building plan or LDraw digital representation.

Examples builds are shown at 
https://rebrickable.com/sets/30556-1/mini-frame/?inventory=1#alt_builds


Potential future updates besides those mentioned in each function are:
    save and load canvas
    apply border to canvas prior to rendering or export
    add LDraw colour dictionary
    space invader sprite function
    morse code pattern generator
    dna code pattern generator
    'snakes', 'clouds' and 'cactus' pattern generators
    fill exposed studs with tile option
    ipywidget interface    
"""

import numpy as np
from datetime import datetime

## tile dictionaries ##
tile_dict = {0:" ",
             1:"■",
             1.1:"◆",
             1.3:"◆",
             1.5:"◆",
             1.7:"◆",
        2:"○",
        3:"◔",
        3.1:"▸",
        3.2:"◢",
        3.3:"▽",
        3.4:"◣",
        3.5:"◂",
        3.6:"◸",
        3.7:"△",
        3.8:"◹",
        4:"◖",
        4.2:"C",
        4.4:"∩",
        4.6:"D",
        4.8:"U",
        7:"🧀",
        7.2:">",
        7.4:"v",
        7.6:"<",
        7.8:"^",
        8:"🎩",
        8.2:"[",
        8.4:"]",
        9:"⼧",
        9.2:"{",
        9.4:"}",
        10:"X",
        11:"▣",
        12:"◎",
        13:"⚘",
        14:"⁕",
        15:"🧁",
        16:"☆",
        17:"♡"}

ldraw_dict = {
    -6:"1.000000 0.000000 0.000000 0.000000 1.000000 0.000000 0.000000 0.000000 1.000000 3958.dat",
    -1:"1.000000 0.000000 0.000000 0.000000 1.000000 0.000000 0.000000 0.000000 1.000000 3811.dat",
             1:"1.000000 0.000000 0.000000 0.000000 1.000000 0.000000 0.000000 0.000000 1.000000 3070b.dat",
             1.1:"◆",
             1.3:"◆",
             1.5:"◆",
             1.7:"◆",
        2:"1.000000 0.000000 0.000000 0.000000 1.000000 0.000000 0.000000 0.000000 1.000000 98138.dat",
        3:"◔",
        3.1:"-0.766045 0.000000 0.642787 0.000000 1.000000 0.000000 -0.642787 0.000000 -0.766045 25269.dat",
        3.2:"-1.000000 0.000000 0.000000 0.000000 1.000000 0.000000 0.000000 0.000000 -1.000000 25269.dat",
        3.3:"-0.707107 0.000000 -0.707107 0.000000 1.000000 0.000000 0.707107 0.000000 -0.707107 25269.dat",
        3.8:"0.000000 0.000000 -1.000000 0.000000 1.000000 0.000000 1.000000 0.000000 0.000000 25269.dat",
        3.5:"0.707107 0.000000 -0.707107 0.000000 1.000000 0.000000 0.707107 0.000000 0.707107 25269.dat",
        3.6:"1.000000 0.000000 0.000000 0.000000 1.000000 0.000000 0.000000 0.000000 1.000000 25269.dat",
        3.7:"0.707104 0.000000 0.707110 0.000000 1.000000 0.000000 -0.707110 0.000000 0.707104 25269.dat",
        3.4:"0.000000 0.000000 1.000000 0.000000 1.000000 0.000000 -1.000000 0.000000 0.000000 25269.dat",
        4:"◖",
        4.2:"0.000000 0.000000 1.000000 0.000000 1.000000 0.000000 -1.000000 0.000000 0.000000 24246.dat",
        4.4:"-1.000000 0.000000 -0.000001 0.000000 1.000000 0.000000 0.000001 0.000000 -1.000000 24246.dat",
        4.6:"0.000001 0.000000 -1.000000 0.000000 1.000000 0.000000 1.000000 0.000000 0.000001 24246.dat",
        4.8:"1.000000 0.000000 0.000001 0.000000 1.000000 0.000000 -0.000001 0.000000 1.000000 24246.dat",
        7:"🧀",
        7.2:"0.000000 0.000000 -1.000000 0.000000 1.000000 0.000000 1.000000 0.000000 0.000000 54200.dat",
        7.4:"1.000000 0.000000 0.000000 0.000000 1.000000 0.000000 0.000000 0.000000 1.000000 54200.dat",
        7.6:"0.000000 0.000000 1.000000 0.000000 1.000000 0.000000 -1.000000 0.000000 0.000000 54200.dat",
        7.8:"-1.000000 0.000000 0.000000 0.000000 1.000000 0.000000 0.000000 0.000000 -1.000000 54200.dat",
        8:"🎩",
        8.2:"1.000000 0.000000 0.000000 0.000000 1.000000 0.000000 0.000000 0.000000 1.000000 49307.dat",
        8.4:"0.000000 0.000000 1.000000 0.000000 1.000000 0.000000 -1.000000 0.000000 0.000000 49307.dat",
        9:"⼧",
        9.2:"1.000000 0.000000 0.000000 0.000000 1.000000 0.000000 0.000000 0.000000 1.000000 35464.dat",
        9.4:"0.000000 0.000000 1.000000 0.000000 1.000000 0.000000 -1.000000 0.000000 0.000000 35464.dat",
        10:"1.000000 0.000000 0.000000 0.000000 1.000000 0.000000 0.000000 0.000000 1.000000 22388.dat",
        11:"1.000000 0.000000 0.000000 0.000000 1.000000 0.000000 0.000000 0.000000 1.000000 3024.dat",
        12:"1.000000 0.000000 0.000000 0.000000 1.000000 0.000000 0.000000 0.000000 1.000000 6141.dat",
        13:"0.707107 0.000000 0.707107 0.000000 1.000000 0.000000 -0.707107 0.000000 0.707107 33291.dat",
        14:"1.000000 0.000000 0.000000 0.000000 1.000000 0.000000 0.000000 0.000000 1.000000 24866.dat",
        15:"1.000000 0.000000 0.000000 0.000000 1.000000 0.000000 0.000000 0.000000 1.000000 53119.dat",
        16:"1.000000 0.000000 0.000000 0.000000 1.000000 0.000000 0.000000 0.000000 1.000000 11609.dat",
        17:"1.000000 0.000000 0.000000 0.000000 1.000000 0.000000 0.000000 0.000000 1.000000 39739.dat"   
    }

ldraw_header = "0 Untitled Model\n0 Name:  dots palette\n0 Author:  \n0 CustomBrick\n0 NumOfBricks:  "

"""
1 <colour> x y z a b c d e f g h i <file>
<colour> is a number representing the colour of the part.
x y z is the x y z coordinate of the part
-1, 7, 9, 16 y is 0.000000 else -8.000000 -Y is height
20 studs is 1x1
a b c d e f g h i represents the rotation and scaling of the part.
"""

## pre-programmed colouring options based on DOTS packaging ##
colour_modes = ['alternating', 'sequence', 'random', 'pass', 'deplete']

## pre-programmed patterns based on DOTS packaging ##
pattern_dict = {
   "dot" : np.array([[2]]),
   
   "quarter" : np.array([[3.2]]),
   
   "scale" : np.array([[3.7]]),

"leaf" : np.array([[3.4],
                 [3.8]]),

"left_circle" : np.array([[3.2],
                        [3.8]]),

"right_circle" : np.array([[3.4],
                         [3.6]]),

"circle" : np.array([[3.2,3.4],
                        [3.8,3.6]
                        ]),
"windmill" : np.array([[3.8,3.2],
                        [3.6,3.4]
                        ]),

"tulip" : np.array([[3.2,3.4],
                        [3.6,3.8]
                        ]),

"butterfly" : np.array([[3.4,3.2],
                        [3.6,3.8]
                        ]) ,

"shield" : np.array([[1,1],
                        [3.8,3.6]
                        ])  ,

"large_leaf" : np.array([[3.2,1],
                        [1,3.6]
                        ]) 
    }


### Functions ###
def Canvas(x,y,colour=1,border=0,cutout=np.array([0,0,0,0])):
    """Encode the configuration into an array.
    
    Return the blank canvas.
    
    Do some checks that the combinations are viable (border and cut out leave some studs
    to tile on). Create the canvas.
    """

    # check border is not too big
    if border > 0 and (x-2*border < 2 or y-2*border < 2):
        print('Border is too large please choose a smaller value')
        return
    # resize canvas based on border
    x = x - 2 * border
    y = y - 2 * border
    
    # check cutout is not too big
    if cutout[2] > x-2 or cutout[3] > y-2:
        print('Cut out is too large please choose a smaller value')
        return
    
    return([x,y,colour,border,cutout[0]-1,cutout[1]-1,cutout[2],cutout[3],np.zeros((3,x,y)),0])
    


def Tile_Check(canvas,canvas_seed,palette,pattern,translation):
    """A basic check their are enough tiles to cover the canvas
    """    
    
    tesselation = np.floor(pattern)
    # count the available tiles
    tiles = palette[:,2].sum()
    # count the available studs
    studs = canvas[0]*canvas[1] - canvas[6]*canvas[7]

    tiles_percent = len(np.where(tesselation>0)[0])/tesselation.size
    if tiles*tiles_percent < studs:
        print('Not enough tiles to cover canvas')



def Pattern(canvas,starting_x,starting_y,pattern,translation,tile_ID,wrap=True,rotate=0):
    """Place the tiles for one pass across the canvas.
    
    Return the canvas with the patterns applied.
    
    The pattern is applied across the canvas using the translation. If a stud already has a tile
    on that part of the pattern will not be placed. THe tile ID is needed so that the colouring
    function has the order the patterns were laid in.
    If wrap is True the the pattern will continue on the top of the canvas if it partly crosses the bottom.
    Rotation currently only works for square patterns.
    """

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
                #print('cant start')
                break
        #randomise pattern orientation
        if rotate >=0 and tesselation.shape[0]==tesselation.shape[1]:
           new_pattern = Rotate_Pattern(pattern,rotate)
           tesselation = np.floor(new_pattern)
        else:
           new_pattern = pattern 
        
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
                    current_solution[current_x+j][current_y+k] = new_pattern[j][k]
                    current_positions[current_x+j][current_y+k] = tile_ID                    
                except:
                    print([i,j,k,current_x+j,current_y+k,tesselation[j][k]])
        tile_ID += 1
        if translation[0] ==0 and translation[1] == 0:
            break

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



def Tile_Pattern(canvas,canvas_seed,pattern,translation,fill=True,wrap=True,rotate=0,tile_ID = 1):
    """Apply the pattern across the canvas as specified.
    
    Return the canvas with the patterns applied.
    
    Starting from the seed location
    """ 
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
            result = Pattern(canvas,offset_x+i*width_x,offset_y+j*width_y,pattern,translation,tile_ID,wrap,rotate)
            canvas[8][0] = result[0].copy()
            canvas[8][1] = result[1].copy()
            tile_ID = result[2]      
            if translation[1] > 0 and j > 0:
                break
    canvas[9] =  tile_ID  
    return canvas



def Mirror_Pattern(canvas,mode):
    """Mirror the pattern on the canvas
    
    Return the output pattern after applying the mirror planes to the canvas.    
    mode=["X","Y","y=x","y=-x"]
    After placing the mirror planes (X, Y, y=x or y=-x) a mask is applied to all but the
    left (and/or upper side). The array is then indexed to the patterns can be translated correctly.
    Finally the tiles are rotated based on how they were mirrored to maintain the correct patterns.
    
    A future update would allow the modes "y=x" and "y=-x" to rotate the tiles correctly.
    """ 

    number_planes = len(mode)
    
    x = canvas[0]
    y= canvas[1]

    working_canvas = np.zeros((3,x,y)).astype('float')
    mask = working_canvas[0].copy()
    index = working_canvas[0].copy()
    
    # index canvas
    count = 1
    for i in np.nditer(index, op_flags=['readwrite']):
        i[...] = count
        count+=1
            
    # fill mask with NaN
    for i in range (0, number_planes):
        if mode[i] == "X":
            for j in range(0,x):
                if j >= np.floor(x/2):
                    mask[:,j]=np.nan
        elif mode[i] == "Y":
            for j in range(0,x):
                if j >= np.floor(x/2):
                    mask[j,:]=np.nan
        elif mode[i] == "y=x":
            mask = np.tril(mask-1)
            mask[mask == 0] = np.nan
            mask[mask < 0] = 0            
        elif mode[i] == "y=-x":
            mask2 = np.triu(working_canvas[0]-1)
            mask2[mask2 == 0] = np.nan
            mask2[mask2 < 0] = 0
            mask = mask*np.fliplr(mask2)

    # update index + mask
    index = index + mask
    index[np.isnan(index)] = 0 
    for i in range (0, number_planes):
        if mode[i] == "X":
            index += np.fliplr(index)
        elif mode[i] == "Y":
            index += np.flipud(index)
        elif mode[i] == "y=x":
            for j in range(0,x):
                for k in range (0,y):
                    if index[k][j] == 0:
                        index[k][j] = index[j][k]
        elif mode[i] == "y=-x":
            for j in range(0,x):
                for k in range (0,y):
                    if index[y-k-1][x-j-1] == 0:
                        index[y-k-1][x-j-1] = index[j][k]

    # apply mask to pattern
    working_canvas = canvas[8].copy()    
    mask[np.isnan(mask)] = -1000
    working_canvas[0] = working_canvas[0]+mask
    working_canvas[0][working_canvas[0]<0]=0
    working_canvas[0]

    # update canvas based on index
    for i in range( 1,int(np.amax(index))):
        locations_list = np.where(index==i)
        count = len(locations_list[0])
        if count>0:
            tile = np.amax(canvas[8][0][locations_list])
            if tile <= 0 or np.isnan(tile): 
                continue
            new_tile = tile*10
 
            origin = [locations_list[0][0],locations_list[1][0]]
            origin_ID = canvas[8][1][origin[0]][origin[1]]
            # index also need to know how the tiles should be transformed          
            for j in range (0,count):
                new_x = locations_list[0][j]
                new_y = locations_list[1][j]
                #this only works for 3 tiles not 4
                if new_x == origin[0] and new_y == origin[1]:
                    continue
                elif new_x == origin[0] and new_y > origin[1]:
                    if new_tile % 10 == 2:
                        tile = round((new_tile+2)/10,1)
                    elif new_tile % 10 == 4:
                        tile = round((new_tile-2)/10,1)
                    elif new_tile % 10 == 6:
                        tile = round((new_tile+2)/10,1)
                    elif new_tile % 10 == 8:
                        tile = round((new_tile-2)/10,1)
                elif new_x > origin[0] and new_y == origin[1]:
                    if new_tile % 10 == 2:
                        tile = round((new_tile+6)/10,1)
                    elif new_tile % 10 == 4:
                        tile = round((new_tile+2)/10,1)
                    elif new_tile % 10 == 6:
                        tile = round((new_tile-2)/10,1)
                    elif new_tile % 10 == 8:
                        tile = round((new_tile-6)/10,1)
                if new_x > origin[0] and new_y > origin[1]:
                    if new_tile % 10 == 2:
                        tile = round((new_tile+4)/10,1)
                    elif new_tile % 10 == 4:
                        tile = round((new_tile+4)/10,1)
                    elif new_tile % 10 == 6:
                        tile = round((new_tile-4)/10,1)
                    elif new_tile % 10 == 8:
                        tile = round((new_tile-4)/10,1)
                
                working_canvas[0][locations_list[0][j]][locations_list[1][j]] = tile
                working_canvas[1][locations_list[0][j]][locations_list[1][j]] = origin_ID

    canvas[8][0] = working_canvas[0].copy()
    canvas[8][1] = working_canvas[1].copy()    
 
    return canvas



def Spiral_Pattern(canvas,canvas_seed,pattern,direction=1,rotate=0,tile_ID = 1):
    """Apply the pattern across the canvas working down then around in a spiral.
    
    Returns the canvas with the applied tiles.
    
    A future update would allow spirals both clockwise and counter-clockwise.
    """ 
    width_x = len(pattern[:,0])
    width_y = len(pattern[0,:])

    x = canvas[0]
    y = canvas[1]

    # x and y must be even numbers or the code stops working
    if x % 2  == 1:
        x = x-1
    if y % 2  == 1:
        y = y-1

    offset_x = canvas_seed[0]
    offset_y = canvas_seed[1]

    extent_x = round(x/len(pattern[:,0]))
    extent_y = round(y/len(pattern[0,:]))

    current_xy = [offset_x,offset_x]
            
    for i in range(0,extent_x*extent_y):

        #print(current_xy)    
        result = Pattern(canvas,current_xy[0],current_xy[1],pattern,[0,0],tile_ID,False,rotate)
        canvas[8][0] = result[0].copy()
        canvas[8][1] = result[1].copy()
        tile_ID = result[2]           

        if current_xy[0] < x-width_x and current_xy[1] == offset_y:
            current_xy[0] += width_x
        elif current_xy[0] == x-width_x  and current_xy[1] < y-width_y: 
            current_xy[0] = x-width_x       
            current_xy[1] += width_y
        elif current_xy[1] == y-width_y  and current_xy[0] > offset_x:
            current_xy[0] -= width_x       
            current_xy[1] = y-width_y   
        elif current_xy[0] == offset_x  and current_xy[1] > offset_y+width_y:
            current_xy[0] = offset_x       
            current_xy[1] -= width_y           
        elif current_xy[0] == offset_x and current_xy[1] == offset_y+width_y:
            x = x - width_x
            y = y - width_y
            offset_x = offset_x + width_x
            offset_y = offset_y + width_y
            extent_x = round(x/len(pattern[:,0]))-2
            extent_y = round(y/len(pattern[0,:]))-2    
            current_xy[0] = offset_x       
            current_xy[1] = offset_y   

    canvas[9] =  tile_ID  
    return canvas

def Spiral_Pattern_List(canvas,canvas_seed,pattern_list,direction=1,rotate=0,tile_ID = 1):
    """Apply the pattern across the canvas working down then around in a spiral.
    
    Returns the canvas with the applied tiles.
    
    A future update would allow spirals both clockwise and counter-clockwise.
    """ 
    
    
    width_x = len(pattern_list[0][8][0][:,0])
    width_y = len(pattern_list[0][8][0][0,:])

    x = canvas[0]
    y = canvas[1]

    # x and y must be multiple or the code stops working
    if x % width_x  != 0:
        x = int((np.floor(x/width_x) +1)* width_x)
    if y % width_y  != 0:
        y = int((np.floor(y/width_y) +1)* width_y)

    offset_x = canvas_seed[0]
    offset_y = canvas_seed[1]

    extent_x = round(x/width_x)
    extent_y = round(y/width_y)

    current_xy = [offset_x,offset_x]
            
    for i in range(0,len(pattern_list)):
        
        #much tidier way to apply pattern to a larger canvas
        canvas[8][0][current_xy[0]:current_xy[0]+pattern_list[i][8][0].shape[0], current_xy[1]:current_xy[1]+pattern_list[i][8][0].shape[1]] = pattern_list[i][8][0]
        canvas[8][1][current_xy[0]:current_xy[0]+pattern_list[i][8][0].shape[0], current_xy[1]:current_xy[1]+pattern_list[i][8][1].shape[1]] = pattern_list[i][8][1]

        if current_xy[0] < x-width_x and current_xy[1] == offset_y:
            current_xy[0] += width_x
        elif current_xy[0] == x-width_x  and current_xy[1] < y-width_y: 
            current_xy[0] = x-width_x       
            current_xy[1] += width_y
        elif current_xy[1] == y-width_y  and current_xy[0] > offset_x:
            current_xy[0] -= width_x       
            current_xy[1] = y-width_y   
        elif current_xy[0] == offset_x  and current_xy[1] > offset_y+width_y:
            current_xy[0] = offset_x       
            current_xy[1] -= width_y           
        elif current_xy[0] == offset_x and current_xy[1] == offset_y+width_y:
            x = x - width_x
            y = y - width_y
            offset_x = offset_x + width_x
            offset_y = offset_y + width_y
            extent_x = round(x/width_x)-2
            extent_y = round(y/width_y)-2    
            current_xy[0] = offset_x       
            current_xy[1] = offset_y   

    canvas[9] =  tile_ID  
    return canvas

def Rotate_Pattern(pattern, angle=0):
    """Given an input tile orientation, rotate by the angle required.
    
    Returns the new tile orientation.
    
    A future update would allow rotation both clockwise and counter-clockwise.
    """  
    
    if angle == 0:
        return pattern
    
    if abs(angle) >= 360:
        rotations = np.random.randint(1,4)
    else:
        rotations = int(angle/90)

    new_pattern = pattern*10

    for i in range(0,rotations):
        new_pattern = np.rot90(new_pattern, k=-1)

        for x in np.nditer(new_pattern, op_flags = ['readwrite']):
            #if 3
            if x == 42:
                x[...] = 48
            elif x == 44:
                x[...] = 42
            elif x == 46:
                x[...] = 44
            elif x == 48:
                x[...] = 46                  
            elif x % 10 == 8 or x % 10 == 7:
                x[...] = x-6
            elif x % 10 == 0:
                x[...]
            else:
                x[...] = x+2
    
    return new_pattern/10



def Colour_Pattern(tile_pattern,palette,colour_mode,tiles_check=True):
    """Try to set the tile colours in the pattern.
    
    Returns the coloured pattern where each group of tiles that is placed is given the same colour.
    The palette defines how many tiles of each shape and colour are available.
    colour_modes available are:
        'alternating'
        'sequence'
        'random' - pick a colour at random from the palette.
        'pass'
        'deplete' - use up all the first colour in the palette before working through the next.
        
    tiles_check tries to update the palette but this is done after each tesselation, not each tile.
    """ 

    palette_position = 0
    # iterate over tesselations
    number_tesselations = int(np.max(tile_pattern[8][1]))
    current_palette = palette[palette[:,2]>0]
    colour_seed = current_palette[0,0]

    for i in range (1, number_tesselations+1):
        # skip if number not found
        if ~np.any(tile_pattern[8][1]==i):
            continue
        
        location = np.where(tile_pattern[8][1]==i)
        # skip if no tile required
        if np.all(np.isnan(tile_pattern[8][0][location])):
            continue
        if tiles_check:
            shapes_required = np.floor(tile_pattern[8][0][location])
            # list of available colours in that shape
            available_palette = current_palette[np.in1d(current_palette[:,1],shapes_required)]
            available_palette = available_palette[available_palette[:][:,2]>0]
        else:
            available_palette = current_palette
            
            if len(available_palette[:][:,0]) == 0:
                print('No more tiles of shape {} available'.format(shapes_required))
        
        if i == 1:
            colour_seed = available_palette[0,0]
        
        if len(location[0]>0):
            for j in range(0,len(location[0])):

                if tiles_check:
                    #change colour if not available       
                    if  ~np.any(available_palette[:][:,0] == colour_seed):
                        #print('all gone')
                        colour_seed = available_palette[0,0]
                
                if tile_pattern[8][0][location[0][j]][location[1][j]] >0:
                    tile_pattern[8][2][location[0][j]][location[1][j]] = colour_seed
                
                if tiles_check:
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
                colour_seed = available_palette[len(available_palette[:,0])-1,0]
            else:
                colour_seed = available_palette[palette_position,0]
        elif colour_mode == 'random':
            colour_seed = available_palette[np.random.randint(0,len(available_palette[:,0])-1),0]
        #loop over palette in turn
        elif colour_mode == 'sequence': # and ~np.any(tile_pattern[8][1]==i+1):
            palette_position += 1
            if palette_position > len(available_palette[:,0])-1:
                palette_position = 0
            colour_seed = available_palette[palette_position,0]
        #use up palette in turn
        elif colour_mode == 'deplete':
            colour_seed = available_palette[0,0]

    return tile_pattern



def Count_Tiles(colour_pattern,palette):
    """Count the number of tiles used in each shape and colour.

    A report is printed to the console.    
    """ 
    
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



def Plot_Pattern(coloured_pattern,cmap="Pastel2_r"):
    """Take a Canvas array and output an image to the Plots pane.
    
    If seaborn and matplotlib are not available write the 3D array to the console.
    The image is coloured plus symbols for tile type and orientation
    This function only has access to 18 basic Lego 1x1 tiles.
    It works by iterating over the array and converting the tile numbers into symbols.
    
    A future update would allow the colours to be correctly applied and the file exported
    to disc.
    """

    # replace the 0 with NaN so the plot looks correct
    colours_used = np.where(coloured_pattern[8][2]==0,np.NaN,coloured_pattern[8][2])
    
    # replace the numbers for the tile orientation with symbols
    legend = coloured_pattern[8][0].copy().tolist()
    shape = coloured_pattern[8][0].shape

    for i in range(0, shape[0]):
        for j in range(0, shape[1]):
            if ~np.isnan(legend[i][j]):
                legend[i][j] = tile_dict[legend[i][j]]

    try:
        import seaborn as sb
        import matplotlib.pyplot as plt
        fig = plt.figure()
        fig.set_size_inches(shape)
        sb.heatmap(colours_used,annot=legend, fmt = '', cmap=cmap)    
    except:
        print(coloured_pattern[8])



def Ldraw_Pattern(coloured_pattern,filename=datetime.now().strftime('%A %d%m%Y %H%M%S'),add_steps=False,base_plate=False):
    """Take a Canvas array and output an LDraw File.
    
    If no filename is specified, the current DateTime string is used. This function
    only has access to 18 basic Lego 1x1 tiles plus the 32x32 base plate. It works by
    iterating over the array and converting the position into an X,Y coordinate, with
    tile orientation and colouring.
    
    A future update would be to work out how many 32x32 base plates are needed to place the
    bricks on and centre them appropriately.
    """

    colours_used = np.where(coloured_pattern[8][2]==0,np.NaN,coloured_pattern[8][2])
    legend = coloured_pattern[8][0]
    tile_IDs = coloured_pattern[8][1]
    shape = coloured_pattern[8][0].shape
    number_tiles = len(np.where(coloured_pattern[8][0]>0)[0])

    output_string = ldraw_header + str(number_tiles)
    
    lines = [output_string]
    #need to iterate over tile ID then x,y
    for k in np.unique(tile_IDs):
        locations = np.where(tile_IDs==k)
        for l in range(0,len(list(locations[0]))):
            i = list(locations[0])[l]
            j = list(locations[1])[l]

            if ~np.isnan(legend[i][j]) and ~np.isnan(colours_used[i][j]):

                # -1, 7, 9, 16 y is 0.000000 else -8.000000 -Y is height
                if int(np.floor(legend[i][j])) == 7 or int(np.floor(legend[i][j])) == 9 or int(np.floor(legend[i][j])) == 16:
                    y_height = "0.000000 "
                else:
                    y_height = "-8.000000 "
                # Create line in LDraw file
                string = "1 " + str(int(colours_used[i][j])) + " " + str(i*20) + ".000000 "+ y_height + str(j*-20) + ".000000 " + ldraw_dict[legend[i][j]]
                lines.append(string)
                #check if steps are chosen and tile ID is about to change
        if add_steps == True:
            string = "0 STEP"
            lines.append(string)


    # open a file in write mode
    with open("pydotART "+filename+".ldr", 'w',encoding='utf8') as f:
        for line in lines:
            f.write(line)
            f.write('\n') 
    # close the file
    f.close

### Example Configuration ###
# What tiles are available? [Colour,Shape,Amount]
palette = np.array([[5,3.,16],
                    [323,3.,16],
                    [31,3.,16],
                    [29,2.,8],
                    [14,2.,4],
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

### Write Program Here ###
