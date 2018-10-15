from PIL import Image
import math
import numpy as np

busy_image = 'drops.jpg'
landscape_image = 'fog.jpg'
face_image = 'face.jpg'
free_choice_image = 'antique.jpg'
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
            r = np.sqrt(dx*dx + dy*dy)
            if r > radius:
                pixel_location_matrix[i][j][0] = i
                pixel_location_matrix[i][j][1] = j
                pixel_location_matrix[i][j][2] = 1
            else:
                beta = np.arctan2(dy, dx)
                beta += angle*(radius - r)/radius
                pixel_i = center[0] + r*np.sin(beta)
                pixel_j = center[1] + r*np.cos(beta)
                pixel_location_matrix[i][j][0] = pixel_i
                pixel_location_matrix[i][j][1] = pixel_j
    return pixel_location_matrix


def ripple(tao_x, tao_y, a_x, a_y, height, width):
    print("executing ripple routine in image")
    pixel_location_matrix = np.zeros(shape=(height, width, 3))
    for i in range(0, height):
        for j in range(0, width):
            pixel_location_matrix[i][j][0] = i + a_y*np.sin((2*math.pi*j)/tao_y)
            pixel_location_matrix[i][j][1] = j + a_x*np.sin((2*math.pi*i)/tao_x)
    return pixel_location_matrix


def spherical(center, radius, height, width, ro):
    print("executing spherical routine in image")
    pixel_location_matrix = np.zeros(shape=(height, width, 3))
    for i in range(0, height):
        for j in range(0, width):
            dy = i - center[0]
            dx = j - center[1]
            r = np.sqrt(dx*dx + dy*dy)
            if r >= radius:
                pixel_location_matrix[i][j][0] = i
                pixel_location_matrix[i][j][1] = j
                pixel_location_matrix[i][j][2] = 1
            else:
                z = np.sqrt(radius*radius - r*r)
                beta_x = (1 - 1/ro)*np.arcsin(dx/(np.sqrt(dx*dx + z*z)))
                beta_y = (1 - 1/ro)*np.arcsin(dy/(np.sqrt(dy*dy + z*z)))
                pixel_i = i - z*np.tan(beta_y)
                pixel_j = j - z*np.tan(beta_x)
                pixel_location_matrix[i][j][0] = pixel_i
                pixel_location_matrix[i][j][1] = pixel_j
    return pixel_location_matrix


def rotation(angle, height, width):
    print("executing rotation routine in image")
    pixel_location_matrix = np.zeros(shape=(height, width, 3))
    # resize_x_max = width
    # resize_y_max = height
    # resize_x_min = 0
    # resize_y_min = 0
    for i in range(0, height):
        for j in range(0, width):
            pixel_i = - j*np.sin(angle) + i*np.cos(angle)
            pixel_j = j*np.cos(angle) + i*np.sin(angle)
            # if pixel_j < resize_x_min:
            #     resize_x_min = int(pixel_j)
            # elif pixel_j > resize_x_max:
            #     resize_x_max = int(pixel_j)
            # if pixel_i < resize_y_min:
            #     resize_y_min = int(pixel_i)
            # elif pixel_i > resize_y_max:
            #     resize_y_max = int(pixel_i)
            pixel_location_matrix[i][j][0] = pixel_i
            pixel_location_matrix[i][j][1] = pixel_j
    return pixel_location_matrix  # , [resize_x_max, resize_x_min, resize_y_max, resize_y_min]


def interpol_lin(image_as_array, location_matrix, transformation_name, height, width, my_image, black=False):
    print("executing interpolation routine")
    print("this may take a while...")
    # if resize:
    #     new_width = resize[0] - resize[1]
    #     new_height = resize[0] - resize[1]
    #     new_image = np.zeros(shape=(new_height, new_width, 3))
    # else:
    new_image = np.copy(image_as_array)
    #     resize = [0]*4
    for i in range(0, height):
        for j in range(0, width):
            if location_matrix[i][j][2] == 1:
                continue
            y = float(location_matrix[i][j][0])
            x = float(location_matrix[i][j][1])
            v0 = int(location_matrix[i][j][0])
            u0 = int(location_matrix[i][j][1])
            if black:
                if u0 < 0 or v0 < 0 or u0 > width-2 or v0 > height-2:
                    new_image[i, j][0] = 0
                    new_image[i, j][1] = 0
                    new_image[i, j][2] = 0
                    continue
            else:
                if u0 < 0:
                    u0 = 0
                if v0 < 0:
                    v0 = 0
                if u0 > width-2:
                    u0 = width-2
                if v0 > height-2:
                    v0 = height-2
            for k in range(0, 3):
                new_image[i, j][k] = int((1 - x + u0)*(1 - y + v0)*image_as_array[v0, u0][k] +
                                         (x - u0)*(1 - y + v0)*image_as_array[v0, u0 + 1][k] +
                                         (1 - x + u0)*(y - v0)*image_as_array[v0 + 1, u0][k] +
                                         (x - u0)*(y - v0)*image_as_array[v0 + 1, u0 + 1][k])
    return_image = Image.fromarray(new_image)
    return_image.save(my_image[:-4] + "_"+transformation_name + my_image[-4:])


def twirl_image(image_name):
    im = Image.open(image_name)
    width, height = im.size
    my_center = [int(height/5), int(width/5)]
    my_radius = int(max(height/2, width/2))
    my_angle = math.pi
    im_as_array = prepare_image(image_name)
    interpol_lin(im_as_array, twirl(my_center, my_radius, my_angle, height, width),
                 "twirl", height, width, image_name)


def ripple_image(image_name):
    im = Image.open(image_name)
    width, height = im.size
    tao_x = 1
    tao_y = 200
    a_x = 0*width/20
    a_y = height/20
    im_as_array = prepare_image(image_name)
    interpol_lin(im_as_array, ripple(tao_x, tao_y, a_x, a_y, height, width),
                 "ripple", height, width, image_name)


def spherical_image(image_name):
    im = Image.open(image_name)
    width, height = im.size
    my_center = [int(height / 3), int(width / 5)]
    my_radius = int(min(height / 5, width / 5))
    ro = 5
    im_as_array = prepare_image(image_name)
    interpol_lin(im_as_array, spherical(my_center, my_radius, height, width, ro),
                 "spherical", height, width, image_name)


def rotate_image(image_name):
    im = Image.open(image_name)
    width, height = im.size
    angle = math.pi/20
    im_as_array = prepare_image(image_name)
    interpol_lin(im_as_array, rotation(angle, height, width),
                 "rotation", height, width, image_name, True)


def turn_gray(image_as_array):
    gray_image = np.zeros(shape=(len(image_as_array), len(image_as_array[0])))
    for i in range(0, len(image_as_array)):
        for j in range(0, len(image_as_array[i])):
            gray_image[i][j] = int(min(image_as_array[i, j][0], image_as_array[i, j][1],
                                   image_as_array[i, j][2]) +
                                   max(image_as_array[i, j][0], image_as_array[i, j][1],
                                       image_as_array[i, j][2]))/2
    return gray_image


# def detect_edges_sobel(image_name, threshold=100):
#     im = Image.open(image_name)
#     im_as_array = prepare_image(image_name)
#     width, height = im.size
#     gray_image = turn_gray(im_as_array)
#     edges_image = np.copy(im_as_array)
#     for i in range(1, height-1):
#         for j in range(1, width-1):
#             gx = int(gray_image[i-1][j-1] + 2*gray_image[i][j-1] + gray_image[i+1][j-1])
#             gx += -int(gray_image[i-1][j+1] + 2*gray_image[i][j+1] + gray_image[i+1][j+1])
#             gy = int(gray_image[i-1][j-1] + 2*gray_image[i-1][j] + gray_image[i-1][j+1])
#             gy += -int(gray_image[i+1][j-1] + 2*gray_image[i+1][j] + gray_image[i+1][j+1])
#             m = math.sqrt(gx*gx + gy*gy)
#             # print(i, j, m)
#             if m > threshold:
#                 edges_image[i][j][0] = 0
#                 edges_image[i][j][1] = 0
#                 edges_image[i][j][2] = 0
#             else:
#                 edges_image[i][j][0] = 255
#                 edges_image[i][j][1] = 255
#                 edges_image[i][j][2] = 255
#     return_image = Image.fromarray(edges_image)
#     return_image.save(image_name[:-4] + "_" + "edges_sobel" + image_name[-4:])


def detect_edges_sobel(image_name, threshold=50):
    im = Image.open(image_name)
    im_as_array = prepare_image(image_name)
    width, height = im.size
    edges_image = np.copy(im_as_array)
    for i in range(1, height-1):
        for j in range(1, width-1):
            for k in range(0, 3):
                gx = int(im_as_array[i-1][j-1][k] + 2*im_as_array[i][j-1][k] + im_as_array[i+1][j-1][k])
                gx += -int(im_as_array[i-1][j+1][k] + 2*im_as_array[i][j+1][k] + im_as_array[i+1][j+1][k])
                gy = int(im_as_array[i-1][j-1][k] + 2*im_as_array[i-1][j][k] + im_as_array[i-1][j+1][k])
                gy += -int(im_as_array[i+1][j-1][k] + 2*im_as_array[i+1][j][k] + im_as_array[i+1][j+1][k])
                m = np.sqrt(gx*gx + gy*gy)
                if m > threshold:
                    # print(i, j, k, m)
                    edges_image[i][j][0] = 0
                    edges_image[i][j][1] = 0
                    edges_image[i][j][2] = 0
                    break
                elif k == 2:
                    edges_image[i][j][0] = 255
                    edges_image[i][j][1] = 255
                    edges_image[i][j][2] = 255
    return_image = Image.fromarray(edges_image)
    return_image.save(image_name[:-4] + "_" + "edges_sobel_" + str(threshold) + image_name[-4:])


def detect_edges_prewitt(image_name, threshold=50):
    im = Image.open(image_name)
    im_as_array = prepare_image(image_name)
    width, height = im.size
    edges_image = np.copy(im_as_array)
    for i in range(1, height-1):
        for j in range(1, width-1):
            for k in range(0, 3):
                m1 = int(im_as_array[i+1][j-1][k]) + int(im_as_array[i+1][j][k]) + int(im_as_array[i+1][j+1][k])\
                    - (int(im_as_array[i-1][j-1][k]) + int(im_as_array[i-1][j][k]) + int(im_as_array[i-1][j+1][k]))
                m2 = int(im_as_array[i+1][j][k]) + int(im_as_array[i+1][j+1][k]) + int(im_as_array[i][j+1][k])\
                    - (int(im_as_array[i][j-1][k]) + int(im_as_array[i-1][j-1][k]) + int(im_as_array[i-1][j][k]))
                m3 = int(im_as_array[i+1][j+1][k]) + int(im_as_array[i][j+1][k]) + int(im_as_array[i-1][j+1][k]) \
                    - (int(im_as_array[i+1][j-1][k]) + int(im_as_array[i][j-1][k]) + int(im_as_array[i-1][j-1][k]))
                m4 = int(im_as_array[i][j+1][k]) + int(im_as_array[i-1][j+1][k]) + int(im_as_array[i-1][j][k])\
                    - (int(im_as_array[i][j-1][k]) + int(im_as_array[i-1][j-1][k]) + int(im_as_array[i+1][j][k]))
                m5 = -(int(im_as_array[i+1][j-1][k]) + int(im_as_array[i+1][j][k]) + int(im_as_array[i+1][j+1][k]))\
                    + int(im_as_array[i-1][j-1][k]) + int(im_as_array[i-1][j][k]) + int(im_as_array[i-1][j+1][k])
                m6 = -(int(im_as_array[i+1][j][k]) + int(im_as_array[i+1][j+1][k]) + int(im_as_array[i][j+1][k]))\
                    + int(im_as_array[i][j-1][k]) + int(im_as_array[i-1][j-1][k]) + int(im_as_array[i-1][j][k])
                m7 = -(int(im_as_array[i+1][j+1][k]) + int(im_as_array[i][j+1][k]) + int(im_as_array[i-1][j+1][k]))\
                    + int(im_as_array[i+1][j-1][k]) + int(im_as_array[i][j-1][k]) + int(im_as_array[i-1][j-1][k])
                m8 = -(int(im_as_array[i][j+1][k]) + int(im_as_array[i-1][j+1][k]) + int(im_as_array[i-1][j][k])) \
                    + int(im_as_array[i][j-1][k]) + int(im_as_array[i-1][j-1][k]) + int(im_as_array[i+1][j][k])
                m = max(m1, m2, m3, m4, m5, m6, m7, m8)
                if m > threshold:
                    # print(i, j, k, m)
                    edges_image[i][j][0] = 0
                    edges_image[i][j][1] = 0
                    edges_image[i][j][2] = 0
                    break
                elif k == 2:
                    edges_image[i][j][0] = 255
                    edges_image[i][j][1] = 255
                    edges_image[i][j][2] = 255
    return_image = Image.fromarray(edges_image)
    return_image.save(image_name[:-4] + "_" + "edges_prewitt_" + str(threshold) + image_name[-4:])


if __name__ == "__main__":
    # twirl_image(face_image)
    # ripple_image(free_choice_image)
    # spherical_image(busy_image)
    # rotate_image(landscape_image)
    # detect_edges_sobel(face_image, threshold=100)
    # detect_edges_sobel(free_choice_image, threshold=50)
    # detect_edges_sobel(free_choice_image, threshold=100)
    # detect_edges_sobel(busy_image, threshold=50)
    # detect_edges_sobel(busy_image, threshold=100)
    # detect_edges_sobel(landscape_image, threshold=50)
    # detect_edges_sobel(landscape_image, threshold=100)
    detect_edges_prewitt(face_image, threshold=50)
