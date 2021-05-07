import pygame, sys
from random import randrange
from pygame.locals import *

pygame.init()
fps = pygame.time.Clock()
bomb = pygame.image.load("bomb.png")
pygame.display.set_icon(bomb)
surfObj = pygame.display.set_mode((173, 200))
pygame.display.set_caption("Minesweeper")

red = pygame.Color(255, 0, 0)
green = pygame.Color(0, 255, 0)

blue = pygame.Color(0, 0, 255)
white = pygame.Color(255, 255, 255)
black = pygame.Color(0, 0, 0)

font = pygame.font.Font("UniversLTStd-BoldEx.otf", 18)

blockSurf = pygame.image.load("block.png")
blockSurfSel = pygame.image.load("selblock.png")
blockSurfBlank = pygame.image.load("blankblock.png")

warn1 = pygame.image.load("block1.png")
warn2 = pygame.image.load("block2.png")
warn3 = pygame.image.load("block3.png")
warn4 = pygame.image.load("block4.png")
warn5 = pygame.image.load("block5.png")
warn6 = pygame.image.load("block6.png")
warn7 = pygame.image.load("block7.png")
warn8 = pygame.image.load("block8.png")
explode = pygame.image.load("explode.png")
flag = pygame.image.load("flag.png")
question = pygame.image.load("question.png")

clock = pygame.image.load("time.png")

boxes = []
numBombs = 0

class box():
	#flag = -3 # -3 = NO FLAG; -2 = FLAGGED; -1 = ?; 0 = BLANK; 1-8 = WARN; 9 = Exploded
	isBomb = False
	index = 0
	x = 0
	y = 0
	def __init__(self, boxPos):
		self.boxP = boxPos
		self.flag = -3

refBlock = box(Rect(-100,-100,0,0))
refBlock.x = -10
refBlock.y = -10
selBlock = refBlock

def drawBox():
	pygame.draw.line(surfObj, black, (10, 10), (163, 10))
	pygame.draw.line(surfObj, black, (10, 10), (10, 163))
	pygame.draw.line(surfObj, black, (10, 163), (163, 163))
	pygame.draw.line(surfObj, black, (163, 10), (163, 163))

def drawBoxesInit():
	for x in range(0, 9):
		for y in range(0, 9):
			bo = box(Rect(x*17+10, y*17+10, 17, 17))
			bo.index = len(boxes)
			bo.x = x
			bo.y = y
			boxes.append(bo)
			surfObj.blit(blockSurf, (x*17 + 10, y*17 + 10))

drawBoxesInit()

def pickBombs():
	global numBombs
	while numBombs < 10:
		x = randrange(0, len(boxes))
		if not boxes[x].isBomb:
			boxes[x].isBomb = True
			numBombs += 1

pickBombs()
flagsUsed = 0
checkedBoxes = []
blocksLeft = 0

def drawBoxes():
	global flagsUsed
	global blocksLeft
	flagsUsed = 0
	blocksLeft = 0
	for b in boxes:
		if b.flag == -3:
			blocksLeft += 1
			surfObj.blit(blockSurf, b.boxP)
		elif b.flag == 0:
			if not b in checkedBoxes:
				pathFind(b)
			surfObj.blit(blockSurfBlank, b.boxP)
		elif b.flag == 9:
			surfObj.blit(explode, b.boxP)
			lose()
		elif b.flag == -2:
			surfObj.blit(flag, b.boxP)
			flagsUsed += 1
		elif b.flag == -1: surfObj.blit(question, b.boxP)
		elif b.flag == 1: surfObj.blit(warn1, b.boxP)
		elif b.flag == 2: surfObj.blit(warn2, b.boxP)
		elif b.flag == 3: surfObj.blit(warn3, b.boxP)
		elif b.flag == 4: surfObj.blit(warn4, b.boxP)
		elif b.flag == 5: surfObj.blit(warn5, b.boxP)
		elif b.flag == 6: surfObj.blit(warn6, b.boxP)
		elif b.flag == 7: surfObj.blit(warn7, b.boxP)
		elif b.flag == 8: surfObj.blit(warn8, b.boxP)
	if blocksLeft == 10: win()


def isInBounds():
	return Rect(10, 10, 153, 153).collidepoint(e.pos)

def overBlock():
	for b in boxes:
		if b.boxP.collidepoint(e.pos):
			return b

def boxAt(x, y):
	for b in boxes:
		if b.x == x and b.y == y:
			return b

def warnInteger(b):
	try:
		if b.x < 9 and b.x > 0 and b.y > 0 and b.y < 9:
			return (boxAt(b.x - 1, b.y), boxAt(b.x + 1, b.y), boxAt(b.x, b.y - 1), boxAt(b.x, b.y + 1), boxAt(b.x - 1, b.y - 1), boxAt(b.x + 1, b.y +1), boxAt(b.x + 1, b.y - 1), boxAt(b.x - 1, b.y + 1))
		elif b.x > 8 and b.y > 0 and b.y < 9:
			return (boxAt(b.x - 1, b.y), boxAt(b.x - 1, b.y - 1), boxAt(b.x - 1, b.y + 1))
		elif b.x < 1 and b.y > 0 and b.y < 9:
			return (boxAt(b.x + 1, b.y), boxAt(b.x + 1, b.y - 1), boxAt(b.x + 1, b.y + 1), boxAt(b.x, b.y+1), boxAt(b.x, b.y-1))
		elif b.y < 1 and b.x > 0 and b.x < 9:
			return (boxAt(b.x, b.y + 1), boxAt(b.x + 1, b.y + 1), boxAt(b.x-1, b.y), boxAt(b.x+1, b.y), boxAt(b.x-1, b.y+1))
		elif b.y == 0 and b.x == 0:
			return (boxAt(1, 0), boxAt(1, 1), boxAt(0, 1))
	except Exception as msg: return None

def getWarn(b):
	warn = 0
	try:
		neighbors = warnInteger(b)
		if not neighbors: return 0
		#print(neighbors)
		for b in neighbors:
			try:
				if b and b.isBomb: warn = warn + 1
			except Exception as e: print("Couldn't detect is neighbor is bomb..." + str(e))
		return warn
	except Exception as ee:
		print("Couldn't find warn int..." + str(ee))
		return warn

boxesToPath = []

def crossFind(b):
	if b.x == 0 and b.y == 0:
		return (boxAt(0, 1), boxAt(1, 0))
	elif b.x == 0 and b.y == 9:
		return (boxAt(0, 8), boxAt(1, 9))
	elif b.x == 9 and b.y == 0:
		return (boxAt(8, 0), boxAt(9, 1))
	elif b.x == 9 and b.y == 9:
		return (boxAt(8, 9), boxAt(9, 8))
	elif b.x > 0  and b.x < 9 and b.y > 0:
		return (boxAt(b.x, b.y-1), boxAt(b.x-1, b.y), boxAt(b.x+1, b.y), boxAt(b.x, b.y+1))
	elif b.x == 0 and b.y > 0 and b.y < 9:
		return (boxAt(b.x, b.y-1), boxAt(b.x, b.y+1), boxAt(b.x+1, b.y))
	elif b.x == 9 and b.y > 0 and b.y < 9:
		return (boxAt(b.x-1, b.y), boxAt(b.x, b.y-1), boxAt(b.x, b.y+1)) 
	elif b.y == 0 and b.x > 0 and b.x < 9:
		return (boxAt(b.x - 1, b.y), boxAt(b.x+1, b.y), boxAt(b.x, b.y+1))
	elif b.y == 9 and b.x > 0 and b.x < 9:
		return (boxAt(b.x - 1, b.y), boxAt(b.x+1, b.y), boxAt(b.x, b.y-1))

def pathFind(b):
	for bo in crossFind(b):
		if bo and getWarn(bo) == 0:
			bo.flag = 0
	for bo2 in warnInteger(b):
		w = getWarn(bo2)
		if w > 0 and w < 9:
			bo2.flag = w
	checkedBoxes.append(b)

lastGame = 0

def lose():
	print("lose")
	resetGame()

def win():
	print("win")
	resetGame()

def resetGame():
	global fps
	global boxes
	global numBombs
	global flagsUsed
	global checkedBoxes
	global blocksLeft
	global lastGame
	fps = pygame.time.Clock()
	boxes[:] = []
	numBombs = 0
	drawBoxesInit()
	pickBombs()
	flagsUsed = 0
	checkedBoxes = []
	blocksLeft = 0
	lastGame = pygame.time.get_ticks()
	
	
while True:
    surfObj.fill(white)
    surfObj.blit(clock, (10, 173))	
    surfObj.blit(bomb, (147, 173))
    
    m = font.render(str(10-flagsUsed), True, black)
    mp = m.get_rect()
    mp.topleft = (120, 173)
    surfObj.blit(m, mp)
    ticks = 0
    if not lastGame == 0:
        mins = (pygame.time.get_ticks() - lastGame) / 1000 / 60
        secs = (pygame.time.get_ticks() - lastGame) / 1000 % 60
    else:
        mins = pygame.time.get_ticks() / 1000 / 60
        secs = pygame.time.get_ticks() / 1000 % 60
    minsS = ""
    secsS = ""
    if secs < 10:
        secsS = "0" + str(int(secs))
    else: secsS = str(int(secs))
    if mins < 10:
        minsS = "0" + str(int(mins))
    else: minsS = str(int(mins))
    
    m2 = font.render(minsS + ":" + secsS, True, black)
    mp2 = m2.get_rect()
    mp2.topleft = (30, 173)
    surfObj.blit(m2, mp2)
    
    drawBox()
    drawBoxes()
    
    for e in pygame.event.get():
        if e.type == QUIT:
            pygame.quit()
            sys.exit()
        elif e.type == MOUSEMOTION:
            selBlock = overBlock()
            if not isInBounds():
    
                selBlock = refBlock
        elif e.type == MOUSEBUTTONUP:
            if isInBounds():
                if e.button == 1:
                    selBlock.flag = getWarn(selBlock)
                    if selBlock.flag == 0:
                        boxesToPath.append(selBlock)
                        pathFind(selBlock)
                    if selBlock.isBomb: selBlock.flag = 9
                elif e.button == 3:
                    if selBlock.flag == -3: selBlock.flag = -2
                    elif selBlock.flag == -2: selBlock.flag = -1
                    elif selBlock.flag == -1: selBlock.flag = -3
    if selBlock.flag == -3: surfObj.blit(blockSurfSel, selBlock.boxP)
    
    pygame.display.update()
    fps.tick(30)