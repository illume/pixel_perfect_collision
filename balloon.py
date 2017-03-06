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

# create a mask for each of them.
terrain1_mask = pygame.mask.from_surface(terrain1, 50)
balloon_mask = pygame.mask.from_surface(balloon, 50)

# this is where the balloon, and terrain are.
terrain1_rect = terrain1.get_rect()
balloon_rect = balloon.get_rect()


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
            if e.key in [K_LEFT]:
                balloon_rect.x -= 1
            if e.key in [K_RIGHT]:
                balloon_rect.x += 1
                
            if e.key in [K_UP]:
                balloon_rect.y -= 1
            if e.key in [K_DOWN]:
                balloon_rect.y += 1



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
    screen.blit(balloon, (balloon_rect[0], balloon_rect[1]) )

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


