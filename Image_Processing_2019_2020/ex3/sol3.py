import numpy as np
from skimage.color import rgb2gray
from imageio import imread
from scipy.ndimage.filters import convolve
import matplotlib.pyplot as plt
import os

GRAY_CODE = 1
RGB_CODE = 2
MAX_GRAY_LEVEL = 255


def read_image(filename, representation):
    """
    :param filename: the full path to the image file
    :param representation: the representation code defining whether the image
    output should be a grayscale or RGB image
    :return: an image represented by a matrix of type np.float64
    """

    def is_rgb(image):
        """
        :param image: either a gray image or a RGB image
        :return: true if image is RGB, false if image is gray
        """
        return len(image.shape) == 3

    image_matrix = imread(filename)
    image_matrix = np.asarray(image_matrix)

    if representation == GRAY_CODE:
        # the rgb2gray makes sure that the image returned is of type np.float64
        # the image is returned normalized as default if its rgb. it its a gray
        # image we need to normalize it
        if is_rgb(image_matrix):
            return (rgb2gray(image_matrix)).astype(np.float64)
        else:
            to_return = (image_matrix / MAX_GRAY_LEVEL).astype(np.float64)
        return to_return

    elif representation == RGB_CODE:
        # the normalization operation makes sure that the image returned is of
        # type np.float64
        return (image_matrix / MAX_GRAY_LEVEL).astype(np.float64)


def get_filter(filter_size):
    """
    :param filter_size:
    :return: the appropriate filter for the given sizeb
    """
    GAUSSIAN_FILTER = np.array([0.5, 0.5])

    if filter_size == 1:
        return np.array([1]).reshape((1, filter_size))

    to_return = GAUSSIAN_FILTER
    for i in range(filter_size - 2):
        to_return = np.convolve(to_return, GAUSSIAN_FILTER)

    return to_return.reshape((1, filter_size))


def blur_image(im, filter_vec):
    """
    :param im:
    :param filter_vec:
    :return: blurs the given image with the given filter
    once along the rows and once along the columns
    """
    to_return = convolve(im, filter_vec)
    to_return = convolve(to_return, filter_vec.T)

    return to_return


def reduce_image(im, filter_vec):
    """
    :param im:
    :param filter_vec:
    :return: blurs and reduces the given image
    """
    to_return = blur_image(im, filter_vec)

    # now reduce the image size by taking every even pixel
    return to_return[1::2, 1::2]


def expand(im_to_expand, filter_vec):
    """
    :param im_to_expand:
    :param filter_vec:
    :return: an expanded image
    the reduce_image and expand function cancel each other out if the image
    is of the size of a power of 2
    """
    number_of_rows_for_new_im = im_to_expand.shape[0] * 2
    number_of_cols_for_new_im = im_to_expand.shape[1] * 2
    shape_for_new_im = (number_of_rows_for_new_im, number_of_cols_for_new_im)

    new_im = np.zeros(shape_for_new_im)

    new_im[0::2, 0::2] = im_to_expand

    # now blur the new image
    # to preserve brightness we use 2*filter_vec since we added many zeros
    return blur_image(new_im, 2 * filter_vec)


def build_gaussian_pyramid(im, max_levels, filter_size):
    """
    :param im: a grayscale image with values between 0 and 1
    :param max_levels: the maximum number of levels in the resulting pyramid
    :param filter_size: the size of the gaussian filter
    :return:
    pyr - a standard python array with maximum length of max_levels
    such that each entry is a grayscale image. pyr[0] would be the original image.
    the last image height or width wont be smaller than 16.
    filter_vec - a row vector of the shape (1, filter_size)
    """

    ######## what to do about the image edges?
    MINIMUM_WIDTH = 16
    filter_vec = get_filter(filter_size)

    pyr = [np.matrix.copy(im)]

    for i in range(1, max_levels):
        next_im = reduce_image(pyr[i - 1], filter_vec)
        if min(next_im.shape) < MINIMUM_WIDTH:
            break
        pyr.append(next_im)

    return pyr, filter_vec


def build_laplacian_pyramid(im, max_levels, filter_size):
    """

    :param im: a grayscale image with values between 0 and 1
    :param max_levels: the maximum number of levels in the resulting pyramid
    :param filter_size: the size of the gaussian filter
    :return:
    pyr - a standard python array with maximum length of max_levels
    such that each entry is a grayscale image. pyr[0] would be the original image.
    the last image height or width wont be smaller than 16.
    filter_vec - a row vector of the shape (1, filter_size)
    """
    gaussian_pyramid, filter_vec = build_gaussian_pyramid(im, max_levels, filter_size)

    pyr = [None for _ in range(len(gaussian_pyramid))]

    # set the last laplacian to be the last gaussian
    pyr[-1] = gaussian_pyramid[-1]

    for i in range(len(pyr) - 2, -1, -1):
        pyr[i] = gaussian_pyramid[i] - expand(gaussian_pyramid[i + 1], filter_vec)

    return pyr, filter_vec


def laplacian_to_image(lpyr, filter_vec, coeff):
    """
    :param lpyr: laplacian pyramid
    :param filter_vec: the filter_vec returned by the
    build_laplacian_pyramid function
    :param coeff: will multiply each im in the pyramid by the scalars
    in this list
    :return: an image
    """

    lpyr_after_multiply = []
    for i in range(len(lpyr)):
        lpyr_after_multiply.append(lpyr[i] * coeff[i])

    current_gaussian = lpyr_after_multiply[-1]
    for i in range(len(lpyr) - 2, -1, -1):
        current_gaussian = expand(current_gaussian, filter_vec) + lpyr_after_multiply[i]

    return current_gaussian


def normalize_image_to_0_1(im):
    """
    :param im: a grayscale image
    :return: the normalized image
    """
    return (im - np.min(im)) / np.max(im)


def render_pyramid(pyr, levels):
    """
    :param pyr: either a Gaussian or Laplacian pyramid
    :param levels: how many levels to take
    :return: the resulting image
    """
    # first normalize the images to be in the range of 0 to 1
    pyr_normalized = list(map(normalize_image_to_0_1, pyr[:levels]))

    # now add rows of zeros to each image in the pyramid so that
    # its would match horizontally to the first image in the pyramid
    number_of_rows_in_first = pyr_normalized[0].shape[0]
    for i in range(1, len(pyr_normalized)):
        cur_im = pyr_normalized[i]
        number_of_rows_in_cur = cur_im.shape[0]
        number_of_cols_in_cur = cur_im.shape[1]
        number_of_rows_to_add = number_of_rows_in_first - number_of_rows_in_cur
        zeros_to_add = np.zeros((number_of_rows_to_add, number_of_cols_in_cur))

        cur_im = np.append(cur_im, zeros_to_add, axis=0)

        pyr_normalized[i] = cur_im

    return np.hstack(pyr_normalized)


def display_pyramid(pyr, levels):
    """
    :param pyr: either a Gaussian or Laplacian pyramid
    :param levels: how many levels to take
    displayes the image returned by the render_pyramid function
    """
    im_to_display = render_pyramid(pyr, levels)
    plt.imshow(im_to_display, cmap='gray')
    plt.show()


def pyramid_blending(im1, im2, mask, max_levels, filter_size_im, filter_size_mask):
    """
    :param im1: grayscale image
    :param im2: grayscale image
    :param mask: a boolean mask, 1 means to take the corresponding part from
    im1, and 0 means to take the corresponding part from im2
    :param max_levels: the max_levels parameter to pass to the function that would generate
    the pyramids of the images
    :param filter_size_im: the filter_size parameter to pass to the function that would generate
    the laplacian pyramids of the images
    :param filter_size_mask: the filter_size parameter to pass to the function that would generate
    the gaussian pyramid of the mask
    :return: im_blend - the blended image
    """
    lpyr1, filter_vec1 = build_laplacian_pyramid(im1, max_levels, filter_size_im)
    lpyr2, filter_vec2 = build_laplacian_pyramid(im2, max_levels, filter_size_im)

    # convert the mask to double, since fractional values should
    # appear while constructing the mask’s pyramid
    mask = mask.astype(np.float64)
    lpyr_mask, filter_vec_mask = build_gaussian_pyramid(mask, max_levels, filter_size_mask)

    lpyr_im_blend = []
    for i in range(len(lpyr1)):
        new_laplacian = lpyr_mask[i] * lpyr1[i] + (1 - lpyr_mask[i]) * lpyr2[i]
        lpyr_im_blend.append(new_laplacian)

    # we will take the same amount from each level
    coeff = [1 for _ in range(len(lpyr1))]

    # since we want the resulting image to be like the 2 given images
    # we feed it the filter_vec of one of the images
    im_blend = laplacian_to_image(lpyr_im_blend, filter_vec1, coeff)

    # clip the im_blend to the range [0, 1]
    im_blend = im_blend.clip(0, 1)

    return im_blend


def relpath(filename):
    """
    :param filename: the relative path
    :return: the real path of the file
    """
    return os.path.join(os.path.dirname(__file__), filename)


def blendRGB(im1_filename, im2_filename, mask_filename, max_levels, filter_size_im, filter_size_mask):
    """
    :param im1_filename: path to RGB image
    :param im2_filename: RGB image path to RGB image
    :param mask_filename: path to a boolean mask, 1 means to take the corresponding part from
    im1, and 0 means to take the corresponding part from im2
    :param max_levels: the max_levels parameter to pass to the function that would generate
    the pyramids of the images
    :param filter_size_im: the filter_size parameter to pass to the function that would generate
    the laplacian pyramids of the images
    :param filter_size_mask: the filter_size parameter to pass to the function that would generate
    the gaussian pyramid of the mask
    :return: im_blend - the blended RGB image where each channel was blended separately
    """
    im1 = read_image(im1_filename, RGB_CODE)
    im2 = read_image(im2_filename, RGB_CODE)
    mask = read_image(mask_filename, GRAY_CODE).astype(np.bool)

    im_blend = np.zeros(im1.shape)
    for channel in range(3):
        im1_channel = im1[:, :, channel]
        im2_channel = im2[:, :, channel]
        im_blend_channel = pyramid_blending(im1_channel, im2_channel, mask, max_levels, filter_size_im,
                                            filter_size_mask)
        im_blend[:, :, channel] = im_blend_channel

    return im1, im2, mask, im_blend


def display_all_images_for_blending(im1, im2, mask, im_blend):
    """
    :param im1:
    :param im2:
    :param mask:
    :param im_blend:
    :return: displays the given images in a single plot
    """
    fig, axes = plt.subplots(2, 2)

    axes[0, 0].imshow(im1)
    axes[0, 1].imshow(im2)
    axes[1, 0].imshow(mask, cmap='gray')
    axes[1, 1].imshow(im_blend)
    plt.show()


def blending_example1():
    """
    :return: im1, im2, mask, im_blend which are the input and  result of the first example
    """
    im1_filename = 'externals/exmp1im1.jpg'
    im2_filename = 'externals/exmp1im2.jpg'
    mask_filename = 'externals/mask1.jpg'

    im1_filename = relpath(im1_filename)
    im2_filename = relpath(im2_filename)
    mask_filename = relpath(mask_filename)

    max_levels = 20
    filter_size_im = 5
    filter_size_mask = 5

    im1, im2, mask, im_blend = blendRGB(im1_filename, im2_filename, mask_filename, max_levels, filter_size_im,
                                        filter_size_mask)

    display_all_images_for_blending(im1, im2, mask, im_blend)
    return im1, im2, mask, im_blend


def blending_example2():
    """
    :return: im1, im2, mask, im_blend which are the input and  result of the second example
    """
    im1_filename = 'externals/exmp2im1.jpg'
    im2_filename = 'externals/exmp2im2.jpg'
    mask_filename = 'externals/mask2.jpg'

    im1_filename = relpath(im1_filename)
    im2_filename = relpath(im2_filename)
    mask_filename = relpath(mask_filename)

    max_levels = 20
    filter_size_im = 10
    filter_size_mask = 10

    im1, im2, mask, im_blend = blendRGB(im1_filename, im2_filename, mask_filename, max_levels, filter_size_im,
                                        filter_size_mask)

    display_all_images_for_blending(im1, im2, mask, im_blend)
    return im1, im2, mask, im_blend
