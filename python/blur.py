import numpy as np
import matplotlib.pyplot as plt
from skimage import img_as_float, color
import imageio.v3 as iio

img = iio.imread("./imgs/city.jpg")
img_grey = color.rgb2gray(img)
img = img_as_float(img_grey)
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






# weighted sum
def w_sum(neighs:np.array, k:np.array) -> float:
    sx = 0.0
    rows, cols = neighs.shape
    for i in range(rows):
        for j in range(cols):
            sx += neighs[i, j] * k[i, j]
    return sx     



# ----------- test
# pxs = np.random.rand(3,3)
# k = kernel(3, g, 0.5)

# print("pixels")
# print(pxs)
# print("")
# print("kernel")
# print(k)
# print("")





def blur(px, k_dim:int, sig:float):
    dims = px.shape
    n_rows = dims[0]
    n_cols = dims[1]
    b = np.zeros(dims)
    k = kernel(k_dim, g, sig)
    
    r = 0
    for i in range(n_rows):
        r += 1
        # print('row: ', r)

        for j in range(n_cols):

            neighs = np.zeros((k_dim,k_dim))
            neighs[1][1] = px[i][j]
            # if top
            if i == 0:
        
                # if left corn.
                if j == 0:
                    neighs[1][2] = px[i][j+1]
                    neighs[2][1] = px[i+1][j]
                    neighs[2][2] = px[i+1][j+1]
                    
                # if right corn.
                elif j == n_cols - 1:
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
            elif i == n_rows - 1:
                
                # if left corn.
                if j == 0:
                    neighs[0][1] = px[i-1][j]
                    neighs[0][2] = px[i-1][j+1]
                    neighs[1][2] = px[i][j+1]
                
                # if right corner
                elif j == n_cols - 1:
                    neighs[0][0] = px[i-1][j-1]
                    neighs[0][1] = px[i-1][j]
                    neighs[1][0] = px[i][j-1]

                else:
                    neighs[0][1] = px[i-1][j]
                    neighs[0][0] = px[i-1][j-1]
                    neighs[0][2] = px[i-1][j+1]
                    neighs[1][2] = px[i][j+1]
                    neighs[1][0] = px[i][j-1]
            
            else:
                # left wall
                if j == 0:
                    neighs[0][1] = px[i-1][j]
                    neighs[0][2] = px[i-1][j+1]
                    neighs[1][2] = px[i][j+1]
                    neighs[2][1] = px[i+1][j]
                    neighs[2][2] = px[i+1][j+1]

                # right wall
                elif j == n_cols - 1:
                    neighs[0][1] = px[i-1][j]
                    neighs[0][0] = px[i-1][j-1]
                    neighs[1][0] = px[i][j-1]
                    neighs[2][0] = px[i+1][j-1]
                    neighs[2][1] = px[i+1][j]
                
                # interrior 
                else:
                    neighs[0][0] = px[i-1][j-1]
                    neighs[0][1] = px[i-1][j]
                    neighs[0][2] = px[i-1][j+1]
                    neighs[1][0] = px[i][j-1]
                    
                    neighs[1][2] = px[i][j+1]
                    neighs[2][0] = px[i+1][j-1]
                    neighs[2][1] = px[i+1][j]
                    neighs[2][2] = px[i+1][j+1]

            
            b[i,j] = w_sum(neighs, k)
            

    return b





# k_dim = 3
# sig = 30.0

# k = kernel(k_dim, g, sig)
# blurd = blur(img, k_dim, sig)
# print("blurring complete !")
# print(blurd.shape)
# print(k)

# plt.imshow(img, cmap='grey')
# plt.show()

# plt.imshow(blurd, cmap='grey')
# plt.show()




