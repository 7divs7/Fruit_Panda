import pygame
import os
import random
import math 
import time

class Basket:
    def __init__(self,x,y):
        self.x = x;
        self.y = y;
        self.vel = 10
        self.img = pygame.transform.scale2x(pygame.image.load(os.path.join("images","basket.png")))

    def draw(self,win):
        win.blit(self.img,(self.x,self.y))
    
    def get_mask(self):
        return pygame.mask.from_surface(self.img)

fruit_image=[pygame.transform.scale2x(pygame.image.load(os.path.join("images","bomb.png"))),
    pygame.transform.scale2x(pygame.image.load(os.path.join("images","apple.png"))),
    pygame.transform.scale2x(pygame.image.load(os.path.join("images","straw.png")))]
#fruit_image = pygame.transform.scale2x(pygame.image.load(os.path.join("images","bomb.png")))

class Fruit:
    def __init__(self):
        self.x = random.randrange(50,700)
        self.y = 0
        self.passed = False
        self.divz = random.randrange(0,3)    
        self.fruit_img = pygame.transform.flip(pygame.transform.flip(fruit_image[self.divz],False,True),False,True)
        
    def move(self):
        self.y += 15

    def draw(self,win):
        win.blit(self.fruit_img,(self.x,self.y))
    
    def collide(self,basket):
        basket_mask = basket.get_mask()
        fruit_mask = pygame.mask.from_surface(self.fruit_img)
        offset = (self.x-round(basket.x),self.y-basket.y)
        point = basket_mask.overlap(fruit_mask,offset)
        if point:
            return True
        return False

def lives(win,life):
    p=0
    for i in range(life):
        win.blit(pygame.image.load(os.path.join("images","pandalife.png")),(750+p,10))
        p+=70

def draw_win(win,basket,fruits,score,life):
    #win.fill((0,128,0))
    if life == 0:
        win.blit(pygame.image.load(os.path.join("images","gameover.png")),(100,250))
        pygame.display.update()
        time.sleep(5)
        pygame.quit()
    else:
        win.blit(pygame.image.load(os.path.join("images","background.jpg")),(0,0))
        #win.blit(pygame.image.load(os.path.join("images","fruit.png")),(800,10))
        lives(win,life)
        
        for i in fruits:
            i.draw(win)
        basket.draw(win)
        pygame.font.init()
        score_font = pygame.font.SysFont("Forte",50)
        score_text = score_font.render("Score: "+str(score),1,(0,255,0))
        win.blit(score_text,(10,10))
        pygame.display.update()

def main():
    basket = Basket(230,800)
    fruits = [Fruit()]
    life = 3
    pygame.init()
    win = pygame.display.set_mode((1000,1000))
    pygame.display.set_caption('Fruit Basket!')
    done = True
    clk = pygame.time.Clock()
    score = 0
    while done:
        clk.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = False
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            basket.x-=basket.vel
        if keys[pygame.K_RIGHT]:
            basket.x+=basket.vel

        add_fruit = False
        del_fruit = []
        
        for i in fruits:
            if i.collide(basket):
                if i.divz == 0:
                    score -= 5
                    life -= 1
                else:
                    score += 1

                #score += 1 
                del_fruit.append(i)
                add_fruit = True
            
            if i.y>1000:
                del_fruit.append(i)
            if not i.passed and i.y>basket.y:
                i.passed = True
                add_fruit = True
            i.move()
        
        if add_fruit:
            fruits.append(Fruit())
        
        for j in del_fruit:
            fruits.remove(j)
        
        draw_win(win,basket,fruits,score,life)
    pygame.quit()
    quit()
main()