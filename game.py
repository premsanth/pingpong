import pygame as pg
import random
import sys
from pygame.locals import *

def from_right(x_cord, width=0):
    return SCREEN_WIDTH - x_cord - width

####### defaults #####################################################
# set up the window
SCREEN_WIDTH  = 500
SCREEN_HEIGHT = 400

# set up the colors
BLACK =(0x00,0x00,0x00)
WHITE =(0xFF,0xFF,0xFF)
RED   =(0xFF,0x00,0x00)
GREEN =(0x00,0xFF,0x00)
BLUE  =(0x00,0x00,0xFF) 


BAR_WIDTH   = 20    # thickness
BAR_HEIGHT  = 300   # length

BAR_CENTER = SCREEN_HEIGHT/2 - BAR_HEIGHT/2
BALL_SPD = 1  # 1p per draw
BALL_SZ = 5

UP    = 1
DOWN  = 2
LEFT  = 3
RIGHT = 4

####### defaults #####################################################


pg.init()
pg.event.set_allowed([pg.KEYDOWN, pg.KEYUP, pg.QUIT])

SCREEN = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

class object:
    x = 0
    y = 0
    x_dir = LEFT 
    y_dir = 0

def main():
    pg.display.set_caption('Drawing')

    ball = object()
    ball.x, ball.y = SCREEN_WIDTH/2, SCREEN_HEIGHT/2

    left_bar  = object()
    left_bar.x, left_bar.y = 0, BAR_CENTER
    left_bar.y_dir = random.randint(UP,DOWN)

    right_bar = object()
    right_bar.x, right_bar.y = from_right(0,BAR_WIDTH), BAR_CENTER
    right_bar.y_dir = random.randint(UP,DOWN)


    # run the game loop
    while True:
        # handle events
        for event in pg.event.get():
            if event.type==QUIT or event.type==KEYDOWN:
               pg.quit()
               sys.exit()

        # paint screen
        draw_stuff(left_bar, right_bar, ball)

        # update display
        pg.display.update()


def draw_bars(lb, rb):
    pg.draw.rect(SCREEN,  RED, (lb.x, lb.y, BAR_WIDTH, BAR_HEIGHT))
    pg.draw.rect(SCREEN, BLUE, (rb.x, rb.y, BAR_WIDTH, BAR_HEIGHT))

def draw_ball(bp):
    pg.draw.circle(SCREEN, BLACK, (bp.x,bp.y), BALL_SZ, 0)

def trajectory(lb, rb, bp):
    global BALL_SPD

    # bounce off walls
    # right wall or bar
    if((bp.x+BALL_SZ >= SCREEN_WIDTH) or
        ((bp.x+BALL_SZ >= SCREEN_WIDTH - BAR_WIDTH) and 
         (bp.y in range(rb.y+BALL_SZ, rb.y+BAR_HEIGHT-BALL_SZ)))):
        print("direction changing to LEFT")
        bp.x_dir = LEFT

    # left wall or bar
    if((bp.x-BALL_SZ <= 0) or 
        ((bp.x-BALL_SZ <= BAR_WIDTH) and 
         (bp.y in range(lb.y+BALL_SZ, lb.y+BAR_HEIGHT-BALL_SZ)))):
        print("direction changing to RIGHT")
        bp.x_dir = RIGHT 

    # top wall
    if(bp.y+BALL_SZ >= SCREEN_HEIGHT):
        bp.y_dir = UP

    # bottom wall
    if(bp.y-BALL_SZ <= 0):
        bp.y_dir = DOWN

    # update
    bp.x = bp.x+BALL_SPD if bp.x_dir==RIGHT else bp.x-BALL_SPD
    bp.y = bp.y+BALL_SPD if bp.y_dir==DOWN  else bp.y-BALL_SPD
    return bp


# draw on the surface object
def draw_stuff(lb, rb, ball):
    SCREEN.fill(WHITE)

    #pg.draw.line(SCREEN, BLUE, (60, 60), (120, 60), 4)
    draw_bars(lb, rb)
    draw_ball(ball)
    ball = trajectory(lb, rb, ball)

main()
