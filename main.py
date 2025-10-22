# Language: MicroPython
from microbit import *
import random
import utime

# Game settings
width = 5  # Micro:Bit LED width
height = 5  # Micro:Bit LED height

# Mario basic state
mario_x = 2
mario_y = 4

# Obstacles (1 = obstacle, 0 = empty)
obstacles = [[0]*width for _ in range(height)]
score = 0
delay = 500  # in milliseconds

# Initialize first obstacles row
for i in range(width):
    obstacles[height-1][i] = 0

# Draw function
def draw():
    display.clear()
    for y in range(height):
        for x in range(width):
            if obstacles[y][x]:
                display.set_pixel(x, y, 9)  # obstacle
    display.set_pixel(mario_x, mario_y, 5)  # Mario

# Move Mario left/right
def move_left():
    global mario_x
    if mario_x > 0:
        mario_x -= 1

def move_right():
    global mario_x
    if mario_x < width-1:
        mario_x += 1

# Simple jump simulation
jumping = False
jump_counter = 0
def jump():
    global jumping, jump_counter
    if not jumping:
        jumping = True
        jump_counter = 0

def update_jump():
    global mario_y, jumping, jump_counter
    if jumping:
        # simple jump: move up 1, then down 1
        if jump_counter == 0:
            mario_y -= 1
        elif jump_counter == 1:
            mario_y += 1
            jumping = False
        jump_counter += 1

# Scroll obstacles down
def scroll_obstacles():
    global obstacles, score
    for y in range(height-1):
        obstacles[y] = obstacles[y+1][:]
    # Generate new obstacles
    new_row = [random.choice([0, 0, 1]) for _ in range(width)]
    obstacles[height-1] = new_row
    score += 1

# Main game loop
while True:
    # Move Mario based on button input
    if button_a.is_pressed():
        move_left()
    if button_b.is_pressed():
        move_right()
    if accelerometer.get_z() < -200:
        jump()

    update_jump()
    draw()
    utime.sleep_ms(delay)
    scroll_obstacles()

    # Check collision
    if obstacles[mario_y][mario_x]:
        display.scroll("Game Over! Score: {}".format(score))
        break