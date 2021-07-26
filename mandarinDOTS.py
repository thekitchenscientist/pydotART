vocab_list = ["以","要","就","可","也","得","着","过","道","所","然","事","经","动","还","进","但","因","从","日","意","它","长","第","公","已","情","知","正","外","两","间","问","最","手","体","等","新","身","表","给","次","门","常","教","比","员","真","走","条","题","别","报","务","场","件","便","司","眼","非","白","思","完","色","路","告","边","望","共","让","运","笑","步","每","快","往","近","夫","准","始","远","备","百","离","病","息","火","早","找","吧","考","红","虽","希","房","黑","足","孩","站","诉","千","男","助","乐","球","错","晚","试","送","药","游","室","您","帮","左","右","穿","哥","弟","慢","忙","介","鱼","跑","贵","班","票","睛","旅","笔","卖","旁","阴","跳","雪","肉","馆","牛","纸","歌","床","玩","妻","休","舞","姓","妹","汽","课","懂","绍","丈","洗","唱","奶","宜","累","羊","零","蛋","鸡","宾","颜","瓜","晴","啡","篮","咖","踢","泳","铅"]


import PIL
from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw
import numpy as np
import pydotART as da

colour = 15
canvas_seed = [0,0]
border=0
cutout=np.array([0,0,0,0])
width_x =  width_y = int(np.sqrt(len(vocab_list))+ 1)*16

canvas = da.Canvas(width_x,width_y,colour,border,cutout)
pattern_list = []
tile_ID=1

#load the font at size 16
font = ImageFont.truetype("GnuUnifontFull-Pm9P.ttf",16)
for phrase in vocab_list:

    width_y = int(16)
    width_x = int(len(phrase)*16)
    
    img=Image.new("1", (width_x,width_y),(1))
    draw = ImageDraw.Draw(img)
    draw.text((0, 0),phrase,(0),font=font)
    phrase_array = np.array(img)
    phrase_array = np.fliplr(phrase_array)
    #convert to canvas
    phrase_canvas = da.Canvas(width_y,width_x,colour,border,cutout) 
    phrase_canvas[8][0][phrase_array==False] = 1
    phrase_canvas[8][1][phrase_array==False] = tile_ID
    pattern_list.append(phrase_canvas)
    tile_ID +=1

#tile and colour
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
da.Ldraw_Pattern(canvas, "Vocab - DOTS", add_steps=True)