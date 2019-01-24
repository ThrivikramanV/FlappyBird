import pygame
import random
import sys

displaywidth=576
displayheight=512
birdwidth=34
birdheight=24
pipewidth=52
pipeheight=320
width_bw_pipes=200
basewidth=969
baseheight=105
digitwidth=24
red=(210,0,0)
brightred=(255,0,0)
green = (0,210,0)
brightgreen=(0,255,0)
blue=(0,0,200)
brightblue=(0,0,255)
brightpurple=(255,0,255)
purple=(220,0,220)
brightyellow=(255,255,0)
yellow=(220,220,0)
black=(0,0,0)
white=(255,255,255)
grey=(210,210,210)

pygame.init()
win = pygame.display.set_mode((displaywidth,displayheight))
pygame.display.set_caption('Flappy Bird')
clock = pygame.time.Clock()

background = pygame.image.load('C:\\Users\\Thrivikraman\\Desktop\\flappybird\\MyVersion\\Assets\\background-day.png')
birds = [pygame.image.load(f'C:\\Users\\Thrivikraman\\Desktop\\flappybird\\MyVersion\\Assets\\redbird{i}.png') for i in range(1,7)]
pipes = [pygame.image.load('C:\\Users\\Thrivikraman\\Desktop\\flappybird\\MyVersion\\Assets\\pipedown.png'),pygame.image.load('C:\\Users\\Thrivikraman\\Desktop\\flappybird\\MyVersion\\Assets\\pipeup.png')]
base = pygame.image.load('C:\\Users\\Thrivikraman\\Desktop\\flappybird\\MyVersion\\Assets\\base.png')
digits = [pygame.image.load(f'C:\\Users\\Thrivikraman\\Desktop\\flappybird\\MyVersion\\Assets\\{i}.png') for i in range(10)]
flappybird = pygame.image.load('C:\\Users\\Thrivikraman\\Desktop\\flappybird\\MyVersion\\Assets\\flappybird.png')
gameover = pygame.image.load('C:\\Users\\Thrivikraman\\Desktop\\flappybird\\MyVersion\\Assets\\gameover.png')
birdicon = pygame.image.load('C:\\Users\\Thrivikraman\\Desktop\\flappybird\\MyVersion\\Assets\\birdicon.png')
cred = pygame.image.load('C:\\Users\\Thrivikraman\\Desktop\\flappybird\\MyVersion\\Assets\\credits.png')

falldown = pygame.mixer.Sound('C:\\Users\\Thrivikraman\\Desktop\\flappybird\\MyVersion\\Assets\\falldown.wav')
hit = pygame.mixer.Sound('C:\\Users\\Thrivikraman\\Desktop\\flappybird\\MyVersion\\Assets\\hit.wav')
point = pygame.mixer.Sound('C:\\Users\\Thrivikraman\\Desktop\\flappybird\\MyVersion\\Assets\\point.wav')

pygame.display.set_icon(birdicon)

def backdisplay():
    win.blit(background,(0,0))
    win.blit(background,(displaywidth/2,0))

def pipesdisplay(pipeslist):
    for ele in pipeslist:
        pipex = ele[0]
        down_pipe_y = ele[1]
        up_pipe_y = down_pipe_y - height_bw_pipes - pipeheight
        win.blit(pipes[0],(pipex,down_pipe_y))
        win.blit(pipes[1],(pipex,up_pipe_y))

def basedisplay(basex):
    win.blit(base,(basex,displayheight-baseheight))

def birddisplay(count,birdx,birdy,angle):
    win.blit(pygame.transform.rotate(birds[count],angle),(birdx,birdy))

def scoredisplay(score,x,y):
    score = str(score)
    scorewidth=digitwidth*len(score)
    n=0
    for i in score:
        i=int(i)
        win.blit(digits[i],((x-(scorewidth/2)+(n*(digitwidth+1))),y))
        n+=1

def messagedisplay(text,colour,fontsize,pos_x,pos_y):
    font = pygame.font.Font('C:\\Windows\\Fonts\\comic.ttf',fontsize)
    textSurf = font.render(text, True, colour)
    textRect = textSurf.get_rect()
    textRect.center = (pos_x,pos_y)
    win.blit(textSurf,textRect)

def crash(score):
    with open(f'C:\\Users\\Thrivikraman\\Desktop\\flappybird\\MyVersion\\bestscores\\{level}.txt','r') as fin:
        bestscore=fin.read()
    bestscore=bestscore.strip()
    bestscore=int(bestscore)
    if score > bestscore:
        with open(f'C:\\Users\\Thrivikraman\\Desktop\\flappybird\\MyVersion\\bestscores\\{level}.txt','w') as fout:
            fout.write(str(score))        
    win.blit(gameover,(displaywidth/2-(192/2),150))
    pygame.display.update()
    pygame.time.delay(3000)
    startscreen()

def pipecrash(pipeslist,basex,count,birdx,birdy,angle,g,score):
    angle_decrement=3
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        backdisplay()
        pipesdisplay(pipeslist)
        basedisplay(basex)
        scoredisplay(score,displaywidth/2,50)
        angle=angle-angle_decrement
        if angle < -90:
            angle=-90
            angle_decrement=0
        birdy = birdy + g
        if birdy + birdwidth > displayheight-baseheight:
            angle=-90
            run = False
        birddisplay(count,birdx,birdy,angle)
        pygame.display.update()
        clock.tick(40)
    crash(score)

def button(msg,x,y,width,height,active,inactive,func):
    global level,height_bw_pipes
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    
    if x < mouse[0] < x+width and y < mouse[1] < y+height:
        pygame.draw.rect(win,active,(x,y,width,height))
        if click[0]==1:
            if func=='play' or func=='credits' or func=='rules' or func=='home' or func=='continue':
                return False
            if func=='easy':
                level='easy'
                height_bw_pipes=200
                return False
            if func=='medium':
                level='medium'
                height_bw_pipes=150
                return False
            if func=='hard':
                level='hard'
                height_bw_pipes=100
                return False
            if func=='levels':
                levelscreen()
            if func=='newgame':
                startscreen()
            if func=='quit':
                pygame.quit()
                sys.exit()
    else:
        pygame.draw.rect(win,inactive,(x,y,width,height))

    messagedisplay(msg,black,20,x+(width/2),y+(height/2))
    return True

def startscreen():
    count=-1
    birdx=150
    birdy=200
    basex=0
    basespeed=-8
    score=0
    angle=0
    rules=False
    credit=False
    
    run=True
    
    while run:
        backdisplay()
        
        run = button('PLAY!',100,300,100,50,brightgreen,green,'play')
        button('QUIT',376,300,100,50,brightred,red,'quit')
        if not rules and not credit:
            rules = not button('RULES',238,300,100,50,brightblue,blue,'rules')
            credit = not button('CREDITS',238,355,100,50,yellow,brightyellow,'credits')
        if rules:
            rules = button('HOME',238,250,100,50,brightblue,blue,'home')
        if credit:
            credit = button('HOME',238,250,100,50,brightblue,blue,'home')
        
        if not rules and not credit:
            scoredisplay(score,displaywidth/2,50)
            win.blit(flappybird,(displaywidth/2-(184/2),120))
            button(f'LEVEL:{level[:1].upper()}',5,5,100,30,purple,brightpurple,'levels')
            messagedisplay('BEST SCORE',brightred,23,500,175)
            with open(f'C:\\Users\\Thrivikraman\\Desktop\\flappybird\\MyVersion\\bestscores\\{level}.txt','r') as fin:
                bestscore=fin.read()
            bestscore=bestscore.strip()
            bestscore=int(bestscore)
            scoredisplay(bestscore,500,200)
        if rules:
            messagedisplay('Use the SpaceBar/UpArrow/W to control the bird',blue,22,displaywidth/2,125)
            messagedisplay('Press Ctrl to pause',blue,22,displaywidth/2,150)
            messagedisplay('Press S to start',blue,22,displaywidth/2,175)
        if credit:
            win.blit(cred,(53,50))
        
        basex+=basespeed
        if basex + basewidth < displaywidth:
            basex=0
        basedisplay(basex)
        
        count+=1
        if count==6:
            count=0                
        if count==0 or count==1:
            birdy=birdy+1
        if count==4 or count==5:
            birdy=birdy-1
        birddisplay(count,birdx,birdy,angle)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    run = False
        
        pygame.display.update()
        clock.tick(20)
    
    gameloop(count,birdx,birdy,basex)

def pause(count,birdx,birdy,angle,basex,pipeslist,score):
    run=True
    while run:
        backdisplay()
        pipesdisplay(pipeslist)
        basedisplay(basex)
        scoredisplay(score,displaywidth/2,50)
        birddisplay(count,birdx,birdy,angle)
        messagedisplay('PAUSED',white,50,displaywidth/2,150)
        button('NEW GAME',100,350,120,50,brightgreen,green,'newgame')
        button('QUIT',356,350,120,50,brightred,red,'quit')
        run = button('CONTINUE',228,300,120,50,brightblue,blue,'continue')

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    run = False

        pygame.display.update()
        clock.tick(20)
        
def gameloop(count,birdx,birdy,basex):
    g=6
    bird_y_change=0
    angle=0
    angle_decrement=3
    pipex = displaywidth
    down_pipe_y = random.randrange(height_bw_pipes+1, displayheight - baseheight)
    pipeslist = [[pipex,down_pipe_y]]
    if level=='easy':
        pipespeed=-4
        basespeed=-4
    if level=='medium':
        pipespeed=-5
        basespeed=-5
    if level=='hard':
        pipespeed=-6
        basespeed=-6
    score=0
    basecrash=False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP or event.key == pygame.K_SPACE or event.key == pygame.K_w:
                    angle=20
                    angle_decrement=0
                    bird_y_change=-12
                if event.key == pygame.K_LCTRL or event.key == pygame.K_RCTRL:
                    pause(count,birdx,birdy,angle,basex,pipeslist,score)
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP or event.key == pygame.K_SPACE or event.key == pygame.K_w:
                    angle_decrement=3
                    bird_y_change=0

        backdisplay()
        
        for ele in pipeslist:
            ele[0]+=pipespeed
        
        pipex = pipeslist[len(pipeslist)-1][0]
        if pipex + pipewidth + width_bw_pipes < displaywidth:
            pipex = displaywidth
            down_pipe_y = random.randrange(height_bw_pipes+1, displayheight - baseheight)
            pipeslist.append([pipex,down_pipe_y])
        
        pipex = pipeslist[0][0]
        if pipex + pipewidth < 0:
            pipeslist.pop(0)

        for ele in pipeslist:
            pipex = ele[0]
            down_pipe_y = ele[1]
            if birdx + birdwidth >= pipex and birdx <= pipex + pipewidth:                        
                if birdy <= down_pipe_y - height_bw_pipes or birdy + birdheight >= down_pipe_y:
                    pygame.mixer.Sound.play(hit)
                    pygame.mixer.Sound.play(falldown)
                    pipecrash(pipeslist,basex,count,birdx,birdy,angle,g,score)
                if birdx+((displaywidth-birdx)%pipespeed)==pipex:
                    pygame.mixer.Sound.play(point)
                    score+=1
        
        pipesdisplay(pipeslist)
        scoredisplay(score,displaywidth/2,50)

        basex+=basespeed
        
        if basex + basewidth < displaywidth:
            basex=0
        
        basedisplay(basex)

        birdy = birdy + g + bird_y_change
        
        if birdy<0:
            birdy=0
        
        if birdy>=displayheight-baseheight-birdheight:
            birdy=displayheight-baseheight-birdheight
            basecrash=True
        
        angle=angle-angle_decrement
        if angle < -90:
            angle=-90
            angle_decrement=0
                
        count+=1
        if count==6:
            count=0
        
        birddisplay(count,birdx,birdy,angle)

        if basecrash:
            pygame.mixer.Sound.play(hit)
            crash(score)

        pygame.display.update()        
        clock.tick(40)

level=''
height_bw_pipes=0
def levelscreen():
    run=True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        win.fill(black)
        run=button('EASY',88,231,120,50,grey,white,'easy')
        if run:
            run=button('MEDIUM',228,231,120,50,grey,white,'medium')
        if run:
            run=button('HARD',368,231,120,50,grey,white,'hard')
        pygame.display.update()
        clock.tick(20)
    startscreen()

levelscreen()
