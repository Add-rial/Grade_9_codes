import pygame
import math
import sys
from pygame import mixer

pygame.init()
mixer.init()

screen=pygame.display.set_mode((700,500))
icon=pygame.transform.scale(pygame.image.load("Space_Wars\icon.ico"),(32,32))

blank_spaces=" "
pygame.display.set_caption(97*blank_spaces+"Space wars")
pygame.display.set_icon(icon)

player_black=pygame.transform.rotate(pygame.image.load("Space_Wars\eattleship_ico_image.png"),-90)
player_color=pygame.transform.rotate(pygame.image.load("Space_Wars\eattelship_colorful.png"),90)
laser1img=pygame.image.load("Space_Wars\laser.png")
laser2img=pygame.image.load("Space_Wars\laser.png")
laser_sound=mixer.Sound("Space_Wars\laser.wav")
explosion=mixer.Sound("Space_Wars\explosion.wav")
buttonPressSound=mixer.Sound("Space_Wars\eutton-press.wav")
shootSymbol=pygame.transform.scale((pygame.image.load("Space_Wars\ShootSymbolRed.png")),(95,95))


laser1x=0
laser1y=0
laser1state="ready"

laser2x=0
laser2y=0
laser2state="ready"

MyFont = pygame.font.Font('Space_Wars\COMIC.ttf', 25)
winner = pygame.font.Font('Space_Wars\COMIC.ttf', 64)
press_space_to_continue_font = pygame.font.Font('Space_Wars\COMIC.ttf', 32)
game_over=False
let_shoot=True

mixer.music.load("Space_Wars\Among Us Theme.mp3")
mixer.music.set_volume(2)
mixer.music.play(-1)

def game():
    global laser1x
    global laser1y
    global laser1state

    global laser2x
    global laser2y
    global laser2state

    global game_over
    global let_shoot

    global MyFont

    mixer.music.load("Space_Wars\eackground.wav")
    mixer.music.set_volume(2)
    mixer.music.play(-1)

    black=(0,0,0)
    red=(225,0,0)
    RUNNING=True

    p2x=480
    p2x_change=0
    p2y=150
    p2y_change=0

    p1x=150
    p1x_change=0
    p1y=150
    p1y_change=0

    p2_lives=10
    p1_lives=10
    while RUNNING:
        screen.fill(black)
        pygame.draw.rect(screen,red,pygame.Rect(350,0,6,600))
        pygame.draw.rect(screen,red,pygame.Rect(0,40,700,6))
        pygame.draw.rect(screen,red,pygame.Rect(0,500,700,6))
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                RUNNING=False
                pygame.quit()
                sys.exit()
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_LEFT:
                    p2x_change = -0.2
                if event.key==pygame.K_RIGHT:
                    p2x_change = 0.2
                if event.key==pygame.K_UP:
                    p2y_change = -0.2
                if event.key==pygame.K_DOWN:
                    p2y_change = 0.2
                
                if event.key==pygame.K_a:
                    p1x_change = -0.2
                if event.key==pygame.K_d:
                    p1x_change = 0.2
                if event.key==pygame.K_w:
                    p1y_change = -0.2
                if event.key==pygame.K_s:
                    p1y_change = 0.2

                if let_shoot:
                    if event.key==pygame.K_LCTRL:
                        if laser1state=="ready":
                            laser1x=p1x
                            laser1y=p1y
                            laser1_move(laser1x,laser1y)

                            laser_sound.play()
                    if event.key==pygame.K_RCTRL:
                        if laser2state=="ready":
                            laser2x=p2x
                            laser2y=p2y
                            laser2_move(laser2x,laser2y)

                            laser_sound.play()

               
            
            if event.type==pygame.KEYUP:
                if event.key==pygame.K_LEFT or event.key==pygame.K_RIGHT :
                    p2x_change = 0
                if event.key==pygame.K_UP or event.key==pygame.K_DOWN:
                    p2y_change = 0
                
                if event.key==pygame.K_d or event.key==pygame.K_a :
                    p1x_change = 0
                if event.key==pygame.K_w or event.key==pygame.K_s:
                    p1y_change = 0

        p2x +=p2x_change
        p2y +=p2y_change

        p1x +=p1x_change
        p1y +=p1y_change


        if p1x >= 280:
            p1x_change=0
            p1x=280
        if p1x <= 0:
            p1x_change=0
            p1x=0
        if p1y <= 50:
            p1y_change=0
            p1y=50
        if p1y >=430:
            p1y_change=0
            p1y=430

        if p2x >= 630:
            p2x_change=0
            p2x=630
        if p2x <= 360:
            p2x_change=0
            p2x=360
        if p2y <= 50:
            p2y_change=0
            p2y=50
        if p2y >=430:
            p2y_change=0
            p2y=430
        
        if laser1state=="fired":
            laser1x +=0.7
            laser1_move(laser1x,laser1y)
            distance_1=math.sqrt(math.pow(((laser1x+64)-(p2x+32)),2)+math.pow(((laser1y+16)-(p2y+32)),2))
            if distance_1 <= 32:
                p2_lives -=1
                laser1state="ready"
                explosion.play()

        if laser1x >= 700:
            laser1state="ready"

        if laser2state=="fired":
            laser2x -=0.7
            laser2_move(laser2x,laser2y)
            distance_2=math.sqrt(math.pow((laser2x-(p1x+32)),2)+math.pow(((laser2y+16)-(p1y+32)),2))
            if distance_2 <= 32:
                p1_lives -=1
                laser2state="ready"
                explosion.play()

        if laser2x <= 0:
            laser2state="ready"

        score_p1 = MyFont.render("Lifes: " + str(p1_lives), True, (255, 255, 255))
        screen.blit(score_p1,(10,10))

        score_p2 = MyFont.render("Lifes: " + str(p2_lives), True, (255, 255, 255))
        screen.blit(score_p2,(585,10))

        player1(p1x,p1y)
        player2(p2x,p2y)

        if p1_lives<=0 and p2_lives>0 :
            winner_show=winner.render("Winner is Player 2", True, (255,255,255))
            screen.blit(winner_show,(70,200))

            winner_show=press_space_to_continue_font.render("Press SpaceBar to Play again",True,(225,225,225))
            screen.blit(winner_show,(115,300))

            game_over=True
            let_shoot=False
            for event in pygame.event.get():
                if event.type==pygame.KEYDOWN:
                    if event.key==pygame.K_SPACE:
                        laser1state="ready"
                        laser2state="ready"
                        game_over=False
                        screen.fill((0,0,0))
                        let_shoot=True
                        game()
                        RUNNING=False
                
                if event.type==pygame.QUIT:
                    RUNNING=False
            
        
        elif p2_lives<=0 and p1_lives>0:
            winner_show=winner.render("Winner is Player 1", True, (255,255,255))
            screen.blit(winner_show,(70,200))

            winner_show=press_space_to_continue_font.render("Press SpaceBar to Play again",True,(225,225,225))
            screen.blit(winner_show,(115,300))
            
            game_over=True
            let_shoot=False
            for event in pygame.event.get():
                if event.type==pygame.KEYDOWN:
                    if event.key==pygame.K_SPACE:
                        laser1state="ready"
                        laser2state="ready"
                        game_over=False
                        screen.fill((0,0,0))
                        let_shoot=True
                        game()
                        RUNNING=False
                if event.type==pygame.QUIT:
                    RUNNING=False

        elif p1_lives==0 and p2_lives==0:
            winner_show=MyFont.render("Wow, Rare Case:A Tie", True, (255,255,255))
            screen.blit(winner_show,(230,250))
            
            game_over=True
            let_shoot=False
            for event in pygame.event.get():
                if event.type==pygame.KEYDOWN:
                    if event.key==pygame.K_SPACE:
                        laser1state="ready"
                        laser2state="ready"
                        game_over=False
                        screen.fill((0,0,0))
                        let_shoot=True
                        game()
                        RUNNING=False
                if event.type==pygame.QUIT:
                    RUNNING=False
        
        
        menu1()
        menu2()
        pygame.display.update()

def player1(x,y):
    screen.blit(player_black,(x,y))

def player2(x,y):
    screen.blit(player_color,(x,y))

def laser1_move(x,y):
    global laser1state
    laser1state="fired"
    screen.blit(laser1img,((x+64),(y+16)))

def laser2_move(x,y):
    global laser2state
    laser2state="fired"
    screen.blit(laser2img,(x,(y+16)))

def menu1():
    screen.blit(shootSymbol,(0,505))

def menu2():
    screen.blit(shootSymbol,(605,505))


instructionfont = pygame.font.Font('Space_Wars\COMIC.ttf', 32)
instructionfont2 = pygame.font.Font('Space_Wars\COMIC.ttf', 21)
def instruction_panel_1():
    run=True
    screen=pygame.display.set_mode((700,500))
    previousButton=button((0,255,0),40,450,130,40,'Previous')
    while run:
        screen.fill((0,0,0))
        previousButton.draw(screen,(255,255,255))
        for event in pygame.event.get():
            pos=pygame.mouse.get_pos()
            if event.type==pygame.QUIT:
               run=False
            if event.type==pygame.MOUSEMOTION:
                if previousButton.isOver(pos):
                    previousButton.color=(255,0,0)
                else:
                    previousButton.color=(0,255,0)
            
            if event.type==pygame.MOUSEBUTTONDOWN:
                if previousButton.isOver(pos):
                    buttonPressSound.play()
                    intro()
                    run=False

        blitter()
        pygame.display.update()

def blitter():
    red=(225,0,0)
    white=(225,225,225)
    pygame.draw.rect(screen,red,pygame.Rect(350,90,6,360))
    pygame.draw.rect(screen,red,pygame.Rect(0,90,700,6))
    pygame.draw.rect(screen,red,pygame.Rect(0,445,700,6))
    instruction=instructionfont.render("Instructions ",True,(225,225,225))
    screen.blit(instruction,(260,25))
    

    instruction=instructionfont.render("Player 1:",True,white)
    screen.blit(instruction,(10,100))

    screen.blit(pygame.transform.rotate(player_black, 90),(150,100))

    instruction=instructionfont.render("Controls:",True, white)
    screen.blit(instruction,(10,160))

    instruction=instructionfont2.render("1) Use 'W' key to move up",True,white )
    screen.blit(instruction,(10,210))

    instruction=instructionfont2.render("2) Use 'S' key to move down",True,white )
    screen.blit(instruction,(10,260))

    instruction=instructionfont2.render("3) Use 'A' key to move left",True,white )
    screen.blit(instruction,(10,310))

    instruction=instructionfont2.render("4) Use 'D' key to move right",True,white )
    screen.blit(instruction,(10,360))

    instruction=instructionfont2.render("5) Use Left Ctrl key to shoot",True,white )
    screen.blit(instruction,(10,410))

    instruction=instructionfont.render("Player 2:",True,white)
    screen.blit(instruction,(370,100))

    screen.blit(pygame.transform.rotate(player_color,-90),(510,100))

    instruction=instructionfont.render("Controls:",True, white)
    screen.blit(instruction,(370,160))

    instruction=instructionfont2.render("1) Use Up key to move up",True,white )
    screen.blit(instruction,(370,210))

    instruction=instructionfont2.render("2) Use Down key to move down",True,white )
    screen.blit(instruction,(370,260))

    instruction=instructionfont2.render("3) Use Left key to move left",True,white )
    screen.blit(instruction,(370,310))

    instruction=instructionfont2.render("4) Use Right key to move right",True,white )
    screen.blit(instruction,(370,360))

    instruction=instructionfont2.render("5) Use Right Ctrl key to shoot",True,white )
    screen.blit(instruction,(370,410))

    
    
def intro():
    runner=True
    playButton=button((0,255,0),275,150,150,70,'PLAY',64)
    instructionButton=button((0,255,0),90,250,530,70,'INSTRUCTIONS',64)
    while runner:
        screen.fill((0,0,0))
        playButton.draw(screen,(255,255,255))
        instructionButton.draw(screen,(255,255,255))

        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                runner=False
            
            pos=pygame.mouse.get_pos()

            if event.type==pygame.MOUSEBUTTONDOWN:
                if playButton.isOver(pos):
                    buttonPressSound.play()
                    game()
                    runner=False
                if instructionButton.isOver(pos):
                    buttonPressSound.play()
                    instruction_panel_1()
                    runner=False
        

            if event.type==pygame.MOUSEMOTION:
                if playButton.isOver(pos):
                    playButton.color= (255,0,0)
                
                else:
                    playButton.color=(0,255,0)

                if instructionButton.isOver(pos):
                    instructionButton.color=(255,0,0)

                else:
                    instructionButton.color=(0,255,0)
        pygame.display.update()
        


class button():
    def __init__(self, color, x,y,width,height, text='',size=32):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.size= size
    def draw(self,win,outline=None):
        #Call this method to draw the button on the screen
        if outline:
            pygame.draw.rect(win, outline, (self.x-2,self.y-2,self.width+4,self.height+4),0)
            
        pygame.draw.rect(win, self.color, (self.x,self.y,self.width,self.height),0)
        
        if self.text != '':
            font = pygame.font.SysFont('comicsans', self.size)
            text = font.render(self.text, 1, (255,255,255))
            win.blit(text, (self.x + (self.width/2 - text.get_width()/2), self.y + (self.height/2 - text.get_height()/2)))

    def isOver(self, pos):
        #Pos is the mouse position or a tuple of (x,y) coordinates
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True
            
        return False


if __name__== "__main__":
    intro()
