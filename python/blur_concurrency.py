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
    print(f'sequential_t: {end - start} s')

    # parallel blurring (cores = 12)
    start = time.time()
    with Pool(cores) as p:
        results = p.map(blur_rows, chunks)
    blurred = np.vstack(results)
    end = time.time()
    print(f'parallel_t: {end - start} s')








