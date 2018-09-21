im1 = 'drops.jpg'
im2 = 'fog.jpg'
im3 = 'face.jpg'
im4 = 'antique.jpg'
test = 'simple.png'
test_small = 'simple.jpg'

from PIL import Image
import math
import numpy as np

my_image = test_small

im = Image.open(my_image)
width, height = im.size
print('this is the image you just loaded:', my_image)
RGB_matrix = im.load()

new_image = [[[0]*3]*width]*height
print(new_image)

# for j in range(0,height):
#     for i in range(0,width):
#         for k in range(0,3):
#             print(RGB_matrix[i,j])
#             new_image[i,j,k] = RGB_matrix[i,j,k]

# for j in range(0,height):
#     for i in range(0,width):
#         if new_image[i,j] == (255,255,255):
#             print('0', end = ' ')
#         else:
#             print('1', end = ' ')
#     print()

def twirl(matrix,center,radius,angle):
    original_pixel_matrix = [[]*width]*height
    for j in range(0,height):     
        for i in range(0,width):
            dx = i - center[0]
            dy = j - center[1]
            r = math.sqrt(dx*dx + dy*dy)
            if r > radius:
                original_pixel_matrix[i,j] = [i,j]
            else:
                betha = np.arctan(dx,dy) + angle*(radius - r)/radius
                pixel_i = center[0] + r*np.cos(betha)
                pixel_j = center[1] + r*np.sin(betha)
                original_pixel_matrix[i,j] = [pixel_i,pixel_j]

    

    # for j in range(0,height):
    #     for i in range(0,width):

        

# for j in range(0,height):
#     for i in range(0,width):
#         if RGB_matrix[i,j] == (255,255,255):
#             print('0', end = ' ')
#         else:
#             print('1', end = ' ')
#     print()
