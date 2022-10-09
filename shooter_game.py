from decimal import Clamped
from pygame import *
from random import randint
#mixer.init()
#mixer.music.load("space.ogg")
#mixer.music.play()

#fire_sound = mixer.Sound("fire.ogg")
img_back = "galaxy.jpg"
img_racket = "rocket.png"
img_enemy = "ufo.png"
img_asteroid = "asteroid.png"
font.init()
font1 = font.SysFont("Arial",80)
font2 = font.SysFont("Arial",40)
win = font1.render("you win", True,(0,255,0))
lose = font1.render("You lose",True,(255,255,255))
score = 0
goal = 10
lost = 0 
max_lost = 3
life = 3 
class GameSprite(sprite.Sprite):
    def __init__(self,player_image,player_x,player_y,size_x,size_y,player_speed):
        sprite.Sprite.__init__(self) #super().__init__()
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x , self.rect.y))
class Player (GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x >5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < 620:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet ("bullet.png",self.rect.centerx,self.rect.top,15,20,-15)
        bullets.add(bullet)
class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_height:
            self.rect.x = randint(80,620)
            self.rect.y = 0
            lost = lost +1
class Bullet (GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()
win_width = 700
win_height = 500
display.set_caption("Shooter")
window = display.set_mode((win_width, win_height))
background = transform.scale(image.load(img_back), (win_width,win_height))
ship = Player(img_racket,5,400,80,100,10)
monsters = sprite.Group()
for i in range(1, 3):
    monster = Enemy(img_enemy, randint(80,630),-40,80,50,randint(1,3))
    monsters.add(monster)
asteroids = sprite.Group()
for i in range (1, 3):
    asteroid = Enemy("asteroid.png",randint(80,620),-40,50,50,randint(1,2))
    asteroids.add(asteroid)
bullets = sprite.Group()
run= True
finish = False
rel_time  = False
num_fire = 0 
from time import time as timer
while run:
    for e in event.get():
        if e.type ==QUIT:
            run =False
        elif e.type ==KEYDOWN:
            if e.key == K_SPACE:
                if num_fire <5 and rel_time == False:
                    num_fire+=1
                    #fire_sound.play()
                    ship.fire()   
                if num_fire >= 5 and rel_time == False:
                    rel_time = True 
                    last_time = timer()

    if not finish:
        window.blit(background,(0, 0))
        #window.blit(win,(200,200))
        ship.update()
        monsters.update()
        asteroids.update()
        bullets.update()
        ship.reset()
        monsters.draw(window)
        asteroids.draw(window)
        bullets.draw(window)
        if rel_time == True:
            now_time = timer()
            if  now_time - last_time < 3:
                reload = font2.render("Wait ... reload",1,(150,0,0))
                window.blit(reload,(260,460))
            else:
                num_fire = 0
                rel_time = False
        collides = sprite.groupcollide(monsters,bullets,True,True)
        for c in collides:
            score = score + 1 
            monster = Enemy(img_enemy,randint(80,620),-40,80,50,randint(1,5))
            monsters.add(monster)
        if sprite.spritecollide(ship,monsters,False)or  sprite.spritecollide(ship,asteroids,False):
            sprite.spritecollide(ship,monsters,True)
            sprite.spritecollide(ship,asteroids,True)
            life = life - 1
        if life == 0 or lost >= max_lost:
            window.blit(lose,(200,200))
            finish= True 
        if score >= goal:
            finish = True
            window.blit(win,(200,200))
              
        if life == 3:
            color_life= (0,150,0) 
        if life == 2:           
            color_life=(100,150,0)
        if life ==1:
            color_life=(150,0,0)
        text_life =font2.render("life"+str(life),1,color_life)
        window.blit(text_life,(630,10))
        text_lose = font2.render("Пропущено:"+str(lost),1,(255,255,255))
        window.blit(text_lose,(10,50))

        score_text = font2.render("Score"+str(score),1,(255,255,255))
        window.blit(score_text,(10,20))




        display.update()
    else:
        finish =False
        score = 0
        lost = 0
        num_fire = 0
        life = 3
        for m in monsters:
            m.kill()
        for a in asteroids:
            a.kill()
        time.delay(3000)
        for i in range(1,6):
            monster = Enemy(img_enemy,randint(80,520),-40,80,50,randint(1,4))
            monsters.add(monster)
        for i in range(1,3):
            asteroid = Enemy("asteroid.png",randint(80,520),-40,80,50,randint(1,2))
            asteroids.add(asteroid)       

    time.delay(50)