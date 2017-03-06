"""
Move the balloon through the cave without hitting the wall.

This uses pixel perfect collision detection to make the game more fun.

Use arrow keys to move the balloon - up, down, left, right.
"""


import os
import pygame
from pygame.locals import *

if not hasattr(pygame, "Mask"):
    raise "Need pygame 1.8 for masks."

pygame.display.init()
pygame.font.init()

pygame.display.set_caption("Balloon!  Don't hit the walls")

# is the game still going?
going = 1

screen = pygame.display.set_mode((320,200))
pygame.key.set_repeat(500, 2)
clock = pygame.time.Clock()


# fill the screen with red... for dramatic effect.
screen.fill((255,0,0))
pygame.display.flip()

def load_image(i):
    'load an image from the data directory with per pixel alpha transparency.'
    return pygame.image.load(os.path.join("data", i)).convert_alpha()

terrain1 = load_image("terrain1.png")
balloon = load_image("balloon.png")



def vadd(x,y):
    return [x[0]+y[0],x[1]+y[1]]

def vsub(x,y):
    return [x[0]-y[0],x[1]-y[1]]

def vdot(x,y):
    return x[0]*y[0]+x[1]*y[1]

def collision_normal(left_mask, right_mask, left_pos, right_pos):


    offset = map(int,vsub(left_pos,right_pos))

    overlap = left_mask.overlap_area(right_mask,offset)

    if overlap == 0:
        return None, overlap

    """Calculate collision normal"""

    nx = (left_mask.overlap_area(right_mask,(offset[0]+1,offset[1])) -
          left_mask.overlap_area(right_mask,(offset[0]-1,offset[1])))
    ny = (left_mask.overlap_area(right_mask,(offset[0],offset[1]+1)) -
          left_mask.overlap_area(right_mask,(offset[0],offset[1]-1)))
    if nx == 0 and ny == 0:
        """One sprite is inside another"""
        return None, overlap

    n = [nx,ny]

    return n, overlap



class Balloon(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self) #call Sprite initializer
        self.image = load_image("balloon.png")

        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)

        self.setPos([0,0])
        self.setVelocity([0,0])

    def setPos(self,pos):
        self.rect[0] = pos[0]
        self.rect[1] = pos[1]

    def setVelocity(self,vel):
        self.vel = [vel[0],vel[1]]

    def move(self,dr):
        print("move!", dr)
        pos = vadd(self.rect,dr)
        self.rect[0] = pos[0]
        self.rect[1] = pos[1]

    def kick(self,impulse):
        print("kick!", impulse)

        self.vel[0] += impulse[0]
        self.vel[1] += impulse[1]


    def collide(self, s):

        offset = list(map(int,vsub(s.rect, self.rect)))

        overlap = self.mask.overlap_area(s.mask,offset)

        if overlap == 0:
            return None, overlap

        """Calculate collision normal"""
        nx = (self.mask.overlap_area(s.mask,(offset[0]+1,offset[1])) -
              self.mask.overlap_area(s.mask,(offset[0]-1,offset[1])))
        ny = (self.mask.overlap_area(s.mask,(offset[0],offset[1]+1)) -
              self.mask.overlap_area(s.mask,(offset[0],offset[1]-1)))

        if nx == 0 and ny == 0:
            """One sprite is inside another"""
            return None, overlap

        n = [nx,ny]



        dv = vsub(s.vel,self.vel)
        J = vdot(dv,n)/(2*vdot(n,n))

        if J > 0:
            """Can scale up to 2*J here to get bouncy collisions"""
            J *= 1.9
            self.kick([nx*J,ny*J])
            s.kick([-J*nx,-J*ny])
            return

        """Separate the sprites"""
        c1 = -overlap/vdot(n,n)
        c2 = -c1/2
        self.kick([c2*nx,c2*ny])
        s.kick([(c1+c2)*nx,(c1+c2)*ny])


    def update(self,dt):
        max_vel = 1
        if self.vel[0] > max_vel:
            self.vel[0] = max_vel
        if self.vel[0] < -max_vel:
            self.vel[0] = -max_vel

        if self.vel[1] > max_vel:
            self.vel[1] = max_vel
        if self.vel[1] < -max_vel:
            self.vel[1] = -max_vel

        print (self.vel, "vel!")
        self.rect[0] += dt*self.vel[0]
        self.rect[1] += dt*self.vel[1]



balloon1 = Balloon()
balloon2 = Balloon()

balloon2.setPos([20,20])
balloon2.setVelocity([2,2])

sprites = pygame.sprite.RenderPlain((balloon1, balloon2))

#if pygame.sprite.spritecollide(b1, b2, False, pygame.sprite.collide_mask):
#    print "sprites have collided!"





# create a mask for each of them.
terrain1_mask = pygame.mask.from_surface(terrain1, 50)

# this is where the balloon, and terrain are.
terrain1_rect = terrain1.get_rect()


# a message for if the balloon hits the terrain.
afont = pygame.font.Font(None, 16)
hitsurf = afont.render("Hit!!!  Oh noes!!", 1, (255,255,255))


last_bx, last_by = 0,0









# start the main loop.

while going:
    events = pygame.event.get()
    for e in events:
        if e.type == QUIT or e.type == KEYDOWN and e.key == K_ESCAPE:
            going = 0
        if e.type == pygame.KEYDOWN:
            # move the balloon around, depending on the keys.
            balloon_rect = balloon1.vel
            if e.key in [K_LEFT]:
                balloon_rect[0] -= 1
            if e.key in [K_RIGHT]:
                balloon_rect[0] += 1

            if e.key in [K_UP]:
                balloon_rect[1] -= 1
            if e.key in [K_DOWN]:
                balloon_rect[1] += 1

    if 0:
        lsprites = list(sprites)
        for i in range(len(lsprites)):
            for j in range(i+1,len(lsprites)):
                lsprites[i].collide(lsprites[j])

    balloon1.collide(balloon2)
    balloon2.collide(balloon1)

    for s in sprites:
        s.update(1)
        if s.rect[0] < -s.image.get_width()-3:
            s.rect[0] = screen.get_width()
        elif s.rect[0] > screen.get_width()+3:
            s.rect[0] = -s.image.get_width()
        if s.rect[1] < -s.image.get_height()-3:
            s.rect[1] = screen.get_height()
        elif s.rect[1] > screen.get_height()+3:
            s.rect[1] = -s.image.get_height()


    balloon_rect = balloon1.rect
    balloon_mask = balloon1.mask
    # see how far the balloon rect is offset from the terrain rect.
    bx, by = (balloon_rect[0], balloon_rect[1])
    offset_x = bx - terrain1_rect[0]
    offset_y = by - terrain1_rect[1]

    #print bx, by
    overlap = terrain1_mask.overlap(balloon_mask, (offset_x, offset_y))

    #
    last_bx, last_by = bx, by





    # draw the background color, and the terrain.
    screen.fill((255,0,0))
    screen.blit(terrain1, (0,0))

    # draw the balloon.
    #screen.blit(balloon, (balloon_rect[0], balloon_rect[1]) )
    sprites.draw(screen)

    # draw the balloon rect, so you can see where the bounding rect would be.
    pygame.draw.rect(screen, (0,255,0), balloon_rect, 1)


    # see if there was an overlap of pixels between the balloon
    #   and the terrain.
    if overlap:
        # we have hit the wall!!!  oh noes!
        screen.blit(hitsurf, (0,0))

    # flip the display.
    pygame.display.flip()

    # limit the frame rate to 40fps.
    clock.tick(40)



pygame.quit()


