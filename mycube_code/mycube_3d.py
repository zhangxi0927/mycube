from vpython import *
import sys
import serial
import glob
import random
import kociemba
import numpy as np
import cv2
fps=12
turnNumber=0

scene.title = 'cube'  # 设置窗口标题

faces={'F': (color.green, vector(0, 0, 1)),
	   'B': (color.blue, vector(0, 0, -1)),
	   'U': (color.yellow, vector(0, 1, 0)),
	   'L': (color.red, vector(-1, 0, 0)),
	   'D': (color.white, vector(0, -1, 0)),
	   'R': (color.orange, vector(1, 0, 0))}

stickers = []
for face_color,face_axis in faces.values():
	for x in (-1,0,1):
		for y in (-1,0,1):
			# 每个颜色的面先形成同一个位置的面，z=1。5
			sticker=box(color=face_color,pos=vector(x,y,1.5),length=0.98,height=0.98,width=0.05)
			# 计算旋转角度，除了正面和背面，都需要转90
			cos_angle=dot(vector(0,0,1),face_axis)
			# 计算旋转轴
			pivot=(cross(vector(0,0,1),face_axis) if cos_angle==0 else vector(1,0,0))
			# origin是起始位置，从起始点到旋转物体这么个轴，围绕axis，旋转angle
			sticker.rotate(angle=acos(cos_angle),axis=pivot,origin=vector(0,0,0))
			stickers.append(sticker)
			#print(sticker.pos,sticker.color)




# Rotate parts of the cube in 3 dimensions
def rotate3D(key):
	#输入的是对应的面的字母
	if key[0] in faces:
		#取相对应的颜色和axis
		face_color, axis = faces[key[0]]
		#如果字母后面有'就转90度，只有一个字母就转-90度
		angle = ((pi / 2) if len(key)>1 else -pi / 2)
		for r in arange(0, angle, angle / fps):
			rate(fps)
			for sticker in stickers:
				# 如果F，转前面，六个绿色三个红三个黄三个橘三个白
				if dot(sticker.pos, axis) > 0.5:
					sticker.rotate(angle=angle / fps, axis=axis,
								   origin=vector(0, 0, 0))
	elif key[0] == 'E': #from right to left
		axis = vector(0, 0.5, 0)
		angle = ((pi / 2) if len(key)>1 else -pi / 2)
		for r in arange(0, angle, angle / fps):
			rate(fps)
			for sticker in stickers:
				sticker.rotate(angle=angle / fps, axis=axis,origin=vector(0, 0, 0))



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



def turnCube(show=1):#from right to left
	global d, u, f, b, r, l, uf, ur, ub, ul, df, dr, db, dl, fr, fl, br, bl, ufr, ufl, ubr, ubl, dfr, dfl, dbr, dbl
	f,r,b,l=r,b,l,f
	ufr['u'], ufr['f'], ufr['r'], ubr['u'], ubr['b'], ubr['r'], \
	ubl['u'], ubl['b'], ubl['l'], ufl['u'], ufl['f'], ufl['l']\
		=ubr['u'], ubr['r'], ubr['b'], ubl['u'], ubl['l'], ubl['b'], \
		 ufl['u'], ufl['l'], ufl['f'], ufr['u'], ufr['r'], ufr['f']

	dfr['d'], dfr['f'], dfr['r'], dbr['d'], dbr['b'], dbr['r'], \
	dbl['d'], dbl['b'], dbl['l'], dfl['d'], dfl['f'], dfl['l']\
		=dbr['d'], dbr['r'], dbr['b'], dbl['d'], dbl['l'], dbl['b'], \
		dfl['d'], dfl['l'], dfl['f'], dfr['d'], dfr['r'], dfr['f']

	ur['u'], ur['r'], uf['u'], uf['f'], ul['u'], ul['l'], ub['u'], ub['b']\
		=ub['u'], ub['b'], ur['u'], ur['r'], uf['u'], uf['f'], ul['u'], ul['l']

	df['d'], df['f'], dr['d'], dr['r'], db['d'], db['b'], dl['d'], dl['l']\
		=dr['d'], dr['r'], db['d'], db['b'], dl['d'], dl['l'], df['d'], df['f']

	fl['f'], fl['l'], fr['f'], fr['r'], br['b'], br['r'], bl['b'], bl['l']\
		=fr['r'], fr['f'], br['r'], br['b'], bl['l'], bl['b'], fl['l'], fl['f']

	rotate3D("E")
	if show==1:
		print("turn the cube")




def resetCube():
	global d, u, f, b, r, l, uf, ur, ub, ul, df, dr, db, dl, fr, fl, br, bl, ufr, ufl, ubr, ubl, dfr, dfl, dbr, dbl

	d = 'w'
	u = 'y'
	f = 'g'
	b = 'b'
	r = 'o'
	l = 'r'

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

	ufr = {'u': 'y', 'd': '', 'f': 'g', 'b': '', 'r': 'o', 'l': ''}
	ufl = {'u': 'y', 'd': '', 'f': 'g', 'b': '', 'r': '', 'l': 'r'}
	ubr = {'u': 'y', 'd': '', 'f': '', 'b': 'b', 'r': 'o', 'l': ''}
	ubl = {'u': 'y', 'd': '', 'f': '', 'b': 'b', 'r': '', 'l': 'r'}
	dfr = {'u': '', 'd': 'w', 'f': 'g', 'b': '', 'r': 'o', 'l': ''}
	dfl = {'u': '', 'd': 'w', 'f': 'g', 'b': '', 'r': '', 'l': 'r'}
	dbr = {'u': '', 'd': 'w', 'f': '', 'b': 'b', 'r': 'o', 'l': ''}
	dbl = {'u': '', 'd': 'w', 'f': '', 'b': 'b', 'r': '', 'l': 'r'}
	printCube()



def isFinished():
	global d, u, f, b, r, l, uf, ur, ub, ul, df, dr, db, dl, fr, fl, br, bl, ufr, ufl, ubr, ubl, dfr, dfl, dbr, dbl
	if d == 'w' and u == 'y' and f == 'g' and b == 'b' and r == 'o' and l == 'r' and \
			uf == {'u': 'y', 'd': '', 'f': 'g', 'b': '', 'r': '', 'l': ''} and \
			ur == {'u': 'y', 'd': '', 'f': '', 'b': '', 'r': 'o', 'l': ''} and \
			ub == {'u': 'y', 'd': '', 'f': '', 'b': 'b', 'r': '', 'l': ''} and \
			ul == {'u': 'y', 'd': '', 'f': '', 'b': '', 'r': '', 'l': 'r'} and \
			df == {'u': '', 'd': 'w', 'f': 'g', 'b': '', 'r': '', 'l': ''} and \
			dr == {'u': '', 'd': 'w', 'f': '', 'b': '', 'r': 'o', 'l': ''} and \
			db == {'u': '', 'd': 'w', 'f': '', 'b': 'b', 'r': '', 'l': ''} and \
			dl == {'u': '', 'd': 'w', 'f': '', 'b': '', 'r': '', 'l': 'r'} and \
			fr == {'u': '', 'd': '', 'f': 'g', 'b': '', 'r': 'o', 'l': ''} and \
			fl == {'u': '', 'd': '', 'f': 'g', 'b': '', 'r': '', 'l': 'r'} and \
			br == {'u': '', 'd': '', 'f': '', 'b': 'b', 'r': 'o', 'l': ''} and \
			bl == {'u': '', 'd': '', 'f': '', 'b': 'b', 'r': '', 'l': 'r'} and \
			ufr == {'u': 'y', 'd': '', 'f': 'g', 'b': '', 'r': 'o', 'l': ''} and \
			ufl == {'u': 'y', 'd': '', 'f': 'g', 'b': '', 'r': '', 'l': 'r'} and \
			ubr == {'u': 'y', 'd': '', 'f': '', 'b': 'b', 'r': 'o', 'l': ''} and \
			ubl == {'u': 'y', 'd': '', 'f': '', 'b': 'b', 'r': '', 'l': 'r'} and \
			dfr == {'u': '', 'd': 'w', 'f': 'g', 'b': '', 'r': 'o', 'l': ''} and \
			dfl == {'u': '', 'd': 'w', 'f': 'g', 'b': '', 'r': '', 'l': 'r'} and \
			dbr == {'u': '', 'd': 'w', 'f': '', 'b': 'b', 'r': 'o', 'l': ''} and \
			dbl == {'u': '', 'd': 'w', 'f': '', 'b': 'b', 'r': '', 'l': 'r'}:
		return 1
	else:
		return 0


def scramble(scranbleNum=10,show=1):
    allMoves=["R","R'","L","L'","U","U'","D","D'","F","F'","B","B'"]
    i=0
    firstScramble = []
    for i in range(scranbleNum):
        m_index=random.randint(0,len(allMoves)-1)
        m=allMoves[m_index]
        firstScramble.append(m)
        turn(m)
        print(i," ",m)
        printCube()
    print(firstScramble)

sign_conv={
	'g' : 'F',
    'y'  : 'U',
    'b'   : 'B',
    'o'    : 'R',
    'r' : 'L',
    'w' : 'D'
}

def solveByKociemba(state):
	raw = ''
	for i in state:
		for j in state[i]:
			raw += sign_conv[j]
	print(raw)
	print("answer:", kociemba.solve(raw))
	return kociemba.solve(raw)

stateForKociemba=  {
	'up' : [ubl['u'],ub['u'],ubr['u'],ul['u'],u,ur['u'],ufl['u'],uf['u'],ufr['u']],
    'right': [ufr['r'], ur['r'], ubr['r'], fr['r'], r, br['r'], dfr['r'], dr['r'], dbr['r']],
    'front':[ufl['f'],uf['f'],ufr['f'],fl['f'],f,fr['f'],dfl['f'],df['f'],dfr['f']],
    'down':[dfl['d'],df['d'],dfr['d'],dl['d'],d,dr['d'],dbl['d'],db['d'],dbr['d']],
    'left':[ubl['l'],ul['l'],ufl['l'],bl['l'],l,fl['l'],dbl['l'],dl['l'],dfl['l']],
    'back':[ubr['b'],ub['b'],ubl['b'],br['b'],b,bl['b'],dbr['b'],db['b'],dbl['b']]
    # 'up':['y','y','y','y','y','y','y','y','y',],
    # 'right':['o','o','o','o','o','o','o','o','o',],
    # 'front':['g','g','g','g','g','g','g','g','g',],
    # 'down':['w','w','w','w','w','w','w','w','w',],
    # 'left':['r','r','r','r','r','r','r','r','r',],
    # 'back':['b','b','b','b','b','b','b','b','b',]
}

def solveMove(answer):
	for i in range(len(answer)):
		move=answer[i]
		print(move)
		print(len(move))
		if len(move)>1 and move[1]=='2':
			turn(move[0])
			turn(move[0])
		else:
			turn(move)
		print(i," ",move)
		printCube()


def printCube():
	print('\n\t'+ubl['u']+ub['u']+ubr['u']+'\n\t'+ul['u'] + u + ur['u']+'\n\t'+ufl['u'] + uf['u'] + ufr['u']+'\n')
	print(ubl['l'] + ul['l'] + ufl['l']+" "+ufl['f'] + uf['f'] + ufr['f']+" "+ufr['r'] + ur['r'] + ubr['r']+" "+ubr['b'] + ub['b'] + ubl['b'] + "\n" )
	print(bl['l'] + l + fl['l'] + " "+fl['f'] + f + fr['f'] + " "+fr['r'] + r + br['r'] + " "+br['b'] + b + bl['b'] + "\n")
	print(dbl['l'] + dl['l'] + dfl['l'] + " "+dfl['f'] + df['f'] + dfr['f'] + " "+dfr['r'] + dr['r'] + dbr['r'] + " "+dbr['b'] + db['b'] + dbl['b']+"\n")
	print("\t"+dfl['d'] + df['d'] + dfr['d']+ "\n\t" + dl['d'] + d + dr['d'] + "\n\t" + dbl['d'] + db['d'] + dbr['d'] + "\n")
	print("********************************************")

# from PIL import ImageGrab
# import numpy as np
# import cv2 as cv
# import imageio
# import time
# cv.namedWindow("grab", cv.WINDOW_NORMAL)
# buff = []
# size = (0, 0, 1200, 1200)
# p = ImageGrab.grab(size)
# x, y = p.size
# while True:
#         im = ImageGrab.grab(size)
#         img = cv.cvtColor(np.array(im), cv.COLOR_RGB2BGR)
#         # video.write(img)
#         cv.imshow("grab", img)
#         buff.append(img)
#         if cv.waitKey(1) & 0xFF == ord('q'):
#             break

scramble()
while True:
	evt=scene.waitfor('keydown')
	command=evt.key
	if command=="F":
		turn("F")
	elif command=="B":
		turn("B")
	elif command=="U":
		turn("U")
	elif command=="D":
		turn("D")
	elif command=="R":
		turn("R")
	elif command=="L":
		turn("L")
	elif command=="f":
		turn("F'")
	elif command=="b":
		turn("B'")
	elif command=="u":
		turn("U'")
	elif command=="d":
		turn("D'")
	elif command=="r":
		turn("R'")
	elif command=="l":
		turn("L'")
	elif command=="E":
		turnCube()
	elif command=="q":
		break
	else:
		continue


	# command=input("enter your command: ")
	# if command=="F":
	# 	turn("F")
	# elif command=="B":
	# 	turn("B")
	# elif command=="U":
	# 	turn("U")
	# elif command=="D":
	# 	turn("D")
	# elif command=="R":
	# 	turn("R")
	# elif command=="L":
	# 	turn("L")
	# elif command=="F'":
	# 	turn("F'")
	# elif command=="B'":
	# 	turn("B'")
	# elif command=="U'":
	# 	turn("U'")
	# elif command=="D'":
	# 	turn("D'")
	# elif command=="R'":
	# 	turn("R'")
	# elif command=="L'":
	# 	turn("L'")
	# elif command=="E":
	# 	turnCube()
	# elif command=="E'":
	# 	turnCube()
	# elif command=="quit":
	# 	break

	printCube()

stateForKociemba=  {
	'up' : [ubl['u'],ub['u'],ubr['u'],ul['u'],u,ur['u'],ufl['u'],uf['u'],ufr['u']],
    'right': [ufr['r'], ur['r'], ubr['r'], fr['r'], r, br['r'], dfr['r'], dr['r'], dbr['r']],
    'front':[ufl['f'],uf['f'],ufr['f'],fl['f'],f,fr['f'],dfl['f'],df['f'],dfr['f']],
    'down':[dfl['d'],df['d'],dfr['d'],dl['d'],d,dr['d'],dbl['d'],db['d'],dbr['d']],
    'left':[ubl['l'],ul['l'],ufl['l'],bl['l'],l,fl['l'],dbl['l'],dl['l'],dfl['l']],
    'back':[ubr['b'],ub['b'],ubl['b'],br['b'],b,bl['b'],dbr['b'],db['b'],dbl['b']]
    # 'up':['y','y','y','y','y','y','y','y','y',],
    # 'right':['o','o','o','o','o','o','o','o','o',],
    # 'front':['g','g','g','g','g','g','g','g','g',],
    # 'down':['w','w','w','w','w','w','w','w','w',],
    # 'left':['r','r','r','r','r','r','r','r','r',],
    # 'back':['b','b','b','b','b','b','b','b','b',]
}
print(stateForKociemba)

# while True:
# 	command=input("enter your command: ")
# 	print(command)
# 	print(type(command))
# 	print(command[0])
# 	if command=="F":
# 		rotate3D("F")
# 	elif command=="B":
# 		rotate3D("B")
# 	elif command=="U":
# 		rotate3D("U")
# 	elif command=="D":
# 		rotate3D("D")
# 	elif command=="R":
# 		rotate3D("R")
# 	elif command=="L":
# 		rotate3D("L")
# 	elif command=="F'":
# 		rotate3D("F'")
# 	elif command=="B'":
# 		rotate3D("B'")
# 	elif command=="U'":
# 		rotate3D("U'")
# 	elif command=="D'":
# 		rotate3D("D'")
# 	elif command=="R'":
# 		rotate3D("R'")
# 	elif command=="L'":
# 		rotate3D("L'")
# 	elif command=="E":
# 		rotate3D("E'")
# 	elif command=="E'":
# 		rotate3D("E'")
# 	elif command=="quit":
# 		break
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


answer=solveByKociemba(stateForKociemba)
answer=answer.split()
print(answer)
solveMove(answer)
# # 连接串口
# com=search_serial_ports()
# #115200是波特率
# serial = serial.Serial(com[0], 115200, timeout=2)  # 连接COM14,波特率位115200
# if serial.isOpen():
# 	print('串口已打开')
# 	# 说白了Python3的字符串的编码语言用的是unicode编码，由于Python的字符串类型是str，
# 	# 在内存中以Unicode表示，一个字符对应若干字节，如果要在网络上传输，
# 	# 或保存在磁盘上就需要把str变成以字节为单位的bytes
# 	# python对bytes类型的数据用带b前缀的单引号或双引号表示：
# 	data = bytes(answer, encoding='utf-8')  # 发送的数据
# 	serial.write(data)  # 串口写数据
# 	serial.write(b'\r\n')  # 为了配合下位机，用0X0D 0X0A做结束标志
# 	print('You Send Data:', data)
# 	while True:
# 		data = serial.read(20)  # 串口读20位数据
# 		if data != b'':
# 			break
# 	print('receive data is :', data)
# else:
# 	print('串口未打开')
# serial.close()
# if serial.isOpen():
# 	print('串口未关闭')
# else:
# 	print('串口已关闭')
