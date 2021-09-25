import cv2
import kociemba
import numpy as np
import time
import colorama
import math
import logging
from vpython import *
import random
import serial
import glob
import sys
import json

fps=24

#六个中心块颜色
d   = 'w'
u   = 'y'
f   = 'g'
b   = 'b'
r   = 'o'
l   = 'r'

#12个边块
uf = {'u': 'y', 'd': '', 'f': 'g', 'b': '', 'r': '', 'l': ''}
ur = {'u': 'y', 'd': '', 'f': '', 'b': '', 'r': 'o', 'l': ''}
ub = {'u': 'y', 'd': '', 'f': '', 'b': 'b', 'r': '', 'l': ''}
ul = {'u': 'y', 'd': '', 'f': '', 'b': '', 'r': '', 'l': 'r'}
df = {'u': '', 'd': 'w', 'f': 'g', 'b': '', 'r': '', 'l': ''}
dr = {'u': '', 'd': 'w', 'f': '', 'b': '', 'r': 'o', 'l': ''}
db = {'u': '', 'd': 'w', 'f': '', 'b': 'b', 'r': '', 'l': ''}
dl = {'u': '', 'd': 'w', 'f': '', 'b': '', 'r': '', 'l': 'r'}
fr = {'u': '', 'd': '', 'f': 'g', 'b': '', 'r': 'o', 'l': ''}
fl = {'u': '', 'd': '', 'f': 'g', 'b': '', 'r': '', 'l': 'r'}
br = {'u': '', 'd': '', 'f': '', 'b': 'b', 'r': 'o', 'l': ''}
bl = {'u': '', 'd': '', 'f': '', 'b': 'b', 'r': '', 'l': 'r'}

#8个角
ufr = {'u': 'y', 'd': '', 'f': 'g', 'b': '', 'r': 'o', 'l': ''}
ufl = {'u': 'y', 'd': '', 'f': 'g', 'b': '', 'r': '', 'l': 'r'}
ubr = {'u': 'y', 'd': '', 'f': '', 'b': 'b', 'r': 'o', 'l': ''}
ubl = {'u': 'y', 'd': '', 'f': '', 'b': 'b', 'r': '', 'l': 'r'}
dfr = {'u': '', 'd': 'w', 'f': 'g', 'b': '', 'r': 'o', 'l': ''}
dfl = {'u': '', 'd': 'w', 'f': 'g', 'b': '', 'r': '', 'l': 'r'}
dbr = {'u': '', 'd': 'w', 'f': '', 'b': 'b', 'r': 'o', 'l': ''}
dbl = {'u': '', 'd': 'w', 'f': '', 'b': 'b', 'r': '', 'l': 'r'}

state_conv={
    'green'  : 'g',
    'white'  : 'w',
    'blue'   : 'b',
    'red'    : 'r',
    'orange' : 'o',
    'yellow' : 'y'
}

faces={'F': (color.green, vector(0, 0, 1)),
	   'B': (color.blue, vector(0, 0, -1)),
	   'U': (color.yellow, vector(0, 1, 0)),
	   'L': (color.red, vector(-1, 0, 0)),
	   'D': (color.white, vector(0, -1, 0)),
	   'R': (color.orange, vector(1, 0, 0))}
cubies = []
def newCube(state):
    global d, u, f, b, r, l, uf, ur, ub, ul, df, dr, db, dl, fr, fl, br, bl, ufr, ufl, ubr, ubl, dfr, dfl, dbr, dbl
    b=0
    for face_color, face_axis in faces.values():
        a = 0
        index_num = [6, 3, 0, 7, 4, 1, 8, 5, 2]
        index_faces = ['front', 'back', 'up', 'left', 'down', 'right']
        for x in (-1, 0, 1):
            for y in (-1, 0, 1):
                # 每个颜色的面先形成同一个位置的面，z=1。5
                faceColor=color_RBG[state[index_faces[b]][index_num[a]]]
                sticker = box(color=vector(faceColor), pos=vector(x, y, 1.5), length=0.98, height=0.98, width=0.05)
                # 计算旋转角度，除了正面和背面，都需要转90,背面转180，正面转0
                cos_angle = dot(vector(0, 0, 1), face_axis)
                # 计算旋转轴，正面和背面的旋转轴是100，其他的事和001的叉乘
                if cos_angle==0:
                    pivot=(cross(vector(0, 0, 1), face_axis))
                elif cos_angle==(dot(vector(0, 0, 1), vector(0, 0, 1))):
                    pivot=vector(1,0,0)
                else:
                    pivot=vector(0,1,0)

                #pivot = (cross(vector(0, 0, 1), face_axis) if cos_angle == 0 else vector(1, 0, 0))
                # origin是起始位置，从起始点到旋转物体这么个轴，围绕axis，旋转angle
                sticker.rotate(angle=acos(cos_angle), axis=pivot, origin=vector(0, 0, 0))
                cubies.append(sticker)
                a+=1
            # print(sticker.pos,sticker.color)
        b += 1
    # 12个边块
    uf['u'],ur['u'],ub['u'],ul['u'],ufr['u'],ufl['u'],ubr['u'],ubl['u']= state_conv[state['up'][7]],state_conv[state['up'][5]],state_conv[state['up'][1]],state_conv[state['up'][3]],state_conv[state['up'][8]],state_conv[state['up'][6]],state_conv[state['up'][2]],state_conv[state['up'][0]]
    df['d'],dr['d'],db['d'],dl['d'],dfr['d'],dfl['d'],dbr['d'],dbl['d']= state_conv[state['down'][1]],state_conv[state['down'][5]],state_conv[state['down'][7]],state_conv[state['down'][3]],state_conv[state['down'][2]],state_conv[state['down'][0]],state_conv[state['down'][8]],state_conv[state['down'][6]]
    uf['f'],df['f'],fr['f'],fl['f'],ufr['f'],ufl['f'],dfr['f'],dfl['f']= state_conv[state['front'][1]],state_conv[state['front'][7]],state_conv[state['front'][5]],state_conv[state['front'][3]],state_conv[state['front'][2]],state_conv[state['front'][0]],state_conv[state['front'][8]],state_conv[state['front'][6]]
    ub['b'],db['b'],br['b'],bl['b'],ubr['b'],ubl['b'],dbr['b'],dbl['b']= state_conv[state['back'][1]],state_conv[state['back'][7]],state_conv[state['back'][3]],state_conv[state['back'][5]],state_conv[state['back'][0]],state_conv[state['back'][2]],state_conv[state['back'][6]],state_conv[state['back'][8]]
    ur['r'],dr['r'],fr['r'],br['r'],ufr['r'],ubr['r'],dfr['r'],dbr['r']= state_conv[state['right'][1]],state_conv[state['right'][7]],state_conv[state['right'][3]],state_conv[state['right'][5]],state_conv[state['right'][0]],state_conv[state['right'][2]],state_conv[state['right'][6]],state_conv[state['right'][8]]
    ul['l'],dl['l'],fl['l'],bl['l'],ufl['l'],ubl['l'],dfl['l'],dbl['l']= state_conv[state['left'][1]],state_conv[state['left'][7]],state_conv[state['left'][5]],state_conv[state['left'][3]],state_conv[state['left'][2]],state_conv[state['left'][0]],state_conv[state['left'][8]],state_conv[state['left'][6]]
    d = 'w'
    u = 'y'
    f = 'g'
    b = 'b'
    r = 'o'
    l = 'r'
    # uf = {'u': state['up'][7], 'd': '', 'f': state['front'][1], 'b': '', 'r': '', 'l': ''}
    # ur = {'u': state['up'][5], 'd': '', 'f': '', 'b': '', 'r': state['right'][1], 'l': ''}
    # ub = {'u': state['up'][1], 'd': '', 'f': '', 'b': state['back'][1], 'r': '', 'l': ''}
    # ul = {'u': state['up'][3], 'd': '', 'f': '', 'b': '', 'r': '', 'l': state['left'][1]}
    # df = {'u': '', 'd': state['down'][1], 'f': state['front'][7], 'b': '', 'r': '', 'l': ''}
    # dr = {'u': '', 'd': state['down'][5], 'f': '', 'b': '', 'r': state['right'][7], 'l': ''}
    # db = {'u': '', 'd': state['down'][7], 'f': '', 'b': state['back'][7], 'r': '', 'l': ''}
    # dl = {'u': '', 'd': state['down'][3], 'f': '', 'b': '', 'r': '', 'l': state['left'][7]}
    # fr = {'u': '', 'd': '', 'f': state['front'][5], 'b': '', 'r': state['right'][3], 'l': ''}
    # fl = {'u': '', 'd': '', 'f': state['front'][3], 'b': '', 'r': '', 'l': state['left'][5]}
    # br = {'u': '', 'd': '', 'f': '', 'b': state['back'][3], 'r': state['right'][5], 'l': ''}
    # bl = {'u': '', 'd': '', 'f': '', 'b': state['back'][5], 'r': '', 'l': state['left'][3]}
    # # 8个角
    # ufr = {'u': state['up'][8], 'd': '', 'f': state['front'][2], 'b': '', 'r': state['right'][0], 'l': ''}
    # ufl = {'u': state['up'][6], 'd': '', 'f': state['front'][0], 'b': '', 'r': '', 'l': state['left'][2]}
    # ubr = {'u': state['up'][2], 'd': '', 'f': '', 'b': state['back'][0], 'r': state['right'][2], 'l': ''}
    # ubl = {'u': state['up'][0], 'd': '', 'f': '', 'b': state['back'][2], 'r': '', 'l': state['left'][0]}
    # dfr = {'u': '', 'd': state['down'][2], 'f': state['front'][8], 'b': '', 'r': state['right'][6], 'l': ''}
    # dfl = {'u': '', 'd': state['down'][0], 'f': state['front'][6], 'b': '', 'r': '', 'l': state['left'][8]}
    # dbr = {'u': '', 'd': state['down'][8], 'f': '', 'b': state['back'][6], 'r': state['right'][8], 'l': ''}
    # dbl = {'u': '', 'd': state['down'][6], 'f': '', 'b': state['back'][8], 'r': '', 'l': state['left'][6]}


def rotateCube(moves):
    print(moves)
    for i in range(len(moves)):
        move = moves[i]
        if len(move) > 1 and move[1] == '2':
            turn(move[0])
            turn(move[0])
        else:
            turn(move)
        print(i, " ", move)
        printCube()




def rotate3D(key):
	#输入的是对应的面的字母
	if key[0] in faces:
		#取相对应的颜色和axis
		face_color, axis = faces[key[0]]
		#如果字母后面有'就转90度，只有一个字母就转-90度
		angle = ((pi / 2) if len(key)>1 else -pi / 2)
		for r in arange(0, angle, angle / fps):
			rate(fps)
			for sticker in cubies:
				# 如果F，转前面，六个绿色三个红三个黄三个橘三个白
				if dot(sticker.pos, axis) > 0.5:
					sticker.rotate(angle=angle / fps, axis=axis,
								   origin=vector(0, 0, 0))




#记录信息
def turn(face,show=1):
	global d, u, f, b, r, l, uf, ur, ub, ul, df, dr, db, dl, fr, fl, br, bl, ufr, ufl, ubr, ubl, dfr, dfl, dbr, dbl
	# global turnNbr
	# turnNbr+=1
	# if show ==1:
	# 	sys.stdou.write(face+", ")
	if face=="R":
		ufr['u'], ufr['f'], ufr['r'], ubr['u'], ubr['b'], ubr['r'], dbr['d'], dbr['b'], dbr['r'], \
		dfr['d'], dfr['f'], dfr['r'] = dfr['f'], dfr['d'], dfr['r'], ufr['f'], ufr['u'], ufr['r'], \
									   ubr['b'], ubr['u'], ubr['r'], dbr['b'], dbr['d'], dbr['r']

		ur['u'], ur['r'], br['b'], br['r'], dr['d'], dr['r'], fr['f'], fr['r'], \
			= fr['f'], fr['r'], ur['u'], ur['r'], br['b'], br['r'], dr['d'], dr['r']
		rotate3D("R")

	if face=="R'":
		dfr['f'], dfr['d'], dfr['r'], ufr['f'], ufr['u'], ufr['r'], ubr['b'], ubr['u'], ubr['r'], \
		dbr['b'], dbr['d'],dbr['r']=ufr['u'], ufr['f'], ufr['r'], ubr['u'], ubr['b'], ubr['r'], \
									dbr['d'], dbr['b'], dbr['r'], dfr['d'], dfr['f'], dfr['r']

		ur['u'], ur['r'], fr['f'], fr['r'], dr['d'], dr['r'], br['b'], br['r']\
			=br['b'], br['r'], ur['u'], ur['r'], fr['f'], fr['r'], dr['d'], dr['r']
		rotate3D("R'")

	if face=="U":
		ufr['u'], ufr['f'], ufr['r'], ubr['u'], ubr['b'], ubr['r'], ubl['u'], ubl['b'], ubl['l'], \
		ufl['u'], ufl['f'],ufl['l']=ubr['u'], ubr['r'], ubr['b'], ubl['u'], ubl['l'], ubl['b'], \
									ufl['u'], ufl['l'], ufl['f'], ufr['u'], ufr['r'], ufr['f']

		ur['u'], ur['r'], uf['u'], uf['f'], ul['u'], ul['l'], ub['u'], ub['b']\
			=ub['u'], ub['b'], ur['u'], ur['r'], uf['u'], uf['f'], ul['u'], ul['l']
		rotate3D("U")

	if face=="U'":
		ubr['u'], ubr['r'], ubr['b'], ubl['u'], ubl['l'], ubl['b'], ufl['u'], ufl['l'], ufl['f'], \
		ufr['u'], ufr['r'], ufr['f']=ufr['u'], ufr['f'], ufr['r'], ubr['u'], ubr['b'], ubr['r'], \
									 ubl['u'], ubl['b'], ubl['l'], ufl['u'], ufl['f'], ufl['l']

		ur['u'], ur['r'], uf['u'], uf['f'], ul['u'], ul['l'], ub['u'], ub['b']\
			=uf['u'], uf['f'], ul['u'], ul['l'], ub['u'], ub['b'], ur['u'], ur['r']
		rotate3D("U'")

	if face=="D":
		dbr['d'], dbr['r'], dbr['b'], dbl['d'], dbl['l'], dbl['b'], dfl['d'], dfl['l'], dfl['f'], \
		dfr['d'], dfr['r'], dfr['f']=dfr['d'], dfr['f'], dfr['r'], dbr['d'], dbr['b'], dbr['r'], \
									 dbl['d'], dbl['b'], dbl['l'], dfl['d'], dfl['f'], dfl['l']

		dr['d'], dr['r'], df['d'], df['f'], dl['d'], dl['l'], db['d'], db['b']\
			=df['d'], df['f'], dl['d'], dl['l'], db['d'], db['b'], dr['d'], dr['r']
		rotate3D("D")

	if face=="D'":
		dfr['d'], dfr['f'], dfr['r'], dbr['d'], dbr['b'], dbr['r'], dbl['d'], dbl['b'], dbl['l'], \
		dfl['d'], dfl['f'], dfl['l']=dbr['d'], dbr['r'], dbr['b'], dbl['d'], dbl['l'], dbl['b'], \
									 dfl['d'], dfl['l'], dfl['f'], dfr['d'], dfr['r'], dfr['f']

		df['d'], df['f'], dr['d'], dr['r'], db['d'], db['b'], dl['d'], dl['l']\
			=dr['d'], dr['r'], db['d'], db['b'], dl['d'], dl['l'], df['d'], df['f']
		rotate3D("D'")

	if face=="L'":
		ufl['u'], ufl['f'], ufl['l'], ubl['u'], ubl['b'], ubl['l'], dbl['d'], dbl['b'], dbl['l'], \
		dfl['d'], dfl['f'], dfl['l']=dfl['f'], dfl['d'], dfl['l'], ufl['f'], ufl['u'], ufl['l'], \
									 ubl['b'], ubl['u'], ubl['l'], dbl['b'], dbl['d'], dbl['l']

		ul['u'], ul['l'], bl['b'], bl['l'], dl['d'], dl['l'], fl['f'], fl['l']\
			=fl['f'], fl['l'], ul['u'], ul['l'], bl['b'], bl['l'], dl['d'], dl['l']
		rotate3D("L'")

	if face=="L":
		dfl['f'], dfl['d'], dfl['l'], ufl['f'], ufl['u'], ufl['l'], ubl['b'], ubl['u'], ubl['l'], \
		dbl['b'], dbl['d'], dbl['l']=ufl['u'], ufl['f'], ufl['l'], ubl['u'], ubl['b'], ubl['l'],\
									 dbl['d'], dbl['b'], dbl['l'], dfl['d'], dfl['f'], dfl['l']

		ul['u'], ul['l'], fl['f'], fl['l'], dl['d'], dl['l'], bl['b'], bl['l']\
			=bl['b'], bl['l'], ul['u'], ul['l'], fl['f'], fl['l'], dl['d'], dl['l']
		rotate3D("L")

	if face=="F":
		ufr['u'], ufr['f'], ufr['r'], dfr['d'], dfr['f'], dfr['r'], dfl['d'], dfl['f'], dfl['l'], \
		ufl['u'], ufl['f'], ufl['l']=ufl['l'], ufl['f'], ufl['u'], ufr['r'], ufr['f'], ufr['u'], \
									 dfr['r'], dfr['f'], dfr['d'], dfl['l'], dfl['f'], dfl['d']

		uf['u'], uf['f'], fl['l'], fl['f'], df['d'], df['f'], fr['r'], fr['f']\
			=fl['l'], fl['f'], df['d'], df['f'], fr['r'], fr['f'], uf['u'], uf['f']
		rotate3D("F")

	if face=="F'":
		ufl['l'], ufl['f'], ufl['u'], ufr['r'], ufr['f'], ufr['u'], dfr['r'], dfr['f'], dfr['d'], \
		dfl['l'], dfl['f'], dfl['d']=ufr['u'], ufr['f'], ufr['r'], dfr['d'], dfr['f'], dfr['r'], \
									 dfl['d'], dfl['f'], dfl['l'], ufl['u'], ufl['f'], ufl['l']

		fl['l'], fl['f'], df['d'], df['f'], fr['r'], fr['f'], uf['u'], uf['f']\
			=uf['u'], uf['f'], fl['l'], fl['f'], df['d'], df['f'], fr['r'], fr['f']
		rotate3D("F'")

	if face=="B'":
		ubr['u'], ubr['b'], ubr['r'], dbr['d'], dbr['b'], dbr['r'], dbl['d'], dbl['b'], dbl['l'], \
		ubl['u'], ubl['b'], ubl['l']=ubl['l'], ubl['b'], ubl['u'], ubr['r'], ubr['b'], ubr['u'], \
									 dbr['r'], dbr['b'], dbr['d'], dbl['l'], dbl['b'], dbl['d']

		ub['u'], ub['b'], bl['l'], bl['b'], db['d'], db['b'], br['r'], br['b']\
			=bl['l'], bl['b'], db['d'], db['b'], br['r'], br['b'], ub['u'], ub['b']
		rotate3D("B'")

	if face=="B":
		ubl['l'], ubl['b'], ubl['u'], ubr['r'], ubr['b'], ubr['u'], dbr['r'], dbr['b'], dbr['d'], \
		dbl['l'], dbl['b'], dbl['d']=ubr['u'], ubr['b'], ubr['r'], dbr['d'], dbr['b'], dbr['r'], \
									 dbl['d'], dbl['b'], dbl['l'], ubl['u'], ubl['b'], ubl['l']

		bl['l'], bl['b'], db['d'], db['b'], br['r'], br['b'], ub['u'], ub['b']\
			=ub['u'], ub['b'], bl['l'], bl['b'], db['d'], db['b'], br['r'], br['b']
		rotate3D("B")


def printCube():
	print('\n\t'+ubl['u']+ub['u']+ubr['u']+'\n\t'+ul['u'] + u + ur['u']+'\n\t'+ufl['u'] + uf['u'] + ufr['u']+'\n')
	print(ubl['l'] + ul['l'] + ufl['l']+" "+ufl['f'] + uf['f'] + ufr['f']+" "+ufr['r'] + ur['r'] + ubr['r']+" "+ubr['b'] + ub['b'] + ubl['b'] + "\n" )
	print(bl['l'] + l + fl['l'] + " "+fl['f'] + f + fr['f'] + " "+fr['r'] + r + br['r'] + " "+br['b'] + b + bl['b'] + "\n")
	print(dbl['l'] + dl['l'] + dfl['l'] + " "+dfl['f'] + df['f'] + dfr['f'] + " "+dfr['r'] + dr['r'] + dbr['r'] + " "+dbr['b'] + db['b'] + dbl['b']+"\n")
	print("\t"+dfl['d'] + df['d'] + dfr['d']+ "\n\t" + dl['d'] + d + dr['d'] + "\n\t" + dbl['d'] + db['d'] + dbr['d'] + "\n")
	print("********************************************")





log = logging.getLogger(__name__)


Magenta=colorama.Fore.MAGENTA
time.sleep(2)
print(f"{Magenta}Please scan your cube")



color_RBG = {
        'red'    : color.red,
        'orange' :color.orange,
        'blue'   :color.blue,
        'green'  : color.green,
        'white'  : color.white,
        'yellow' :color.yellow
        }

color = {
        'red'    : (0,0,255),
        'orange' : (0,165,255),
        'blue'   : (255,0,0),
        'green'  : (0,255,0),
        'white'  : (255,255,255),
        'yellow' : (0,255,255)
        }

state=  {
            'up':['white','white','white','white','white','white','white','white','white',],
            'right':['white','white','white','white','white','white','white','white','white',],
            'front':['white','white','white','white','white','white','white','white','white',],
            'down':['white','white','white','white','white','white','white','white','white',],
            'left':['white','white','white','white','white','white','white','white','white',],
            'back':['white','white','white','white','white','white','white','white','white',]
        }
sign_conv={
            'green'  : 'F',
            'white'  : 'D',
            'blue'   : 'B',
            'red'    : 'L',
            'orange' : 'R',
            'yellow' : 'U'
          }
stickers = {
        'main': [  #scan时对准的小窗口
            [200, 120], [300, 120], [400, 120],
            [200, 220], [300, 220], [400, 220],
            [200, 320], [300, 320], [400, 320]
        ],
        'current': [ # 时刻都在闪烁的小cube
            [20, 20], [54, 20], [88, 20],
            [20, 54], [54, 54], [88, 54],
            [20, 88], [54, 88], [88, 88]
        ],
        # 'preview': [
        #     [20, 130], [54, 130], [88, 130],
        #     [20, 164], [54, 164], [88, 164],
        #     [20, 198], [54, 198], [88, 198]
        # ],
        'left': [
            [50, 280], [94, 280], [138, 280],
            [50, 324], [94, 324], [138, 324],
            [50, 368], [94, 368], [138, 368]
        ],
        'front': [
            [188, 280], [232, 280], [276, 280],
            [188, 324], [232, 324], [276, 324],
            [188, 368], [232, 368], [276, 368]
        ],
        'right': [
            [326, 280], [370, 280], [414, 280],
            [326, 324], [370, 324], [414, 324],
            [326, 368], [370, 368], [414, 368]
        ],
        'up': [
            [188, 128], [232, 128], [276, 128],
            [188, 172], [232, 172], [276, 172],
            [188, 216], [232, 216], [276, 216]
        ],
        'down': [
            [188, 434], [232, 434], [276, 434],
            [188, 478], [232, 478], [276, 478],
            [188, 522], [232, 522], [276, 522]
        ],
        'back': [
            [464, 280], [508, 280], [552, 280],
            [464, 324], [508, 324], [552, 324],
            [464, 368], [508, 368], [552, 368]
        ],
    }



font = cv2.FONT_HERSHEY_SIMPLEX    #CV_FONT_HERSHEY_SIMPLEX 正常大小无衬线字体。   CV_FONT_HERSHEY_SCRIPT_SIMPLEX -  手写风格字体。
#平面图每个面上的小字
textPoints=  {
            'front':[['F',242, 354],['G',(0,255,0),260,360]],
            'back':[['B',518, 354],['B',(255,0,0),536,360]],
            'down':[['D',242, 508],['W',(255,255,255),260,514]],
            'up': [['U', 242, 202], ['Y', (0, 255, 255), 260, 208]],
            'left':[['L',104, 354],['R',(0,0,255),122,360]],
            'right':[['R',380,354],['O',(0,165,255),398,360]],

        }
check_state=[]
solution=[]
solved=False

# VideoCapture()中参数是0，表示打开笔记本的内置摄像头，参数是视频文件路径则打开视频，如vc = cv2.VideoCapture("../testi.mp4")
cap=cv2.VideoCapture(0)
#cv2.namedWindow('read color')


def rotate2D(side):
    main=state[side]
    front=state['front']
    left=state['left']
    right=state['right']
    up=state['up']
    down=state['down']
    back=state['back']
    if side=='front':
        left[2],left[5],left[8],up[6],up[7],up[8],right[0],right[3],right[6],down[0],down[1],down[2]=down[0],down[1],down[2],left[8],left[5],left[2],up[6],up[7],up[8],right[6],right[3],right[0]
    elif side=='up':
        left[0],left[1],left[2],back[0],back[1],back[2],right[0],right[1],right[2],front[0],front[1],front[2]=front[0],front[1],front[2],left[0],left[1],left[2],back[0],back[1],back[2],right[0],right[1],right[2]
    elif side=='down':
        left[6],left[7],left[8],back[6],back[7],back[8],right[6],right[7],right[8],front[6],front[7],front[8]=back[6],back[7],back[8],right[6],right[7],right[8],front[6],front[7],front[8],left[6],left[7],left[8]
    elif side=='back':
        left[0],left[3],left[6],up[0],up[1],up[2],right[2],right[5],right[8],down[6],down[7],down[8]=up[2],up[1],up[0],right[2],right[5],right[8],down[8],down[7],down[6],left[0],left[3],left[6]
    elif side=='left':
        front[0],front[3],front[6],down[0],down[3],down[6],back[2],back[5],back[8],up[0],up[3],up[6]=up[0],up[3],up[6],front[0],front[3],front[6],down[6],down[3],down[0],back[8],back[5],back[2]
    elif side=='right':
        front[2],front[5],front[8],down[2],down[5],down[8],back[0],back[3],back[6],up[2],up[5],up[8]=down[2],down[5],down[8],back[6],back[3],back[0],up[8],up[5],up[2],front[2],front[5],front[8]

    main[0],main[1],main[2],main[3],main[4],main[5],main[6],main[7],main[8] = main[6],main[3],main[0],main[7],main[4],main[1],main[8],main[5],main[2]


def revrotate2D(side):   #rotate2D   revrotate2D
    main = state[side]
    front = state['front']
    left = state['left']
    right = state['right']
    up = state['up']
    down = state['down']
    back = state['back']
    if side=='front':
        left[2],left[5],left[8],up[6],up[7],up[8],right[0],right[3],right[6],down[0],down[1],down[2]=up[8],up[7],up[6],right[0],right[3],right[6],down[2],down[1],down[0],left[2],left[5],left[8]
    elif side=='up':
        left[0],left[1],left[2],back[0],back[1],back[2],right[0],right[1],right[2],front[0],front[1],front[2]=back[0],back[1],back[2],right[0],right[1],right[2],front[0],front[1],front[2],left[0],left[1],left[2]
    elif side=='down':
        left[6],left[7],left[8],back[6],back[7],back[8],right[6],right[7],right[8],front[6],front[7],front[8]=front[6],front[7],front[8],left[6],left[7],left[8],back[6],back[7],back[8],right[6],right[7],right[8]
    elif side=='back':
        left[0],left[3],left[6],up[0],up[1],up[2],right[2],right[5],right[8],down[6],down[7],down[8]=down[6],down[7],down[8],left[6],left[3],left[0],up[0],up[1],up[2],right[8],right[5],right[2]
    elif side=='left':
        front[0],front[3],front[6],down[0],down[3],down[6],back[2],back[5],back[8],up[0],up[3],up[6]=down[0],down[3],down[6],back[8],back[5],back[2],up[0],up[3],up[6],front[0],front[3],front[6]
    elif side=='right':
        front[2],front[5],front[8],down[2],down[5],down[8],back[0],back[3],back[6],up[2],up[5],up[8]=up[2],up[5],up[8],front[2],front[5],front[8],down[8],down[5],down[2],back[6],back[3],back[0]

    main[0],main[1],main[2],main[3],main[4],main[5],main[6],main[7],main[8]=main[2],main[5],main[8],main[1],main[4],main[7],main[0],main[3],main[6]


answer_string=[]
def solve(state):
    raw=''
    for i in state:
        for j in state[i]:
            raw+=sign_conv[j]
    print(raw)
    print("answer:,",kociemba.solve(raw))
    answer_string=kociemba.solve(raw)
    return answer_string




blue_low=[90, 43,46]
blue_high=[125, 255, 255]
red_low=[140, 40, 40]
red_high=[180, 255, 255]
yellow_low=[20, 40, 40]
yellow_high=[30, 255, 255]
orange_low=[0, 40, 40]
orange_high=[20, 255, 255]
green_low=[45, 40, 40]
green_high=[95, 255, 255]
white_low=[0, 0, 100]
white_high=[180, 30, 255]



def color_detect(h,s,v):
    # if h <= 8 and s>=43 and v>=46 :
    #     return 'red'
    # elif h <=13 and h>=0 and s>=40 and v>=40:
    #     return 'orange'
    # elif h <= 35  and h>=20 and s>=43 and v>=46:
    #     return 'yellow'
    # elif h<= 77 and h>=35 and s>=43 and v>=46:
    #     return 'green'
    # elif h <= 124 and h>=77 and s>=43 and v>=46:
    #     return 'blue'
    # elif h <= 180 and s<=30 and v>=100:
    #     return 'white'
    # return 'white'

    if h <= 8 and s>=5 :
        return 'red'
    elif h <=13 and h>=0:
        return 'orange'
    elif h <= 35  and h>=20 and s>=43 and v>=46:
        return 'yellow'
    elif h<= 85 and h>=70 and s>=43 and v>=46:
        return 'green'
    elif h <= 130 and h>=77 and s>=43 and v>=46:
        return 'blue'
    elif h <= 180 and s<=30 and v>=100:
        return 'white'
    return 'white'

    # if h < 5 and s>5 :
    #     return 'red'
    # elif h <10 and h>=3:
    #     return 'orange'
    # elif h <= 25 and h>10:
    #     return 'yellow'
    # elif h>=70 and h<= 85 and s>100 and v<180:
    #     return 'green'
    # elif h <= 130 and s>70:
    #     return 'blue'
    # elif h <= 100 and s<10 and v<200:
    #     return 'white'
    # return 'white'


# cv2.rectangle(在什么图片上画矩形, 左上角坐标,右下角坐标, 颜色, 矩形边框粗细（-1代表CV_FILLED填充）)
# 画左边不断闪烁的小正方形，和识别用的小正方形的方法
def draw_strickers(frame,stickers,name):
    for x, y in stickers[name]:
        cv2.rectangle(frame,(x,y),(x+30, y+30),(255,255,255),2)


# 画二维展开图的方法(白色的边框)
def draw_preview_stickers(frame,stickers):
        stick=['front','back','left','right','up','down']
        for name in stick:
            for x,y in stickers[name]:
                cv2.rectangle(frame, (x,y), (x+40, y+40), (255,255,255), 2)


# 画展开图赏的字母
def texton_preview_stickers(frame,stickers):
        stick=['front','back','left','right','up','down']
        for name in stick:
            for x,y in stickers[name]:
                sym,x1,y1=textPoints[name][0][0],textPoints[name][0][1],textPoints[name][0][2]
                cv2.putText(preview, sym, (x1,y1), font,1,(0, 0, 0), 1, cv2.LINE_AA)
                sym,col,x1,y1=textPoints[name][1][0],textPoints[name][1][1],textPoints[name][1][2],textPoints[name][1][3]
                cv2.putText(preview, sym, (x1,y1), font,0.5,col, 1, cv2.LINE_AA)
# void cv::putText(
# 		cv::Mat& img, // 待绘制的图像
# 		const string& text, // 待绘制的文字
# 		cv::Point origin, // 文本框的左下角
# 		int fontFace, // 字体 (如cv::FONT_HERSHEY_PLAIN)
# 		double fontScale, // 尺寸因子，值越大文字越大
# 		cv::Scalar color, // 线条的颜色（RGB）
# 		int thickness = 1, // 线条宽度
# 		int lineType = 8, // 线型（4邻域或8邻域，默认8邻域）
# 		bool bottomLeftOrigin = false // true='origin at lower left'
# 	);
# linetype：线条的类型，8 连接，抗锯齿等。默认情况是 8 连接。cv2.LINE_AA 为抗锯齿，这样看起来会非常平滑。


# 画二维展开图的方法(白色边框里面的白色，把粗细改成-1就是填充效果)
def fill_stickers(frame,stickers,sides):  # 传进的sides是当前的state
    for side,colors in sides.items():
        num=0
        for x,y in stickers[side]:
            cv2.rectangle(frame,(x,y),(x+40,y+40),color[colors[num]],-1)
            if side == 'down':
                cv2.rectangle(frame, (232, 478), (232 + 40, 478 + 40), (255, 255, 255), -1)
            num+=1
# for key,values in  dict.items()


def process(operation):
    # 传入kocimba得来的解法string，传入，转动的操作
    replace={
                "F":[rotate2D,'front'],
                "F2":[rotate2D,'front','front'],
                "F'":[revrotate2D,'front'],
                "U":[rotate2D,'up'],
                "U2":[rotate2D,'up','up'],
                "U'":[revrotate2D,'up'],
                "L":[rotate2D,'left'],
                "L2":[rotate2D,'left','left'],
                "L'":[revrotate2D,'left'],
                "R":[rotate2D,'right'],
                "R2":[rotate2D,'right','right'],
                "R'":[revrotate2D,'right'],
                "D":[rotate2D,'down'],
                "D2":[rotate2D,'down','down'],
                "D'":[revrotate2D,'down'],
                "B":[rotate2D,'back'],
                "B2":[rotate2D,'back','back'],
                "B'":[revrotate2D,'back']
    }
    a=0
    for i in operation:
        for j in range(len(replace[i])-1):
            replace[i][0](replace[i][j+1])

        cv2.putText(preview, i, (700,a+50), font,1,(0,255,0), 1, cv2.LINE_AA)
        fill_stickers(preview,stickers,state)
        solution.append(preview)  #把所有算法都放进一个string
        cv2.imshow('solution',preview)
        cv2.waitKey()
        cv2.putText(preview, i, (700,50), font,1,(0,0,0), 1, cv2.LINE_AA)




def search_serial_ports():
    if sys.platform.startswith('win'):
        ports=['COM%s'% (i+1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        ports=glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        ports=glob.glob('/dev/tty.*')
    else:
        raise EnvironmentError("unsupported platform!(windows,mac,linux,cygwin are supported!)")
    result=[]
    for port in ports:
        try:
            s=serial.Serial(port)
            s.close()
            result.append(port)
        except(OSError, serial.SerialException):
            pass
    return result

# if __name__=='__main__':


# 展开图的大小
preview=np.zeros((700,800,3),np.uint8)
# img = np.zeros([400, 400, 3], np.uint8)
#zeros:double类零矩阵  创建400*400 3个通道的矩阵图像 参数时classname为uint8

while True:
    hsv=[]
    current_state=[]
    # flag, img_rd = cv2.VideoCapture(0).read()
    # 功能：读取一帧的图片
    # 参数：无
    # 返回值：flag：bool值：True：读取到图片，
    # 　　　　　　　　　　　False：没有读取到图片
    # 　　　　img_rd：一帧的图片
    ret,img=cap.read()
    # cv2.imread()和cv2.cvtColor()的使用
    # cv2.imread()
    # 接口读图像，读进来直接是BGR
    # 格式数据格式在0~255
    # 需要特别注意的是图片读出来的格式是BGR，不是我们最常见的RGB格式，颜色肯定有区别。
    # cv2.cvtColor(p1, p2)
    # 是颜色空间转换函数，p1是需要转换的图片，p2是转换成何种格式。
    # cv2.COLOR_BGR2RGB：将BGR格式转换成RGB格式
    # cv2.COLOR_BGR2GRAY：将BGR格式转换成灰度图片
    frame=cv2.cvtColor(img,cv2.COLOR_BGR2HSV) #现在是rgb，frame是rbg版的img
    #frame=cv2.GaussianBlur(frame,frame,)

    #mask=np.zeros(frame.shape,dtype=np.uint8)
    # 画scan对准的小矩形
    draw_strickers(img,stickers,'main')
    # 画时刻都在闪烁的小cube
    draw_strickers(img,stickers,'current')

    # 画展开图的边框，里面的填充，还有字母
    draw_preview_stickers(preview,stickers)
    fill_stickers(preview,stickers,state)
    texton_preview_stickers(preview,stickers)

    # 读取检测的小矩形的hsv值
    for i in range(9):
        #读取frame的像素的hsv，先是行的index（y），再是列的index（x）
        hsv.append(frame[stickers['main'][i][1] + 10][stickers['main'][i][0] + 10])



    # 闪烁的小矩形填充颜色
    a=0
    for x,y in stickers['current']:
        color_name=color_detect(hsv[a][0],hsv[a][1],hsv[a][2])
        cv2.rectangle(img,(x,y),(x+30,y+30),color[color_name],-1)
        a+=1
        current_state.append(color_name)


    k=cv2.waitKey(5)&0xFF   #按键对应的ASCII码值并不一定仅仅只有8位，同一按键对应的ASCII并不一定相同（但是后8位一定相同）,引用&0xff，正是为了只取按键对应的ASCII值后8位来排除不同按键的干扰进行判断按键是什么。
    if k==27:   #ESC
        break;
    elif k==ord('u'):
        state['up']=current_state
        print(current_state)
        check_state.append('u')
    elif k ==ord('r'):
        check_state.append('r')
        print(current_state)
        state['right']=current_state
    elif k ==ord('l'):
        check_state.append('l')
        print(current_state)
        state['left']=current_state
    elif k ==ord('d'):
        check_state.append('d')
        print(current_state)
        state['down']=current_state
        state['down'][4]='white'
    elif k ==ord('f'):
        check_state.append('f')
        print(current_state)
        state['front']=current_state
    elif k ==ord('b'):
        check_state.append('b')
        print(current_state)
        state['back']=current_state
    elif k ==ord('c'):
        if len(set(check_state)) == 6:
            print(state)
            newCube(state)
            printCube()
        else:
            print("all side are not scanned check other window for finding which left to be scanned?")
            print("left to scan:", 6 - len(set(check_state)))

    elif k==ord('\r'):
        if len(set(check_state))==6:
            try:
                solved=solve(state)
                if solved:
                    operation=solved.split(' ')
                    rotateCube(operation)
                    answerchange = []
                    for i in range(len(operation)):
                        answerchange.append(operation[i])
                        if len(answerchange[i]) == 1:
                            answerchange[i] = answerchange[i] + '1'
                        if len(answerchange[i]) == 2:
                            if answerchange[i][1] == "'":
                                answerchange[i] = answerchange[i][0] + '3'

                    print(answerchange)
                    # 连接串口
                    com=search_serial_ports()
                    #115200是波特率
                    serial = serial.Serial(com[0], 115200, timeout=2)  # 连接COM14,波特率位115200
                    if serial.isOpen():
                        print('串口已打开')
                        # 说白了Python3的字符串的编码语言用的是unicode编码，由于Python的字符串类型是str，
                        # 在内存中以Unicode表示，一个字符对应若干字节，如果要在网络上传输，
                        # 或保存在磁盘上就需要把str变成以字节为单位的bytes
                        # python对bytes类型的数据用带b前缀的单引号或双引号表示：
                        data = bytes(answerchange,encoding='utf-8')  # 发送的数据
                        serial.write(data)  # 串口写数据
                        serial.write(b'\r\n')#为了配合下位机，用0X0D 0X0A做结束标志
                        print('You Send Data:', data)
                        while True:
                            data = serial.read(20)  # 串口读20位数据
                            if data != b'':
                                break
                        print('receive data is :', data)
                    else:
                        print('串口未打开')
                    serial.close()
                    if serial.isOpen():
                        print('串口未关闭')
                    else:
                        print('串口已关闭')
                    print(operation)
                    process(operation)
            except:
                print("error in side detection ,you may do not follow sequence or some color not detected well.Try again")
        else:
            print("all side are not scanned check other window for finding which left to be scanned?")
            print("left to scan:",6-len(set(check_state)))
    cv2.imshow('preview',preview)  #平面图的窗口
    cv2.imshow('frame',img[0:500,0:500])  #scan颜色的窗口




cv2.destroyALLWindows()



