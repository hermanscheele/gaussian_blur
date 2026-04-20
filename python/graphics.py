import numpy as np
import pygame as pg
from blur import img, blurd
import imageio.v3 as iio
from skimage import img_as_float, color
from gol import game_of_life


# img = iio.imread("./imgs/city.jpg")
# img = color.rgb2gray(img)
# print(img.shape)

# k_dim = 3
# sig = 30.0

# k = kernel(k_dim, g, sig)
# blurred = blur(img, k_dim, sig)



BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


img = (img * 255).astype(np.uint8).T
img = np.stack([img, img, img], axis=-1)

blurd = (blurd * 255).astype(np.uint8).T
blurd = np.stack([blurd, blurd, blurd], axis=-1)



pg.init()
clock = pg.time.Clock()
screen = pg.display.set_mode(img.shape[:2])

run = True
i = 1
while run:
    for event in pg.event.get():
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_q:
                run = False

    
    if i % 2 == 0:
        pg.surfarray.blit_array(screen, img)
    else:
        pg.surfarray.blit_array(screen, blurd)
        
    
    i+=1

    clock.tick(1)
    pg.display.flip()   


pg.quit()





# TODO: Make GoL generlizable with width and heigth initializaiton so we can match img dimensions