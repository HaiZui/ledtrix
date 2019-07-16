# Use python 3.x
from time import sleep, time
import random
import argparse

import board
import neopixel


NO_PIXELS = 300

RED = (255, 0, 0)
pixels = neopixel.NeoPixel(board.D18, NO_PIXELS, auto_write=False)

parser = argparse.ArgumentParser(description='Wheel of Fortune!')
parser.add_argument('--running_time', default = 10)
args = parser.parse_args()
running_time = int(args.running_time)

def turn_off(pixels, index):
    pixels[index] = (0, 0, 0)

def turn_on(pixels, index, color):
    pixels[index] = color

def clear(pixels):
    pixels.fill((0,0,0))

def random_color():
    list_rgb = range(255)
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

def adjust_tail(tail):
    dimmed_tail = [tuple(int(tail[i][j] * 2**(-i)) for j in range(len(tail[i]))) for i in range(len(tail))]
    return dimmed_tail 

def flash_random_pixel(pixels, time):
    random_pixel_index = random.choice(range(len(pixels)))
    pixels[random_pixel_index] = random_color()
    pixels.show()
    sleep(time)
    turn_off(pixels, random_pixel_index)
    return random_pixel_index

def flash_pixel(pixels, index, color, max_time=None, flash_time=0.1):
    if max_time is None:
        end_time = time() + 60
    else:
        end_time = time() + max_time

    while True:
        # Turn on
        pixels[index] = color
        pixels.show()
        sleep(flash_time)
        turn_off(pixels, index)
        pixels.show()
        sleep(flash_time)


# Main program
def wheel(tail_length):    
    tail_positions = [(i+10*i)%255 for i in range(tail_length)]
    color_seqment = [advance_color(i) for i in tail_positions]

    #loop_i = 0
    try:
        loop_i = 0
        while True:
            for index in range(len(pixels)):
                    random_pixel_index = flash_random_pixel(pixels, 0.001)
                    clear(pixels) 
                    color_seqment = adjust_tail([advance_color(i%255) for i in tail_positions])
                    print(color_seqment)
                    for tail_i in range(tail_length):
                        turn_on(pixels, index-tail_i, color_seqment[tail_i])
            
                    pixels.show()
                    sleep(0.001)
                    tail_positions = [i+2 for i in tail_positions]
                    loop_i += 1
            break
        print('Winner is number {}'.format(random_pixel_index))
        flash_pixel(pixels, random_pixel_index, RED, 0.3)
    except KeyboardInterrupt:
        clear(pixels)
        pixels.show()
        pass

    print('\nExiting')
    clear(pixels)
    pixels.show()



if __name__ == '__main__':
    wheel(5)
