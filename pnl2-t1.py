from PIL import Image
import math
import numpy as np
import scipy.misc

im1 = 'drops.jpg'
im2 = 'fog.jpg'
face_image = 'face.jpg'
im4 = 'antique.jpg'
size_test = 'antique_test.jpg'
test = 'simple.png'
test_small = 'simple.jpg'


def prepare_image(image_name):
    im = Image.open(image_name)
    width, height = im.size
    print('this is the image you just loaded:', image_name, im.mode, height, 'x', width)
    image_as_array = np.asarray(im)
    return image_as_array


def twirl(center, radius, angle, height, width):
    print("executing twirl routine in image")
    pixel_location_matrix = np.zeros(shape=(height, width, 3))
    for i in range(0, height):
        for j in range(0, width):
            dy = i - center[0]
            dx = j - center[1]
            r = math.sqrt(dx*dx + dy*dy)
            if r > radius:
                pixel_location_matrix[i][j][0] = i
                pixel_location_matrix[i][j][1] = j
            else:
                pixel_location_matrix[i][j][2] = 1
                beta = np.arctan2(dy, dx)
                beta += angle*(radius - r)/radius
                pixel_i = center[0] + r*np.sin(beta)
                pixel_j = center[1] + r*np.cos(beta)
                pixel_location_matrix[i][j][0] = pixel_i
                pixel_location_matrix[i][j][1] = pixel_j
    return pixel_location_matrix


def interpol_lin(image_as_array, location_matrix, transformation_name, height, width, my_image):
    new_image = np.copy(image_as_array)
    for i in range(0, height):
        # new_line = []
        for j in range(0, width):
            if location_matrix[i][j][2] == 0:
                continue
            y = float(location_matrix[i][j][0])
            x = float(location_matrix[i][j][1])
            v0 = int(location_matrix[i][j][0])
            u0 = int(location_matrix[i][j][1])
            if u0 < 0:
                u0 = 0
            if v0 < 0:
                v0 = 0
            if u0 > width-2:
                u0 = width-2
            if v0 > height-2:
                v0 = height-2
            # new_color = [0.0]*3
            for k in range(0, 3):
                new_image[i, j][k] = int((1 - x + u0)*(1 - y + v0)*image_as_array[v0, u0][k] +
                                         (x - u0)*(1 - y + v0)*image_as_array[v0, u0 + 1][k] +
                                         (1 - x + u0)*(y - v0)*image_as_array[v0 + 1, u0][k] +
                                         (x - u0)*(y - v0)*image_as_array[v0 + 1, u0 + 1][k])
            # new_color_tuple = (new_color[0], new_color[1], new_color[2])
            # new_line.append(new_color_tuple)
        # new_image.append(new_line)
    return_image = Image.fromarray(new_image)
    return_image.save(my_image[:-4] + "_"+transformation_name + my_image[-4:])

    # return_image = Image.fromarray(np.array(new_image), im.mode)

    # return_image = Image.new(im.mode, [width, height])
    # image_as_list = []
    # for j in range(0, height)
    #     for i in range(0, width):
    #         image_as_list.append()
    #
    # return_image.putdata(new_image)
    # return_image.save(my_image[:-4] + "_transformed" + my_image[-4:])
    # return_image.save(my_image[:-4] + "_transformed", "png")

    # scipy.misc.imsave("image.png", img)
    # for j in range(0,height):
    #     for i in range(0,width):


# for j in range(0,height):
#     for i in range(0,width):
#         if RGB_matrix[i,j] == (255,255,255):
#             print('0', end = ' ')
#         else:
#             print('1', end = ' ')
#     print()


# def test_image():
#     new_image = np.copy(image_as_array)
#     print(new_image[0, 0])
#     # print(new_image[width-1, height-1])
#     print(new_image[height-1, width-1])
#     new_image[0, 0][0] = 2
#     print(new_image[0, 0])
#     new_image = Image.fromarray(image_as_array)
#     new_image.save(my_image[:-4] + "_test" + my_image[-4:])

    # for j in range(0, height):
    #     new_line = []
    #     for i in range(0, width):
    #         new_color = [0.0] * 3
    #         for k in range(0, 3):
    #             new_color[k] = RGB_matrix[i, j][k]
    #         new_line.append(new_color)
    #     new_image.append(new_line)
    #     return_image = Image.fromarray(np.array(new_image), im.mode)
    #     return_image.save(my_image[:-4] + "_test" + my_image[-4:])


def twirl_image(image_name):
    im = Image.open(image_name)
    width, height = im.size
    my_center = [int(height/2), int(width/2)]
    my_radius = int(min(height/4, width/4))
    my_angle = math.pi
    im_as_array = prepare_image(image_name)
    interpol_lin(im_as_array, twirl(my_center, my_radius, my_angle, height, width),
                 "twirl", height, width, image_name)


if __name__ == "__main__":
    twirl_image(face_image)


