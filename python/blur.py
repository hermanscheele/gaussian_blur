from skimage import img_as_float
import imageio.v3 as iio

img = iio.imread("IMG_9296.png")
img_float = img_as_float(img)


print(img_float)