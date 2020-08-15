import numpy as np
from skimage.color import rgb2gray
from imageio import imread
from scipy.io import wavfile
from scipy import signal
from scipy.ndimage.interpolation import map_coordinates

GRAY_CODE = 1
RGB_CODE = 2
MAX_GRAY_LEVEL = 255


def stft(y, win_length=640, hop_length=160):
    """
    as we were told in the forum by koren, we should simply include
    the ex2 helper functions in our code.
    https://moodle2.cs.huji.ac.il/nu19/mod/forum/discuss.php?d=9334
    as such I also needed to include the ex2 helper imports
    :param y:
    :param win_length:
    :param hop_length:
    :return:
    """
    fft_window = signal.windows.hann(win_length, False)

    # Window the time series.
    n_frames = 1 + (len(y) - win_length) // hop_length
    frames = [y[s:s + win_length] for s in np.arange(n_frames) * hop_length]

    stft_matrix = np.fft.fft(fft_window * frames, axis=1)
    return stft_matrix.T


def istft(stft_matrix, win_length=640, hop_length=160):
    """
    as we were told in the forum by koren, we should simply include
    the ex2 helper functions in our code.
    https://moodle2.cs.huji.ac.il/nu19/mod/forum/discuss.php?d=9334
    as such I also needed to include the ex2 helper imports
    :param stft_matrix:
    :param win_length:
    :param hop_length:
    :return:
    """
    n_frames = stft_matrix.shape[1]
    y_rec = np.zeros(win_length + hop_length * (n_frames - 1), dtype=np.float)
    ifft_window_sum = np.zeros_like(y_rec)

    ifft_window = signal.windows.hann(win_length, False)[:, np.newaxis]
    win_sq = ifft_window.squeeze() ** 2

    # invert the block and apply the window function
    ytmp = ifft_window * np.fft.ifft(stft_matrix, axis=0).real

    for frame in range(n_frames):
        frame_start = frame * hop_length
        frame_end = frame_start + win_length
        y_rec[frame_start: frame_end] += ytmp[:, frame]
        ifft_window_sum[frame_start: frame_end] += win_sq

    # Normalize by sum of squared window
    y_rec[ifft_window_sum > 0] /= ifft_window_sum[ifft_window_sum > 0]
    return y_rec


def phase_vocoder(spec, ratio):
    """
    as we were told in the forum by koren, we should simply include
    the ex2 helper functions in our code.
    https://moodle2.cs.huji.ac.il/nu19/mod/forum/discuss.php?d=9334
    as such I also needed to include the ex2 helper imports
    :param spec:
    :param ratio:
    :return:
    """
    num_timesteps = int(spec.shape[1] / ratio)
    time_steps = np.arange(num_timesteps) * ratio
    time_steps = time_steps[time_steps < spec.shape[1]]

    # interpolate magnitude
    yy = np.meshgrid(np.arange(time_steps.size), np.arange(spec.shape[0]))[1]
    xx = np.zeros_like(yy)
    coordiantes = [yy, time_steps + xx]
    warped_spec = map_coordinates(np.abs(spec), coordiantes, mode='reflect',
                                  order=1).astype(np.complex)

    # phase vocoder
    # Phase accumulator; initialize to the first sample
    spec_angle = np.pad(np.angle(spec), [(0, 0), (0, 1)], mode='constant')
    phase_acc = spec_angle[:, 0]

    for (t, step) in enumerate(np.floor(time_steps).astype(np.int)):
        # Store to output array
        warped_spec[:, t] *= np.exp(1j * phase_acc)

        # Compute phase advance
        dphase = (spec_angle[:, step + 1] - spec_angle[:, step])

        # Wrap to -pi:pi range
        dphase = np.mod(dphase - np.pi, 2 * np.pi) - np.pi

        # Accumulate phase
        phase_acc += dphase

    return warped_spec


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


def DFT(signal):
    """
    :param signal: array of dtype float64 with shape (N,1)
    :return: fourier_signal - an array of dtype complex128 with
    the same shape which would hold the fourier representation
    of the given signal
    """
    N = signal.shape[0]

    # create a 2d matrix where mat[u][x] = e^-2piiux/N
    whole_from_0_to_n_minus_1 = np.arange(0, N)
    mat = whole_from_0_to_n_minus_1.reshape((N, 1)) * whole_from_0_to_n_minus_1
    e_to_power_2_pi_i = np.e ** (-2 * np.pi * 1j / N)
    mat = e_to_power_2_pi_i ** mat

    # now F(u) would be equal to signal.dot(row u of mat)
    # so overall the fourier_signal would be the matrix multiplication
    # of signal and mat
    fourier_signal = mat.dot(signal)

    return fourier_signal


def IDFT(fourier_signal):
    """
    :param fourier_signal: an array of dtype complex128 with
    :return: an array of dtype float64 with shape (N,1) which would be the
    inverse of the fourier transform of the given signal
    """
    N = fourier_signal.shape[0]

    # create a 2d matrix where mat[u][x] = e^2piiux/N
    whole_from_0_to_n_minus_1 = np.arange(0, N)
    mat = whole_from_0_to_n_minus_1.reshape((N, 1)) * whole_from_0_to_n_minus_1
    e_to_power_2_pi_i = np.e ** (2 * np.pi * 1j / N)
    mat = e_to_power_2_pi_i ** mat

    # now F(u) would be equal to signal.dot(row u of mat)
    # so overall the fourier_signal would be the matrix multiplication
    # of signal and mat
    signal = mat.dot(fourier_signal) / N

    return signal


def DFT2(image):
    """
    :param image: a 2d array of dtype float64 with shape (N,M,1)
    :return: fourier_signal - a 2d array of dtype complex128 with
    the same shape which would hold the fourier representation
     of the given image
    """
    dft_per_rows = DFT(image)
    dft_per_cols = DFT(dft_per_rows.T)
    return dft_per_cols.T


def IDFT2(fourier_image):
    """
    :param fourier_image: a 2d array of dtype complex128
    :return: inverse of the fourier transform of the given image
    """
    idft_per_rows = IDFT(fourier_image)
    idft_per_cols = IDFT(idft_per_rows.T)
    return idft_per_cols.T


def change_rate(filename, ratio):
    """
    :param filename: a path to the wavfile
    :param ratio: a positive float64 representing the duration change

    changes the rate of the given audio file and saves the result into
    a new file called change_rate.wav
    """
    rate_of_file, data = wavfile.read(filename)

    wavfile.write('change_rate.wav', int(rate_of_file * ratio), data)


def resize(data, ratio):
    """
    :param data: a 1d ndarray of type float64 representing the sample points
    :param ratio: a positive float64 representing the duration change
    :return: a 1d ndarray of type float64 representing the new sample points
    """
    number_of_samples = len(data)
    fourier_data = DFT(data)

    # shift the zero frequency component to the center of the spectrum
    fourier_data = np.fft.fftshift(fourier_data)

    # now check if ratio is bigger or smaller than 1 and act accordingly
    if ratio > 1:
        number_of_items_to_clip = number_of_samples - \
                                  round(number_of_samples / ratio)
        number_of_items_to_clip_from_left = number_of_items_to_clip // 2
        number_of_items_to_clip_from_right = number_of_items_to_clip - \
                                             number_of_items_to_clip_from_left
        fourier_data = fourier_data[number_of_items_to_clip_from_left:
                                    number_of_samples -
                                    number_of_items_to_clip_from_right]
    if ratio < 1:
        number_of_items_to_add = round(number_of_samples * (1 / ratio - 1))
        number_of_items_to_add_to_left = number_of_items_to_add // 2
        number_of_items_to_add_to_right = number_of_items_to_add - \
                                          number_of_items_to_add_to_left
        fourier_data = np.pad(fourier_data,
                              (number_of_items_to_add_to_left,
                               number_of_items_to_add_to_right),
                              mode='constant')

    # shift the zeo frequency component back to the start of the spectrum
    fourier_data = np.fft.ifftshift(fourier_data)

    new_data_points = IDFT(fourier_data)
    if not np.iscomplexobj(data):
        new_data_points = new_data_points.real

    return new_data_points


def change_samples(filename, ratio):
    """
    :param filename: a path to the wavfile
    :param ratio: a positive float64 representing the duration change

    this function creates a new wav file called change_samples.wav which would
    have a different sample number dictated by the ratio argument

    :return: a 1d ndarray of type float64 representing the new sample points
    """
    rate_of_file, data = wavfile.read(filename)
    data = np.array(data).astype(np.float64)
    new_sample_points = resize(data, ratio)

    # before writing we need to normalize the values of the sample points
    max_value = np.max(np.abs(new_sample_points))
    new_sample_points = new_sample_points / max_value

    wavfile.write('change_samples.wav', rate_of_file, new_sample_points)

    return new_sample_points


def resize_spectrogram(data, ratio):
    """
    :param data: a 1d ndarray of type float64 representing the sample points
    :param ratio: a positive float64 representing the rate of change
    :return: the new sample points according to ratio
    """
    spectrogram = stft(data)

    new_spectrogram = []
    for row in spectrogram:
        new_spectrogram.append(resize(row, ratio))

    new_spectrogram = np.array(new_spectrogram)

    new_sample_points = istft(new_spectrogram)
    return new_sample_points


def resize_vocoder(data, ratio):
    """
    :param data: a 1d ndarray of type float64 representing the sample points
    :param ratio: a positive float64 representing the rate of change
    :return: the new sample points according to ratio
    """
    spectrogram = stft(data)

    spectrogram = phase_vocoder(spectrogram, ratio)
    new_sample_points = istft(spectrogram)

    return new_sample_points


def conv_der(im):
    """
    :param im: a grey scale image of type float64
    :return: a grey scale image of type float64 which is the
    given image derivative
    """
    derivative_formula = [[0, 0, 0], [0.5, 0, -0.5], [0, 0, 0]]
    rows_der = np.array(derivative_formula).transpose()
    cols_der = np.array(derivative_formula)

    rows_derivative = signal.convolve2d(im, rows_der, mode='same')
    cols_derivative = signal.convolve2d(im, cols_der, mode='same')
    derivative = rows_derivative ** 2 + cols_derivative ** 2
    magnitude_derivative = np.sqrt(derivative)

    return magnitude_derivative


def fourier_der(im):
    """
    :param im: a grey scale image of type float64
    :return: a grey scale image of type float64 which is the
    given image derivative
    """

    def get_multiplicity_array(num):
        """
        :param num:
        :return:
        if num is even it returns [-n/2...0...n/2 - 1]
        if num is odd it returns [-(n-1)/2...0...(n-1)/2]
        """
        if num % 2 == 1:
            multiplicity_array = np.arange((num + 1) // 2)
        else:
            multiplicity_array = np.arange(num // 2)

        flipped_multiplicity_array = np.flip(multiplicity_array[1:]) * -1
        multiplicity_array = np.concatenate((flipped_multiplicity_array,
                                             multiplicity_array))

        if num % 2 == 0:
            multiplicity_array = np.concatenate(([-num // 2],
                                                 multiplicity_array))

        return multiplicity_array

    number_of_rows, number_of_cols = im.shape

    dx = get_multiplicity_array(number_of_cols)
    dx = np.tile(dx, (number_of_rows, 1))

    dy = get_multiplicity_array(number_of_rows)
    dy = np.tile(np.flip(dy), (number_of_cols, 1)).T

    im_dft = DFT2(im)
    im_dft = np.fft.fftshift(im_dft)

    rows_derivative = im_dft * dx
    rows_derivative *= 2 * np.pi * 1j / number_of_cols
    rows_derivative = np.fft.ifftshift(rows_derivative)
    rows_derivative = IDFT2(rows_derivative)

    cols_derivative = im_dft * dy
    cols_derivative *= 2 * np.pi * 1j / number_of_rows
    cols_derivative = np.fft.ifftshift(cols_derivative)
    cols_derivative = IDFT2(cols_derivative)

    derivative = abs(rows_derivative) ** 2 + \
                 abs(cols_derivative) ** 2
    magnitude_derivative = np.sqrt(derivative)

    return magnitude_derivative
