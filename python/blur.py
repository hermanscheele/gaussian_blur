import numpy as np
import matplotlib.pyplot as plt
from skimage import img_as_float, color
import imageio.v3 as iio

img = iio.imread("./imgs/me.png")
img_grey = color.rgb2gray(img)
img = img_as_float(img_grey).T
dims = img.shape



# plt.imshow(img, cmap='gray')
# plt.show()



# gaussian blur
def g(dx:float, dy:float, sigma:float) -> float:
    return np.exp(-(dx**2 + dy**2) / (2*sigma**2))

# build kernel
def kernel(dim:int, g, sig:float) -> np.array:
    k = np.zeros((dim, dim))
    r = dim // 2
    for dx in range(-r,r+1):
        for dy in range(-r,r+1):
            k[dx+r,dy+r] = g(dx,dy,sig) 
    
    k /= k.sum()
    return k

print("")
k = kernel(3, g, 1)
print("kernel result:")
print(k)



# test








# test2
# px = np.random.rand(3,3)
# for i in range(3):
#     for j in range(3):







def apply_kernel(px):
    dims = px.shape
    n_rows = dims[0]
    n_cols = dims[1]

    for i in range(n_rows):
        for j in range(n_cols):
            pass








# def apply_kernel(px:np.array, g:function, sig:float):
#     dims = px.shape
#     n_rows = dims[0] - 1
#     n_cols = dims[1] - 1
#     blur = np.zeros(dims)

#     for i in range(n_rows):
#         for j in range(n_cols):

            
#             neighs = []

#             # if top
#                 # if left corn.
#                 # if right corn.
#                 # else
#             if i == 0:
#                 if j == 0:
#                     # neighs.append((0, 1))
#                     # neighs.append((1, 1))
#                     # neighs.append((1, 0))
#                     blur[i]
#                     blur[][j] = g(0, 1, sig)
#                     blur[i][j] = g(1, 1, sig)
#                     blur[i][j] = g(1, 0, sig)

#                 elif j == n_cols:
#                     neighs.append()
                    
#                 else:
#                     pass        

#             # if floor
#                 # if left corn.
#                 # if right corn.
#                 # else

#             # if left wall
#                 # if top corn.
#                 # if floor corn.
#                 # else

#             # if right wall
#                 # if top corn.
#                 # if floor corn.
#                 # else



#     pass