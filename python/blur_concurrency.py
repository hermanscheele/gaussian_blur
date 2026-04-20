import numpy as np
import matplotlib.pyplot as plt
from skimage import img_as_float, color
import imageio.v3 as iio
from multiprocessing import Pool, cpu_count
from blur import blur
import time


img = iio.imread("./imgs/me.png")
img_grey = color.rgb2gray(img)
img = img_as_float(img_grey)
dims = img.shape


# plt.imshow(img, cmap='grey')
# plt.show()


cores = cpu_count()
k_dim = 3
sig = 1.0


def blur_rows(rows):
    return blur(rows, k_dim, sig)

chunks = np.array_split(img, cores)



if __name__ == '__main__':

    # sequential blurring
    start = time.time()
    blurrd = blur(img, k_dim, sig)
    end = time.time()
    s_t = end - start
    print(f'sequential_t: {s_t} s')

    # parallel blurring (cores = 12)
    start = time.time()
    with Pool(cores) as p:
        results = p.map(blur_rows, chunks)
    blurred = np.vstack(results)
    end = time.time()
    p_t = end - start
    print(f'parallel_t: {p_t} s')


    print(f'speedup: {s_t / p_t}')


