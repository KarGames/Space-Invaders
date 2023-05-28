import pygame
import random

pygame.init()

WIDTH, HEIGHT = 500, 500

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

class Ship():
    def __init__(self, posX, posY, lives):
        self.posX = posX
        self.posY = posY
        self.lives = lives
        
class Bullet():
    def __init__(self, posX, posY, speed):
        self.posX = posX
        self.posY = posY
        self.speed = speed
        
    def moveBullet(self):
        self.posY -= self.speed
        
    def outOfBoundaries(self):
        if self.posY <= 0:
            return True
        return False
    

class Alien():
    def __init__(self, posX, posY, speed):
        self.posX = posX
        self.posY = posY
        self.speed = speed

    def moveAlien(self):
        self.posY += self.speed
    

FPS = 60
running = True

move = ""
fire = False
difficulty = 150
bullets = []
aliens = []

pWidth, pHeight = 50, 50
bWidth, bHeight = 10, 10
aWidth, aHeight = 40, 40

player = Ship(screen.get_width()/2 - pWidth/2, screen.get_height() - pHeight-10, 3)

def handleMovement(move):
    speed = 5
    if move == "left":
        player.posX-=speed
    if move == "right":
        player.posX+=speed
    
def handleBoundaries():
    if player.posX <= 0:
        player.posX = 0
    elif player.posX >= screen.get_width() - pWidth:
        player.posX = screen.get_width() - pWidth

def spawnAlien():
    x = random.randrange(0 + aWidth, screen.get_width() - aWidth)
    alien = Alien(x, 0, 5)
    
    aliens.append(alien)
    
def checkCollision():
    for bullet in bullets:
        for alien in aliens:
            if pygame.Rect.colliderect(pygame.Rect(bullet.posX, bullet.posY, bWidth, bHeight), pygame.Rect(alien.posX, alien.posY, aWidth, aHeight)):
                bullets.remove(bullet)
                aliens.remove(alien)
    
def loss():
    if player.lives <= 0:
        return True
    return False
        
while running:
    clock.tick(60)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                move = "left"
            if event.key == pygame.K_d:
                move = "right"
            if event.key == pygame.K_SPACE:
                bullets.append(Bullet(player.posX + pWidth/2, player.posY, 10))
            
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a or event.key == pygame.K_d:
                move = ""
        
    screen.fill("black")
    
    for bullet in bullets:
        if bullet.outOfBoundaries():
            bullets.remove(bullet)
        
        bullet.moveBullet()
        
        pygame.draw.rect(screen, (0, 0, 255), pygame.Rect(bullet.posX, bullet.posY, bWidth, bHeight))
    
    for alien in aliens:
        alien.moveAlien()
        if alien.posY >= screen.get_height():
            player.lives -= 1
            aliens.remove(alien)
        pygame.draw.rect(screen, (250, 0, 0), pygame.Rect(alien.posX, alien.posY, aWidth, aHeight))
    
    handleBoundaries()
    handleMovement(move)
    
    if random.randrange(0, difficulty) == 1:
        spawnAlien()
    
    checkCollision()
    
    if loss():
        print("GAME OVER!!!")
        running = False
   
    pygame.draw.rect(screen, (0, 255, 0), pygame.Rect(player.posX, player.posY, pWidth, pHeight))
    
    pygame.display.flip()
    
pygame.quit