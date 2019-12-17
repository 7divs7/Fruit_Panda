import pygame
import os
import random
import math 
import time
import neat

pygame.init()
pygame.display.set_mode()
class Basket:
    def __init__(self,x,y):
        self.x = x;
        self.y = y;
        self.vel = 10
        self.img = pygame.transform.scale2x(pygame.image.load(os.path.join("images","basket.png")).convert_alpha())

    def draw(self,win):
        win.blit(self.img,(self.x,self.y))
    
    def get_mask(self):
        return pygame.mask.from_surface(self.img)

fruit_image=[pygame.transform.scale2x(pygame.image.load(os.path.join("images","bomb.png")).convert_alpha()),
    pygame.transform.scale2x(pygame.image.load(os.path.join("images","apple.png")).convert_alpha()),
    pygame.transform.scale2x(pygame.image.load(os.path.join("images","straw.png")).convert_alpha())]
#fruit_image = pygame.transform.scale2x(pygame.image.load(os.path.join("images","bomb.png")))

class Fruit:
    def __init__(self):
        self.x = random.randrange(50,700)
        self.y = 0
        self.passed = False
        self.divz = random.randrange(0,3)    
        self.fruit_img = pygame.transform.flip(pygame.transform.flip(fruit_image[self.divz],False,True),False,True)
        if self.divz == 0:
            self.bof = 0
        else:
            self.bof = 1

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

def draw_win(win,baskets,fruits,score,gen):
    #win.fill((0,128,0))
    
    win.blit(pygame.image.load(os.path.join("images","background.jpg")).convert(),(0,0))
    #win.blit(pygame.image.load(os.path.join("images","fruit.png")),(800,10))
    #lives(win,life)
    
    for i in fruits:
        i.draw(win)
    for basket in baskets:
        basket.draw(win)
    pygame.font.init()
    score_font = pygame.font.SysFont("Forte",50)
    score_text = score_font.render("Score: "+str(score),1,(0,255,0))
    win.blit(score_text,(10,10))
    gen_text = score_font.render("Gen: " + str(gen-1),1,(0,255,0))
    win.blit(gen_text,(550,10))
    pygame.display.update()

def run(config_path):
    config = neat.config.Config(neat.DefaultGenome,neat.DefaultReproduction,neat.DefaultSpeciesSet,neat.DefaultStagnation,config_path)
    p = neat.Population(config)
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    winner = p.run(main,100)

gen = 0

def main(genomes,config):
    global gen
    gen+=1
    baskets = []
    fruits = [Fruit()]
    #life = 3
    pygame.init()
    win = pygame.display.set_mode((800,700))
    pygame.display.set_caption('Fruit Basket!')
    done = True
    clk = pygame.time.Clock()
    
    nets = []
    ge = []
    
    for _,g in genomes:
        net = neat.nn.FeedForwardNetwork.create(g,config)
        nets.append(net)
        baskets.append(Basket(230,500))
        g.fitness = 0
        ge.append(g)
    
    score = 0
    while done:
        clk.tick(0)

        curr_fruit = 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = False
        
        if len(baskets) > 0:
            if len(fruits) >1 and baskets[0].y < fruits[0].y + fruits[0].fruit_img.get_width():
                curr_fruit = 1
        else:
            done = False
            break

        for x,basket in enumerate(baskets):
            ge[x].fitness += 0.1
            
            #d = math.sqrt((basket.x-fruits[curr_fruit].x)**2+(basket.y-fruits[curr_fruit].y)**2)
            output = nets[x].activate((basket.x,fruits[curr_fruit].x,fruits[curr_fruit].y,fruits[curr_fruit].bof))

            
            if output[0]>0.5:
                basket.x-=basket.vel
            elif output[1]>0.5:
                basket.x+=basket.vel
            

        add_fruit = False
        del_fruit = []
        
        for fruit in fruits:

            for x,basket in enumerate(baskets):
                if (fruit.collide(basket) and fruit.divz==0) or basket.x<-100 or basket.x>480:
                    ge[x].fitness -= 5
                    baskets.pop(x)
                    nets.pop(x)
                    ge.pop(x)
                if not fruit.passed and fruit.y>basket.y:
                    fruit.passed = True
                    add_fruit = True
            
            if fruit.y+fruit.fruit_img.get_width()>650:
                del_fruit.append(fruit)
            
            fruit.move()


        if add_fruit:
            score += 1
            for g in ge:
                g.fitness += 10
            fruits.append(Fruit())
        for i in del_fruit:
            fruits.remove(i)


        draw_win(win,baskets,fruits,score,gen)
    

if __name__=="__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir,"config-feedforward.txt")
    run(config_path)