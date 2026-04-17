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


# weighted sum
def w_sum(x:float, neighs:np.array, k:np.array) -> float:
    sx = 0.0
    rows, cols = neighs.shape
    for i in range(rows):
        for j in range(cols):
            sx += neighs[i, j] * k[i, j]
    return sx     



# ----------- test
pxs = np.random.rand(3,3)
c = pxs[1,1]
neighs = pxs

k = kernel(3, g, 1)
w = w_sum(c, neighs, k)
print(w)





def blur(px, k_dimdim:int, sig:float):
    dims = px.shape
    n_rows = dims[0]
    n_cols = dims[1]
    b = np.zeros(dims)
    k = kernel(k_dim,sig)
    
    for i in range(n_rows):
        for j in range(n_cols):
            
            neighs = np.zeros(k_dim,k_dim)
            # if top
            if i == 0:
        
                # if left corn.
                if j == 0:
                    neighs[1][2] = px[i][j+1]
                    neighs[2][1] = px[i+1][j]
                    neighs[2][2] = px[i+1][j+1]
                    
            
                # if right corn.
                elif j == dims[1] - 1:
                    neighs[1][0] = px[i][j-1]
                    neighs[0][0] = px[i+1][j-1]
                    neighs[2][1] = px[i+1][j]
                    
                # else
                else:
                    neighs[1][2] = px[i][j+1]
                    neighs[2][1] = px[i+1][j]
                    neighs[2][2] = px[i+1][j+1]
                    neighs[1][0] = px[i][j-1]
                    neighs[2][0] = px[i+1][j-1]
            # if floor
                # if left corn.
                # if right corn.
                # else

            # if left wall
                # if top corn.
                # if floor corn.
                # else

            # if right wall
                # if top corn.
                # if floor corn.
                # else


            # else (interior)



            pass


