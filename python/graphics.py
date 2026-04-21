import numpy as np
import pygame as pg
from blur import blur
import imageio.v3 as iio
from skimage import img_as_float, color
from gol import apply_rule, init_grid, gen_random, add_ones, render_grid
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
k_dim = 3
sig = 2.0



img = iio.imread("./imgs/city.jpg")
img_grey = color.rgb2gray(img)
img = np.array(img_as_float(img_grey))
dims = img.shape
print(img.shape)

h = img.shape[0]
w = img.shape[1]

blurd = blur(img, k_dim, sig)

img = (img * 255).astype(np.uint8).T
img = np.stack([img, img, img], axis=-1)

blurd = (blurd * 255).astype(np.uint8).T
blurd = np.stack([blurd, blurd, blurd], axis=-1)

grid = init_grid(w, h)
coordi = gen_random(w, h, 5000)
grid = add_ones(grid, coordi)
render_grid(grid)





pg.init()
clock = pg.time.Clock()
screen = pg.display.set_mode(img.shape[:2])

run = True
buffer_img = img
while run:
    for event in pg.event.get():
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_q:
                run = False


    for i in range(w):
        for j in range(h):
            buffer_img[i,j] = blurd[i,j] if grid[i,j] else img[i,j]
            # render_img[i,j] = 255 if grid[i,j] else img[i,j]

   
    pg.surfarray.blit_array(screen, buffer_img)
    print(np.sum(grid))
    apply_rule(grid)

    clock.tick(100)
    pg.display.flip()   


pg.quit()





