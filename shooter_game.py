from pygame import *
from random import *
from time import time as timer
font.init()

window = display.set_mode((700, 500))
display.set_caption('Space King')
background = transform.scale(image.load('galaxy.jpg'), (700, 500))
clock = time.Clock()
font1 = font.SysFont('Arial', 36)
font2 = font.SysFont('Arial', 50)
finish = False
num_fire = 0
rel_time = False

Winner = font1.render(
    'Вы победили!', True, (255, 255, 255)
    )
Losed = font1.render(
    'Вы проиграли!', True, (255, 255, 255)
    )

class GameSprite(sprite.Sprite):
    def __init__(self,player_image,player_x,player_y,player_speed,size_x,size_y):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (size_x,size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < 620:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet('bullet.png', self.rect.centerx - 5, self.rect.top, 15, 15, 20)
        bullets.add(bullet)
        

class Enemy(GameSprite):
    def __init__(self,player_image,player_x,player_y,player_speed,size_x,size_y,is_asteroid = False):
        super().__init__(player_image,player_x,player_y,player_speed,size_x,size_y)
        self.is_asteroid = is_asteroid
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > 500:
            self.rect.x = randint(80, 700 - 80)
            self.rect.y = -50
            if not self.is_asteroid:
                lost = lost + 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()

score = 0
lost = 0
life = 3
rocket = Player('rocket.png',300,400,10,80,100)
monsters = sprite.Group()
asteroids = sprite.Group()
for i in range (1, 4):
    asteroid = Enemy('asteroid.png', randint(80, 700 - 80), -40, random() * 2 + 1, 80, 50, True)
    asteroids.add(asteroid)
for i in range(1, 6):
    monster = Enemy('ufo.png', randint(80, 700 - 80), -40, random() * 2 + 1, 80, 50)
    monsters.add(monster)
bullets = sprite.Group()

mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')

game = True
while game:
    window.blit(background,(0, 0))
    rocket.reset()
    monsters.draw(window)
    bullets.draw(window)
    asteroids.draw(window)
    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire < 5 and rel_time == False:
                    num_fire = num_fire + 1
                    fire_sound.play()
                    rocket.fire()
                
                if num_fire >= 5 and rel_time == False:
                    last_time = timer()
                    rel_time = True
    
    if not finish:
        monsters.update()
        rocket.update()
        bullets.update()
        asteroids.update()

        if rel_time == True:
            now_time = timer()

            if now_time - last_time < 3:
                reload = font2.render('Wait, reload.....', 1, (150,0,0))
                window.blit(reload, (260, 460))
            else:
                num_fire = 0

        lose = font1.render(
            'Пропущено: ' + str(lost), True, (255,255,255)
            )
        score_text = font1.render(
            'Счёт: ' + str(score), True, (255,255,255)
        )
        if life == 3:
            color = (0, 255, 0)
        if life == 2:
            color = (255, 255, 0)
        if life == 1:
            color = (255, 0, 0)
        lifes = font2.render(
            'Жизни: ' + str(life), True,color
        )
        window.blit(lose, (10, 10))
        window.blit(score_text, (10, 40))
        window.blit(lifes, (500, 40))
        sprites_list = sprite.groupcollide(
            asteroids, bullets, False, True
        )
        sprites_list = sprite.groupcollide(
            monsters, bullets, True, True
        )
        for s in sprites_list:
            monster = Enemy('ufo.png', randint(80, 700 - 80), -40, random() * 2 + 1 + score / 10, 80, 50)
            monsters.add(monster)
            score += 1
        sprites_list = sprite.spritecollide(
            rocket, monsters, True
        )
        if sprites_list or sprite.spritecollide(rocket, asteroids, True):
            life -= 1

        if lost >= 5 or life <= 0:
            print('Ваш максимальный балл:', score)
            finish = True
        
        display.update()
        clock.tick(60)