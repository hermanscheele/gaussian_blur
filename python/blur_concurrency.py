import numpy as np
import matplotlib.pyplot as plt
from skimage import img_as_float, color
import imageio.v3 as iio
from multiprocessing import Pool, cpu_count
from blur import blur, kernel, g
import time


img = iio.imread("./imgs/city.jpg")
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

#chunks = np.array_split(img, cores)
chunk_size = len(img) // cores - 1
idx = []
for i in range(cores):
    idx.append((chunk_size * i, chunk_size * (i+1))))

def blur_idx(idx):
    return blur(img[idx[0] : idx[1]], k_dim, sig)


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

    plt.imshow(blurred, cmap='grey')
    plt.show()




    # investigation --------------
    # col = blurred[15:19]
    # print(col[:10])
    # k = kernel(3, g, 1.0)
    # print(k)

    # plt.imshow(col, cmap='grey')
    # plt.show()


