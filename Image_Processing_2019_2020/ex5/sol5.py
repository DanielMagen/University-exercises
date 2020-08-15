from . import sol5_utils
# import sol5_utils
from skimage.color import rgb2gray
from imageio import imread
import numpy as np
import scipy
import random
from tensorflow.keras.layers import Conv2D, Add, Input, Activation
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import Adam

GRAY_CODE = 1
RGB_CODE = 2
MAX_GRAY_LEVEL = 255

SUBTRACT_FROM_EACH_PIXEL = 0.5
CHANNELS_FOR_GRAY_IMAGE = 1


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


def load_dataset(filenames, batch_size, corruption_func, crop_size):
    """
    :param filenames: a list of filenames
    :param batch_size:
    :param corruption_func:
    :param crop_size:
    :return: a generator that outputs random tuples of the form (source_batch, target_batch)
    where each output variable has the shape (batch_size, height, width, 1)
    target_batch = clean
    source_batch = corrupted according to the corruption_func
    """
    height, width = crop_size
    apply_corruption_on_size_times = 3
    height_of_corruption_patch = height * apply_corruption_on_size_times
    width_of_corruption_patch = width * apply_corruption_on_size_times

    loaded_into_memory = {}

    while True:
        chosen_batch_paths = random.choices(filenames, k=batch_size)
        chosen_batch = []

        # now check if those images are loaded into memory and if not load them
        for im_path in chosen_batch_paths:
            if im_path not in loaded_into_memory:
                loaded_into_memory[im_path] = read_image(im_path, GRAY_CODE)
            chosen_batch.append(loaded_into_memory[im_path])

        # now crop the images
        source_batch = []
        target_batch = []

        for im in chosen_batch:
            current_im_height, current_im_width = im.shape
            starting_row = np.random.randint(0, current_im_height - height_of_corruption_patch)
            starting_col = np.random.randint(0, current_im_width - width_of_corruption_patch)
            im_crop = im[starting_row:starting_row + height_of_corruption_patch,
                      starting_col:starting_col + width_of_corruption_patch]

            # now choose which inner patch to crop from the slightly larger crop
            current_im_height, current_im_width = im_crop.shape
            starting_row = np.random.randint(0, current_im_height - height)
            starting_col = np.random.randint(0, current_im_width - width)

            target_batch.append(im_crop[starting_row:starting_row + height,
                                starting_col:starting_col + width].reshape(height, width, CHANNELS_FOR_GRAY_IMAGE))

            source_batch.append(corruption_func(im_crop)[starting_row:starting_row + height,
                                starting_col:starting_col + width].reshape(height, width, CHANNELS_FOR_GRAY_IMAGE))

        source_batch = np.array(source_batch) - SUBTRACT_FROM_EACH_PIXEL
        target_batch = np.array(target_batch) - SUBTRACT_FROM_EACH_PIXEL

        yield source_batch, target_batch


def resblock(input_tensor, num_channels):
    """
    :param input_tensor:
    :param num_channels:
    :return: output_tensor as described in the resnet block specification
    """
    conv1 = Conv2D(filters=num_channels, kernel_size=(3, 3), padding='same')(input_tensor)
    relu = Activation('relu')(conv1)
    conv2 = Conv2D(filters=num_channels, kernel_size=(3, 3), padding='same')(relu)
    addition = Add()([input_tensor, conv2])

    return Activation('relu')(addition)


def build_nn_model(height, width, num_channels, num_res_blocks):
    num_channels_for_last_conv_layer = 1

    inp = Input(shape=(height, width, CHANNELS_FOR_GRAY_IMAGE))
    starting_layer = Conv2D(filters=num_channels, kernel_size=(3, 3), padding='same')(inp)
    starting_layer = Activation('relu')(starting_layer)

    current_layer = starting_layer
    for _ in range(num_res_blocks):
        current_layer = resblock(current_layer, num_channels)

    current_layer = Conv2D(filters=num_channels_for_last_conv_layer, kernel_size=(3, 3), padding='same')(
        current_layer)
    addition = Add()([inp, current_layer])

    return Model(inputs=inp, outputs=addition)


def train_model(model, images, corruption_func, batch_size,
                steps_per_epoch, num_epochs, num_valid_samples):
    """
    :param model:
    :param images:
    :param corruption_func:
    :param batch_size:
    :param steps_per_epoch:
    :param num_epochs:
    :param num_valid_samples:
    """
    percentage_of_test = 0.8
    num_of_testing_samples = int((len(images) * percentage_of_test))
    testing_data = images[:num_of_testing_samples]
    validation_data = images[num_of_testing_samples:]

    crop_height = model.input_shape[1]
    crop_width = model.input_shape[2]
    crop_size = (crop_height, crop_width)
    train_generator = load_dataset(testing_data, batch_size, corruption_func, crop_size)
    validation_generator = load_dataset(validation_data, batch_size, corruption_func, crop_size)

    model.compile(loss='mean_squared_error', optimizer=Adam(beta_2=0.9))

    model.fit_generator(train_generator, steps_per_epoch=steps_per_epoch, epochs=num_epochs,
                        validation_data=validation_generator, validation_steps=num_valid_samples)


def restore_image(corrupted_image, base_model):
    height, width = corrupted_image.shape
    a = Input(shape=(height, width, CHANNELS_FOR_GRAY_IMAGE))
    b = base_model(a)
    new_model = Model(inputs=a, outputs=b)

    new_corrupted_image = corrupted_image - SUBTRACT_FROM_EACH_PIXEL
    new_corrupted_image = new_corrupted_image.reshape(height, width, CHANNELS_FOR_GRAY_IMAGE)

    # keras always wants batch of images and not just one
    corrupted_image_batch = np.array([new_corrupted_image])

    restored_image = new_model.predict(corrupted_image_batch)[0]

    restored_image_height, restored_image_width, _ = restored_image.shape
    restored_image = restored_image.reshape(restored_image_height, restored_image_width)

    restored_image = restored_image.astype(np.float64)
    restored_image += SUBTRACT_FROM_EACH_PIXEL
    restored_image = np.clip(restored_image, 0, 1)

    return restored_image


def round_image_to_nearest_fraction_255_and_clip(image):
    max_gray_level = 255
    to_return = image
    to_return *= max_gray_level
    to_return = np.round(to_return)
    to_return = to_return / max_gray_level

    return to_return.clip(0, 1)


def add_gaussian_noise(image, min_sigma, max_sigma):
    sigma = np.random.uniform(min_sigma, max_sigma)
    mean = 0
    add_to_image = np.random.normal(mean, sigma, image.shape)

    to_return = image + add_to_image

    return round_image_to_nearest_fraction_255_and_clip(to_return)


def learn_denoising_model(num_res_blocks=5, quick_mode=False):
    images = sol5_utils.images_for_denoising()
    height, width = 24, 24
    num_channels = 48
    batch_size = 100
    steps_per_epoch = 100
    num_epochs = 5
    num_valid_samples = 1000

    if quick_mode:
        batch_size = 10
        steps_per_epoch = 3
        num_epochs = 2
        num_valid_samples = 30

    min_sigma, max_sigma = 0, 0.2
    corruption_func = lambda image: add_gaussian_noise(image, min_sigma, max_sigma)

    model = build_nn_model(height, width, num_channels, num_res_blocks)
    train_model(model, images, corruption_func, batch_size,
                steps_per_epoch, num_epochs, num_valid_samples)

    return model


def add_motion_blur(image, kernel_size, angle):
    motion_blur_kernel = sol5_utils.motion_blur_kernel(kernel_size, angle)
    return scipy.ndimage.filters.convolve(image, motion_blur_kernel)


def random_motion_blur(image, list_of_kernel_sizes):
    angle = np.random.uniform(0, np.pi)
    index_in_list_of_kernel_sizes = int(np.random.uniform(0, len(list_of_kernel_sizes)))
    kernel_size = list_of_kernel_sizes[index_in_list_of_kernel_sizes]

    blurred_image = add_motion_blur(image, kernel_size, angle)

    return round_image_to_nearest_fraction_255_and_clip(blurred_image)


def learn_deblurring_model(num_res_blocks=5, quick_mode=False):
    images = sol5_utils.images_for_deblurring()
    height, width = 16, 16
    num_channels = 32
    batch_size = 100
    steps_per_epoch = 100
    num_epochs = 10
    num_valid_samples = 1000

    if quick_mode:
        batch_size = 10
        steps_per_epoch = 3
        num_epochs = 2
        num_valid_samples = 30

    list_of_kernel_sizes = [7]
    corruption_func = lambda image: random_motion_blur(image, list_of_kernel_sizes)

    model = build_nn_model(height, width, num_channels, num_res_blocks)
    train_model(model, images, corruption_func, batch_size,
                steps_per_epoch, num_epochs, num_valid_samples)

    return model
