import copy
import math
import sys
import ex6_helper

#############################################################
# FILE : ex6.py
# WRITER : Daniel Magen
# EXERCISE : intro2cs ex6 2017-2018
# DESCRIPTION: a program used to rotate an image into an horizontal position
#############################################################

MAX_GREY_VALUE = 255  # maximum grey value in image
MIN_GREY_VALUE = 0  # minimum grey value in image

NUMBER_OF_ARGUMENTS = 3  # the number of arguments we are expecting to use
MSG_INVALID_NUMBER_OF_PARAMETERS = "Wrong number of parameters. \
The correct usage is: ex6.py <image_source> <output > <max_diagonal>"


def otsu(image):
    """
    this function receives a grey image 
    and returns an optimal threshold for the image
    """
    max_intra_variance = 0
    th_with_max_var = 0

    for th in range(MAX_GREY_VALUE + 1):
        n_black = 0
        n_white = 0
        mean_black = 0
        mean_white = 0

        for row in image:
            for pixel in row:
                if pixel < th:
                    mean_black += pixel
                    n_black += 1
                else:
                    mean_white += pixel
                    n_white += 1

        if n_black == 0 or n_white == 0:
            continue

        mean_black = mean_black / n_black
        mean_white = mean_white / n_white

        intra_variance = n_black * n_white * (mean_black - mean_white) ** 2

        if intra_variance > max_intra_variance:
            max_intra_variance = intra_variance
            th_with_max_var = th

    return th_with_max_var


def threshold_filter(image):
    """
    this function receives a grey image 
    and returns an image that is only black and white
    using the optimal threshold for the image to determine which pixel 
    will be represented as either black or white
    """
    new_image = copy.deepcopy(image)

    max_intra_variance = otsu(new_image)

    for i in range(len(new_image)):
        for j in range(len(new_image[i])):
            if new_image[i][j] < max_intra_variance:
                new_image[i][j] = MIN_GREY_VALUE
            else:
                new_image[i][j] = MAX_GREY_VALUE

    return new_image


def in_bounds(tuple_of_lengths, tuple_of_location):
    """
    this function receives 
    a tuple representing the max lengths of 
    the different dimensions of an image 
    and a tuple representing a location 
    returns true if the location is in the the bounds given by the 
    length-tuple
    """
    for i, loc in enumerate(tuple_of_location):
        if loc >= tuple_of_lengths[i]:
            return False

        if loc < 0:
            return False

    return True


def calulate_center_of_odd_square_2dmatrix(odd_square_2dmatrix):
    """
    this function receives an odd square 2d matrix 
    and returns its center coordinates
    """
    row_center = (len(odd_square_2dmatrix) - 1) // 2
    col_center = (len(odd_square_2dmatrix[0]) - 1) // 2

    return (row_center, col_center)


def sum_list_of_tuples(list_of_tuples):
    """
    this function receives
    a list of tuples of the same length
    and returns a new tuple of the same length 
    in which each item in index i is the sum of the other tuples
    items at index i
    """
    length_of_tuples = len(list_of_tuples[0])
    sum_of_tpls = [0] * length_of_tuples

    for i in range(length_of_tuples):
        for tpl in list_of_tuples:
            sum_of_tpls[i] += tpl[i]

    return sum_of_tpls


def get_dimension_of_lists(matrix):
    """
    this function receives a square matrix comprised of lists of lists
    returns it's dimensions in an n-tuple
    """
    dimensions = []
    next_dimesion_to_check = matrix

    while (isinstance(next_dimesion_to_check, list)):
        dimensions.append(len(next_dimesion_to_check))
        next_dimesion_to_check = next_dimesion_to_check[0]

    return dimensions


def apply_given_filter_on_location(image, given_filter,
                                   center_of_given_filter,
                                   location_in_image):
    """
    this function receives 
    an image 
    a filter containing numbers
    a tuple representing the center of the filter 
    and a location in the image
    it calculates the sum given by multiplying each pixel in the image
    with a number in the filter that has the same relative position  to the 
    center of the filter as the pixel is to the given location in the image
    """
    dimension_of_image = get_dimension_of_lists(image)

    sum_of_filter_application = 0

    for i in range(len(given_filter)):
        for j in range(len(given_filter[0])):
            relative_i = i - center_of_given_filter[0]
            relative_j = j - center_of_given_filter[1]

            location_to_check = sum_list_of_tuples([location_in_image,
                                                    (relative_i, relative_j)])

            if in_bounds(dimension_of_image, location_to_check):
                sum_of_filter_application += \
                    image[location_to_check[0]][location_to_check[1]] \
                    * given_filter[i][j]
            else:
                sum_of_filter_application += \
                    image[location_in_image[0]][location_in_image[1]] \
                    * given_filter[i][j]

    return sum_of_filter_application


def fix_value_of_filter_application(sum_of_filter_application):
    """
    this function receives a number
    if the number is negative it turns it into it's absolute value
    if the number is not whole, it rounds it to the nearest round number
    if the number exceeds MAX_GREY_VALUE it returns MAX_GREY_VALUE
    """

    if sum_of_filter_application < 0:
        sum_of_filter_application *= -1

    if sum_of_filter_application % 1 > 0:
        sum_of_filter_application -= sum_of_filter_application % 1

    if sum_of_filter_application > MAX_GREY_VALUE:
        return MAX_GREY_VALUE

    return int(sum_of_filter_application)


def apply_filter(image, given_filter):
    """
    this function receives
    a grey image
    a filter which is a matrix of size 3x3
    
    it returns an image of the same dimensions as the given image
    such that each pixel in the new image is calculated by
    taking each pixel as the "center pixel" 
    and multiplying each pixel in the image with a number in the filter that 
    has the same relative position to the center of the filter 
    as the pixel is to the center pixel
    """
    new_image = copy.deepcopy(image)

    center_of_filter = calulate_center_of_odd_square_2dmatrix(given_filter)

    for i in range(len(new_image)):
        for j in range(len(new_image[0])):
            new_image[i][j] = apply_given_filter_on_location(image,
                                                             given_filter,
                                                             center_of_filter,
                                                             (i, j))

            new_image[i][j] = fix_value_of_filter_application(new_image[i][j])

    return new_image


def detect_edges(image):
    """
    this function receives
    a grey image
    
    it returns an image of the same dimensions as the given image
    such that each pixel in the new image is it's value minus 
    the average of all the pixels that are near him
    """
    FILTER_SIZE = 3
    multiply_by = -1 / (FILTER_SIZE ** 2 - 1)

    FILTER_FOR_DETECTING_EDGE = [[multiply_by, multiply_by, multiply_by],
                                 [multiply_by, 1, multiply_by],
                                 [multiply_by, multiply_by, multiply_by]]

    image_after_filter = apply_filter(image, FILTER_FOR_DETECTING_EDGE)

    return image_after_filter


def downsample_by_3(image):
    """
    this function receives an image
    
    it returns an image that has its size reduced by 3 in both the 
    rows and columns
    """
    STRIDE = 3
    divide_by = (STRIDE ** 2)
    filter_for_downsample = [[1] * STRIDE] * STRIDE

    center_of_filter_for_dwnsmpl = \
        calulate_center_of_odd_square_2dmatrix(filter_for_downsample)

    new_image = []
    for i in range(center_of_filter_for_dwnsmpl[0], len(image), STRIDE):
        new_row = []

        for j in range(center_of_filter_for_dwnsmpl[1], len(image[0]), STRIDE):
            sum_of_pixels = \
                apply_given_filter_on_location(image,
                                               filter_for_downsample,
                                               center_of_filter_for_dwnsmpl,
                                               (i, j))
            new_row.append(int(sum_of_pixels / divide_by))

        new_image.append(new_row)

    return new_image


def distance_between_2_points(p1, p2):
    """
    this function receives 2 tuples that represent points
    
    it returns the distance between the 2 points
    """
    return ((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2) ** 0.5


def get_image_diagonal_size(image):
    """
    this function receives an image
    
    and returns its diagonal length
    """
    return distance_between_2_points((len(image), len(image[0])), (0, 0))


def downsample(image, max_diagonal_size):
    """
    this function receives an image and a number
    
    it returns an image that has its size reduced and has a diagonal length 
    that is smaller or equal to that of the the given number
    """
    diagonal_size = get_image_diagonal_size(image)
    new_image = image

    while (diagonal_size > max_diagonal_size):
        new_image = downsample_by_3(new_image)
        diagonal_size = get_image_diagonal_size(new_image)

    return new_image


def calculate_max_jump_that_is_in_range_2(line):
    """
    this function is given a list of coordinates representing a line
    as given in the ex6_helper.pixels_on_line function
    it assumes that the distance between each nearby coordinates is the same
    it returns the max number of indices you can traverse starting from any 
    coordinate, and still stay within distance 2 in the 
    """
    if len(line) < 2:
        return 0

    distance_between_each_index = distance_between_2_points(line[0], line[1])

    return math.floor(2 / distance_between_each_index)


def get_next_white_block(image, line, index_in_line, max_jump):
    """
    this function is given and an image
    
    a list of coordinates representing a line as given 
    in the ex6_helper.pixels_on_line function
    
    an index in the line
    
    and the maximum distance between 2 blocks
    
    returns the index of the closest coordinate in the line list
    that has the value MAX_GREY_VALUE in the 
    
    if there is no such index it returns False
    """
    if index_in_line >= len(line):
        return False

    for i in range(index_in_line, min(index_in_line + max_jump, len(line))):
        if image[line[i][0]][line[i][1]] == MAX_GREY_VALUE:
            return i

    return False


def rank_line(image, line):
    """
    this function receives a black and white image
    
    and a list of coordinates representing a line as given 
    in the ex6_helper.pixels_on_line function
    
    it returns the sum of the squares of the lengths of all the white lines
    in the give line
    such that "a white line" is a consecutive list of white pixels 
    that are at max distance 2 apart
    """
    max_jump_that_in_range_2 = calculate_max_jump_that_is_in_range_2(line)
    rank_of_line = 0
    i = -1

    while i < len(line):
        next_white_pixel = False

        while i < len(line) and next_white_pixel is False:
            i += 1
            next_white_pixel = get_next_white_block(image,
                                                    line,
                                                    i,
                                                    max_jump_that_in_range_2)

        white_line_starting_location = next_white_pixel

        while i < len(line) and next_white_pixel is not False:
            i = next_white_pixel
            next_white_pixel = get_next_white_block(image,
                                                    line,
                                                    i + 1,
                                                    max_jump_that_in_range_2)

        if white_line_starting_location is not False:
            rank_of_line += (1 + i - white_line_starting_location) ** 2

    return rank_of_line


def get_angle(image):
    """
    this function receives a black and white image
    
    it finds the line in the image that has the greatest square lengths 
    of white lines, and returns that line angle with the top of the image
    """
    DEGREES = 180

    max_distance = get_image_diagonal_size(image)
    max_distance = math.ceil(max_distance)

    dominant_angle = 0
    rank_of_dominant_angle = 0

    for angle in range(DEGREES):
        angle_in_radians = math.radians(angle)
        overall_angle_rank = 0

        for distance in range(max_distance + 1):
            line_to_check = ex6_helper.pixels_on_line(image,
                                                      angle_in_radians,
                                                      distance)
            overall_angle_rank += rank_line(image, line_to_check)

            if 0 < angle < 90:
                line_to_check = ex6_helper.pixels_on_line(image,
                                                          angle_in_radians,
                                                          distance,
                                                          top=False)
                overall_angle_rank += rank_line(image, line_to_check)

        if overall_angle_rank > rank_of_dominant_angle:
            rank_of_dominant_angle = overall_angle_rank
            dominant_angle = angle

    return dominant_angle


def rotate_around_center(center_crdnts, current_crdnts, angle_of_rotation):
    """
    this function receives 
    a tuple that represent a center coordinates
    a tuple that represent a coordinates
    an angle of rotation
    
    it returns the point coordinates after being rotated 
    counter clockwise around the center coordinates
    if the resulting coordinate is not whole
    it's values are floored
    """
    x_value = current_crdnts[0] - center_crdnts[0]
    y_value = current_crdnts[1] - center_crdnts[1]
    sin_ang = math.sin(angle_of_rotation)
    cos_ang = math.cos(angle_of_rotation)

    new_x_value = cos_ang * x_value - sin_ang * y_value + center_crdnts[0]
    new_y_value = cos_ang * y_value + sin_ang * x_value + center_crdnts[1]

    return math.floor(new_x_value), math.floor(new_y_value)


def apply_rotation_to_four_coreners(center_crdnts, image, angle_of_rotation):
    """
    this function receives 
    a tuple that represent a center coordinates
    an image
    an angle of rotation
    
    it returns a tuple containing 4 tuples that represent the location of 
    the 4 corner pixels of the image after being rotated by the given angle
    
    """
    image_dimensions = get_dimension_of_lists(image)
    four_corners_rotation_application = []

    for i in range(0, image_dimensions[0], image_dimensions[0] - 1):
        for j in range(0, image_dimensions[1], image_dimensions[1] - 1):
            x_rot, y_rot = rotate_around_center(center_crdnts,
                                                (i, j,),
                                                angle_of_rotation)
            four_corners_rotation_application.append((x_rot, y_rot))

    return four_corners_rotation_application


def by_how_much_to_shift_after_rotation(application_rotation_to_four_coreners):
    """
    this function receives 
    a tuple containing 4 tuples that represent the location of 
    the 4 corner pixels of an image after being rotated by some angle
    
    and returns the absolute values of the min (x,y) of all points
    """
    min_x = min(application_rotation_to_four_coreners, key=lambda tpl: tpl[0])
    min_y = min(application_rotation_to_four_coreners, key=lambda tpl: tpl[1])

    return (abs(min_x[0]), abs(min_y[1]))


def get_image_after_rotation_dimensions(application_rotation_to_four_coreners,
                                        how_shift_after_rotation):
    """
    this function receives 
    a tuple containing 4 tuples that represent the location of 
    the 4 corner pixels of an image after being rotated by some angle
    
    and returns the image dimensions after it's rotation by that angle
    """
    max_x = 0
    max_y = 0

    for corner in application_rotation_to_four_coreners:
        tmp_x, tmp_y = sum_list_of_tuples([corner, how_shift_after_rotation])
        if tmp_x > max_x:
            max_x = tmp_x

        if tmp_y > max_y:
            max_y = tmp_y

    return max_x + 1, max_y + 1


def rotate(image, angle):
    """
    this function receives an image and an angle
    it returns a new image that is the image rotated by the given angle
    in a clockwise direction
    """
    center_coordinates = (len(image) // 2, len(image[0]) // 2)

    application_rotation_to_four_coreners = \
        apply_rotation_to_four_coreners(center_coordinates, image, angle)

    how_shift_after_rotation = \
        by_how_much_to_shift_after_rotation(application_rotation_to_four_coreners)
    # used to determines by how much to shift the resulting rotation 
    # in the x direction and y directions

    image_rotation_dimensions = \
        get_image_after_rotation_dimensions(application_rotation_to_four_coreners,
                                            how_shift_after_rotation)

    new_image = []
    # create new image
    for _ in range(image_rotation_dimensions[0]):
        row = []
        for _ in range(image_rotation_dimensions[1]):
            row.append(MIN_GREY_VALUE)

        new_image.append(row)

    for i in range(len(new_image)):
        for j in range(len(new_image[i])):
            x_adjusted = i - how_shift_after_rotation[0]
            y_adjusted = j - how_shift_after_rotation[1]

            rotation_crdnte = rotate_around_center(center_coordinates,
                                                   (x_adjusted, y_adjusted),
                                                   angle)

            if rotation_crdnte[0] in range(0, len(image)) and \
                    rotation_crdnte[1] in range(0, len(image[0])):
                new_image[i][j] = image[rotation_crdnte[0]][rotation_crdnte[1]]

    return new_image


def make_correction(image, max_diagonal):
    """
    this function receives an image and a number
    the number represents the max length of the diagonal of an image 
    that the program will run it's tests on
    
    using a smaller or equal sized image the function 
    identifies the angle the image is rotated by, and rotates the image
    into a horizontal state
    """
    new_image = downsample(image, max_diagonal)  # make image smaller
    new_image = threshold_filter(new_image)  # make image black and white
    new_image = detect_edges(image)  # edge detection
    new_image = threshold_filter(new_image)  # make image black and white
    dominant_angle = get_angle(new_image)  # get dominant angle in image
    dominant_angle = math.radians(dominant_angle)
    new_image = rotate(image, -dominant_angle)  # rotate image

    return (new_image)


if __name__ == "__main__":
    if len(sys.argv) == NUMBER_OF_ARGUMENTS + 1:
        file_name = sys.argv[1]
        image = ex6_helper.load_image(file_name)

        output_name = sys.argv[2]

        max_diagonal = float(sys.argv[3])

        image = make_correction(image, max_diagonal)

        ex6_helper.save(image, output_name)
    else:
        sys.exit(MSG_INVALID_NUMBER_OF_PARAMETERS)
