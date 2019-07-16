# Use python 3.x
from time import sleep
import random

import board
import neopixel


NO_PIXELS = 300

pixels = neopixel.NeoPixel(board.D18, NO_PIXELS, auto_write=False)


def turn_off(pixels, index):
    pixels[index] = (0, 0, 0)

def turn_on(pixels, index, color):
    pixels[index] = color

def clear(pixels):
    pixels.fill(BLACK)

def random_color():
    list_rgb = range(100)
    r = random.choice(list_rgb)
    g = random.choice(list_rgb)
    b = random.choice(list_rgb)

    return (r, g, b)

def advance_color(pos):
    if pos < 0 or pos > 255:
        r = g = b = 0
    elif pos < 85:
        r = int(pos * 3)
        g = int(255 - pos*3)
        b = 0
    elif pos < 170:
        pos -= 85
        r = int(255 - pos*3)
        g = 0
        b = int(pos*3)
    else:
        pos -= 170
        r = 0
        g = int(pos*3)
        b = int(255 - pos*3)

    return (r, g, b)

# Main program
if __name__ == '__main__':
    
    RED = (255,0,0)
    tail_length = 5
    tail_positions = [(i+10*i)%255 for i in range(tail_length)]
    print(tail_positions)
    color_seqment = [advance_color(i) for i in tail_positions]

    loop_i = 0
    try:
        while True:
            for index in range(len(pixels)):
                
                #print('Turning on pixel {}'.format(index))
                clear(pixels) 
                color_seqment = [advance_color(i%255) for i in tail_positions]
                for tail_i in range(tail_length):
                    turn_on(pixels, index-tail_i, color_seqment[tail_i])
        
                pixels.show()
                sleep(0.001)
                tail_positions = [i+2 for i in tail_positions]
                
        
    except KeyboardInterrupt:
        clear(pixels)
        pixels.show()
        pass

    print('\nExiting')
    clear(pixels)
    pixels.show()



