from skimage.color import rgb2gray
import matplotlib.pyplot as plt
from imageio import imread
import numpy as np

GRAY_CODE = 1
RGB_CODE = 2
MAX_GRAY_LEVEL = 255

RGB2YIQ_MATRIX = np.array([[0.299, 0.587, 0.114],
                           [0.596, -0.275, -0.321],
                           [0.212, -0.523, 0.311]])

NUMBER_OF_BINS_IN_HISTOGRAM = 256
MINIMAL_VALUE_FOR_HISTOGRAM = 0
MAXIMAL_VALUE_FOR_HISTOGRAM = MAX_GRAY_LEVEL
RANGE_OF_VALUES_FOR_HISTOGRAM = (
    MINIMAL_VALUE_FOR_HISTOGRAM, MAXIMAL_VALUE_FOR_HISTOGRAM)
RANGE_OF_VALUES_FOR_CLIP_1 = (0, 1)
RANGE_OF_VALUES_FOR_CLIP_255 = (0, 255)
LOCATION_OF_HISTOGRAM_IN_NP = 0


def read_image(filename, representation):
    """
    :param filename: the full path to the image file
    :param representation: the representation code defining whether the image
    output should be a grayscale or RGB image
    :return: an image represented by a matrix of type np.float64
    """

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


def display_image_in_plt(image_matrix, representation):
    """
    :param image_matrix: a np matrix representing an image with the range 0-1
    :param representation: representation code
    displays the image as a plt image
    """
    im_to_display = image_matrix.clip(RANGE_OF_VALUES_FOR_CLIP_1[0],
                                      RANGE_OF_VALUES_FOR_CLIP_1[1])

    if representation == GRAY_CODE:
        plt.imshow(im_to_display, cmap='gray')
    elif representation == RGB_CODE:
        # convert the representation to be 0-255 instead of 0-1
        plt.imshow(im_to_display)
    plt.show()


def is_rgb(image):
    """
    :param image: either a gray image or a RGB image
    :return: true if image is RGB, false if image is gray
    """
    return len(image.shape) == 3


def imdisplay(filename, representation):
    """
    :param filename: the full path to the image file
    :param representation: the representation code defining whether the image
    is a grayscale or a RGB image
    """
    image_matrix = read_image(filename, representation)
    display_image_in_plt(image_matrix, representation)


def rgb2yiq(imRGB):
    return imRGB.dot(RGB2YIQ_MATRIX.T)


def yiq2rgb(imYIQ):
    yiq2rgb_matrix = np.linalg.inv(RGB2YIQ_MATRIX)
    return imYIQ.dot(yiq2rgb_matrix.T)


def yiq2gray(imYIQ):
    """
    :param imYIQ: a YIQ image
    :return: the y channel of the image
    """
    y_channel = 0

    return imYIQ[:, :, y_channel]


def histogram_equalize(im_orig):
    """
    :param im_orig: either a grayscale or RGB image if values
    between 0 and 1
    :return: 3 items:
    1) the equalized image
    2) a 256 bin histogram of the original image
    3) a 256 bin histogram of the equalized image
    """
    if is_rgb(im_orig):
        im_given_is_rgb = True
        im_in_yiq_format = rgb2yiq(im_orig)
        im_to_work_with = yiq2gray(im_in_yiq_format)
    else:
        im_given_is_rgb = False
        im_in_yiq_format = None
        im_to_work_with = np.matrix.copy(im_orig)

    # change the values of the im_to_work_with to be integers
    # in the range 0 - 255
    im_to_work_with = im_to_work_with * MAX_GRAY_LEVEL
    im_to_work_with = im_to_work_with.astype(int)

    hist_orig = np.histogram(im_to_work_with, bins=NUMBER_OF_BINS_IN_HISTOGRAM,
                             range=RANGE_OF_VALUES_FOR_HISTOGRAM)[
        LOCATION_OF_HISTOGRAM_IN_NP]

    cumulative_hist = np.cumsum(hist_orig)

    total_number_of_pixels = cumulative_hist[-1]

    # convert the cumulative histogram such that the cumulative
    # histogram of the uniform distribution would be the identity function
    cumulative_hist = cumulative_hist / total_number_of_pixels
    cumulative_hist *= MAX_GRAY_LEVEL

    # now stretch the cumulative histogram linearly
    # the values that become negative will not be mapped anywhere
    # since there are 0 pixels of such values
    cm_index = np.nonzero(cumulative_hist)[0][0]
    cm = cumulative_hist[cm_index]

    # now check that the cumulative histogram contains more than 1
    # non zero value. only change the cumulative histogram if it has more than
    # 1 non zero value, i.e. if its max and min are different. otherwise we
    # will encounter division by zero
    if not cumulative_hist[MAX_GRAY_LEVEL] == cm:
        cumulative_hist = cumulative_hist - cm

    # now change the values in the cumulative histogram to make it the
    # correct mapping function we should use to change the pixel values
    cumulative_hist = cumulative_hist / cumulative_hist[MAX_GRAY_LEVEL]
    cumulative_hist = cumulative_hist * MAX_GRAY_LEVEL
    cumulative_hist = np.round(cumulative_hist)

    # now convert the image according to the correct mapping
    im_eq = cumulative_hist[im_to_work_with]
    im_eq.clip(RANGE_OF_VALUES_FOR_CLIP_255[0],
               RANGE_OF_VALUES_FOR_CLIP_255[1])

    # now calculate the histogram of the new equalized image
    hist_eq = np.histogram(im_eq, bins=NUMBER_OF_BINS_IN_HISTOGRAM,
                           range=RANGE_OF_VALUES_FOR_HISTOGRAM)[
        LOCATION_OF_HISTOGRAM_IN_NP]

    # now change the im_eq to be back in the range 0 - 1
    # (im_to_work_with was converted to be in the range 0 - 255)
    im_eq = im_eq / MAX_GRAY_LEVEL

    if im_given_is_rgb:
        # convert it back to RGB from
        im_in_yiq_format[:, :, 0] = im_eq
        im_eq = yiq2rgb(im_in_yiq_format)

    return [im_eq, hist_orig, hist_eq]


def find_index_of_nearest_value(np_array, value):
    """
    :param np_array: a numpy array
    :param value: the value which should be found
    :return: the index at which the array[index] is closest to the given value
    """
    return (np.abs(np_array - value)).argmin()


def quantize(im_orig, n_quant, n_iter):
    """
    :param im_orig: either a grayscale or RGB image if values
     between 0 and 1
    :param n_quant: number of intensities the output should have
    :param n_iter: maximum number of iterations of the optimization
    :return: 2 things:
    1) a quantized image
    2) error - array with the shape (n_iter) (or less) of the
    total intensities error for each iteration of the quantization process
    """
    if is_rgb(im_orig):
        im_given_is_rgb = True
        im_in_yiq_format = rgb2yiq(im_orig)
        im_to_work_with = yiq2gray(im_in_yiq_format)
    else:
        im_given_is_rgb = False
        im_in_yiq_format = None
        im_to_work_with = np.matrix.copy(im_orig)

    # change the values of the im_to_work_with to be integers
    # in the range 0 - 255
    im_to_work_with = im_to_work_with * MAX_GRAY_LEVEL
    im_to_work_with = np.rint(im_to_work_with)

    hist_im = np.histogram(im_to_work_with, bins=NUMBER_OF_BINS_IN_HISTOGRAM,
                           range=RANGE_OF_VALUES_FOR_HISTOGRAM)[
        LOCATION_OF_HISTOGRAM_IN_NP]

    cumulative_hist = np.cumsum(hist_im)

    total_number_of_pixels = cumulative_hist[-1]

    # to make sure that we never segment the image histogram such that
    # there would exist a whole segment with no pixels (which would cause the
    # program to crash), we would use the cumulative histogram to calculate
    # in which locations we need to segment the image histogram such that each
    # starting segment would have roughly the same number of pixels.
    # note that if the y axis of the cumulative histogram goes from 1 to N then
    # then x such that cum_his(x) = N/k would be an x such that N\k
    # of the image pixels would be smaller than it
    # as such, the first segment locations would be
    # cum_his^(-1) of (i*(N\n_quant))
    # for i in range 0 to n_quant
    z = np.zeros(shape=(n_quant + 1,)).astype(np.float64)
    z[0] = 0  # first separator would always be 0
    # last separator would always 255
    z[n_quant] = NUMBER_OF_BINS_IN_HISTOGRAM - 1

    for i in range(1, n_quant):
        value_to_find = i * (total_number_of_pixels / n_quant)
        z[i] = find_index_of_nearest_value(cumulative_hist, value_to_find)

    # in the lecture we saw that both the q values and the error values
    # are computed by the probability histogram (histogram / number of pixels)
    # but in the lecture we saw that the values are simply computed by the histogram
    # I assume that the lecture is right and compute the errors by the histogram
    # to denote this difference though, I would refer to the histogram as p
    p = hist_im

    # also create the an array zp such that zp[z] = z * p(z)
    zp = np.multiply(p, np.arange(NUMBER_OF_BINS_IN_HISTOGRAM))

    q = np.zeros(shape=(n_quant,)).astype(np.float64)
    error = np.zeros(shape=(0,))

    for i in range(n_iter):
        previous_z = z.copy()
        # in order for us to use the z array in the calculations below
        # we need it to temporarily be of type int
        z = np.rint(z).astype(np.int)
        current_error_for_iter = 0

        # now calculate the new q values
        for j in range(n_quant):
            q[j] = zp[z[j]: z[j + 1] + 1].sum()
            q[j] = q[j] / (p[z[j]: z[j + 1] + 1].sum())

            # now update the error
            deviations_from_q = np.arange(z[j], z[j + 1]) - q[j]
            deviations_from_q = np.square(deviations_from_q)
            error_for_this_q = deviations_from_q.dot(p[z[j]: z[j + 1]])

            current_error_for_iter += error_for_this_q

        error = np.append(error, current_error_for_iter)

        # now calculate the new z values
        # before continuing restore the z array to be of type float64
        z = previous_z.copy()
        for j in range(1, n_quant):
            z[j] = (q[j - 1] + q[j]) / 2

        # now check if there was a convergence, is fo stop
        if np.array_equal(z, previous_z):
            break

    # now round z before using them to remap the image pixels
    z = np.rint(z).astype(np.int)

    def lut(previous_pixel_value):
        """
        :param previous_pixel_value: a value between 0 and 255
        :return: the new value the pixel should have after the quantization
        """
        # find the zi that corresponds to the given pixel
        index_of_zi = 0
        for j in range(1, n_quant):
            if z[j] >= previous_pixel_value:
                break
            index_of_zi = j

        qi = q[index_of_zi]
        return qi

    mapping_function = np.vectorize(lut)
    im_quant = mapping_function(im_to_work_with)

    # now change the im_quant to be back in the range [0,1]
    # (im_to_work_with was converted to be in the range 0 - 255)
    im_quant = im_quant / MAX_GRAY_LEVEL

    if im_given_is_rgb:
        # convert it back to RGB from
        im_in_yiq_format[:, :, 0] = im_quant
        im_quant = yiq2rgb(im_in_yiq_format)

    return [im_quant, error]
