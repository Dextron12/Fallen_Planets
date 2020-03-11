import pygame, os
from ast import literal_eval

width,height = 840, 620

pygame.init()

class auth:
    user = 'Dextron12' #use this to run through luancher
    #user = None # default user keep for luancher to authenticate

    def initialize(self):
        if self.user != None:
            Game.menu(Game)


class static:
    staticImages = {}

    def loadImage(self, tag, name):
        img = pygame.image.load("Library\\resources\\images\\%s" % name)
        self.staticImages[tag] = img

    def update(self, nw, nh):
        for image in self.staticImages:
            try:
                int(image)
            except:
                self.staticImages[image] = pygame.transform.scale(self.staticImages.get(image), (nw,nh))

class Engine:
    x,y = 0,0
    loadedWorld = {}
    world = None

    colSize = (width-200)/9

    InventoryBarSurf = pygame.Surface((640,50), pygame.SRCALPHA, 32)

    def editWorld(self,name):
        with open('saves/%s.dat' % name, 'r') as f:
            worldData = f.read()
        worldData = worldData.split('~')
        saveName = worldData[0]
        self.loadedWorld = literal_eval(worldData[1])
    

    def createWorld(self,tileX,tileY,saveName):
        for x in range(tileX):
            for y in range(tileY):
                self.loadedWorld[str(x) + '-' + str(y)] = '1'
        maxWidth, maxHeight = x,y

        self.world = pygame.Surface((maxWidth*32,maxHeight*32))#, pygame.SRCALPHA, 32)
        for pos in self.loadedWorld:
            x = int(pos.split('-')[0])
            y = int(pos.split('-')[1])
            self.world.blit(static.staticImages.get(self.loadedWorld.get(pos)), (x*32,y*32))
        #self.world = world.convert_alpha()
        if not os.path.exists("saves"):
            os.mkdir("saves")
        if not os.path.exists("saves\\" + saveName):
            with open("saves/%s.dat" % saveName, "w") as f:
                f.write("Savename: %s" % saveName + '~' + str(self.loadedWorld))
        return maxWidth*32, maxHeight*32

    def createWorldArgs(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                

    def displayWorld(self):
        Game.window.blit(self.world, (self.x*32,self.y*32))

    def movement(self):
        key = pygame.key.get_pressed()
        if key[pygame.K_w]:
            self.y += 1
        if key[pygame.K_s]:
            self.y -= 1
        if key[pygame.K_a]:
            self.x += 1
        if key[pygame.K_d]:
            self.x -= 1

        if key[pygame.K_1]:
            Game.inventorySelector = 0
        if key[pygame.K_2]:
            Game.inventorySelector = 1
        if key[pygame.K_3]:
            Game.inventorySelector = 2
        if key[pygame.K_4]:
            Game.inventorySelector = 3
        if key[pygame.K_5]:
            Game.inventorySelector = 4
        if key[pygame.K_6]:
            Game.inventorySelector = 5
        if key[pygame.K_7]:
            Game.inventorySelector = 6
        if key[pygame.K_8]:
            Game.inventorySelector = 7
        if key[pygame.K_9]:
            Game.inventorySelector = 8

    def InventoryBar(self, selected):
        for s in range(9):
            if selected == s:
                pygame.draw.rect(self.InventoryBarSurf, (255,0,0), (self.colSize*s,0,self.colSize,50), 4)
            else:
                pygame.draw.rect(self.InventoryBarSurf, (0,0,0), (self.colSize*s,0,self.colSize,50), 2)

        Game.window.blit(self.InventoryBarSurf, (100,height-70))

    def updateCoords(self,w,h):
        self.InventoryBarSurf = pygame.Surface((Game.width-200,50), pygame.SRCALPHA, 32)

class GUI:

    def button(self,x,y,w,h,ic,ac,name, surf, funcName=None, args=None):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        pygame.draw.rect(surf, ic, (x,y,w,h))
        if x+w > mouse[0] > x and y+h > mouse[1] > y:
            pygame.draw.rect(surf, ac, (x,y,w,h))
            if click[0] == 1:
                if funcName != None:
                    if args != None:
                        funcName(args)
                    else:
                        funcName()
        self.text(self, x+(w/2), y+(h/2), (0,0,0), 'Arial.ttf', h/2, name, surf)

    def text(self,x,y,color, font, size, msg, surf):
        font = pygame.font.SysFont(font, int(size))
        text = font.render(msg, True, color)
        textRect = text.get_rect()
        textRect.center = (x,y)
        surf.blit(text, textRect)

class Game:

    
    window = pygame.display.set_mode((width,height), pygame.RESIZABLE | pygame.SRCALPHA)

    #Engine.InventoryBarSurf = Engine.InventoryBarSurf.convert_alpha()

    Engine.editWorld(Engine, 'idk')


    loopGame = True

    static.loadImage(static, '1', "Grass.png")
    static.loadImage(static, 'menuBackground', "background.png")

    maxX,maxY = Engine.createWorld(Engine,100,100,"idk")
    inventorySelector = 1

    def menu(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.VIDEORESIZE:
                    self.window = pygame.display.set_mode((event.w,event.h), pygame.RESIZABLE)
                    static.update(static, event.w, event.h)
                    width,height = event.w,event.h
            self.window.blit(static.staticImages.get('menuBackground'), (0,0))

            GUI.button(GUI,width/2-50,150,100,50, (47,79,79), (105,105,105),"New Game", self.window, Engine.createWorldArgs, Engine)
            GUI.text(GUI, width/2,40, (0,0,0), 'Arial', 60, 'Fallen Planets', self.window)
            GUI.button(GUI, width/2-50,230,100,50,(47,79,79), (105,105,105),"Load Game", self.window)
            GUI.button(GUI, width/2-50, 310,100,50, (47, 79, 79), (105, 105, 105), 'Muliplayer', self.window) # MULITPLAYER MODE WILL BE DONE WITH SOCKETS AND SOCKET SERVER WITH ONE SOCKET CONNECTION
            GUI.button(GUI, width/2-50, 390, 100, 50, (47, 79, 79), (105, 105, 105), 'Options', self.window) # 80px apart from other buttons
            GUI.button(GUI, width/2-50, 470, 100, 50, (47, 79, 79), (105, 105, 105), 'Quit', self.window)

            pygame.display.flip()

    def main(self):
        while self.loopGame:
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.VIDEORESIZE:
                    self.window = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
                    width,height = event.w,event.h
                    Engine.updateCoords(Engine, event.w, event.h)
            self.window.fill((0, 0, 255))

            Engine.displayWorld(Engine)

            Engine.InventoryBar(Engine, self.inventorySelector)


            pygame.display.flip()
            Engine.movement(Engine)

auth.initialize(auth)
            



