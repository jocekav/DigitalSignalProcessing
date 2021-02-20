import numpy as np
import matplotlib
from matplotlib import pyplot as plt
from numpy import hanning
from numpy.core.shape_base import block

def generateSinusoidal(amplitude, sampling_rate_Hz, frequency_Hz, length_secs, phase_radians):
    t = np.arange(0, length_secs + (1/sampling_rate_Hz), 1/sampling_rate_Hz)
    x = amplitude * np.sin((2 * np.pi * frequency_Hz * t) + phase_radians)
    return t, x

def generateSquare(amplitude, sampling_rate_Hz, frequency_Hz, length_secs, phase_radians):
    t,x = generateSinusoidal(amplitude, sampling_rate_Hz, frequency_Hz, length_secs, phase_radians)
    for i in range(2,20):
        if i % 2 != 0:
            t, y = generateSinusoidal(4/(np.pi*i*amplitude), sampling_rate_Hz, i*frequency_Hz, length_secs, phase_radians)
            x += y
    return t, x


def computeSpectrum(x, sample_rate_Hz):
    fft = np.fft.fft(x)
    fft = fft[:int(len(fft)/2)]
    #bin = (1/len(fft)) * sample_rate_Hz
    f = np.linspace(0, sample_rate_Hz, len(fft))
    # print(sample_rate_Hz/len(fft))
    # print(len(fft))
    norm = np.linalg.norm(fft)
    if norm != 0: 
        fft = fft / norm
    XAbs = np.abs(fft)
    XPhase = np.angle(fft)
    XRe = np.real(fft)
    XIm = np.imag(fft)
    return f,XAbs,XPhase,XRe,XIm

def generateBlocks(x, sample_rate_Hz, block_size, hop_size):
    X = np.zeros((int(len(x)/hop_size), block_size))
    count = 0
    for i in range(0, len(x), hop_size):
        #timestamp = i/sample_rate_Hz
        size = len(x[i:i+block_size])
        ind = X[count]
        X[count][0:size] = x[i:i+block_size]
    t = np.arange(0, len(x), hop_size/sample_rate_Hz)
    return t, X

#Write a function (freq_vector, time_vector, magnitude_spectrogram) = mySpecgram(x,  block_size, hop_size, sampling_rate_Hz, window_type) 
# that computes the FFT per block windowed using the window type specified.
#  freq_vector and time_vector are both column vectors containing the frequency of the bins in Hz 
# (block_size/2 x 1) and the time stamps of the blocks in seconds (N x 1) respectively 
# where N is the number of blocks. magnitude_spectrogram is a (block_size/2 x N) matrix 
# where each column is the FFT of a signal block.  
# The parameter window_type is a string which can take the following values: 
# ‘rect’ for a rectangular window and ‘hann’ for a Hann window. 
# The function should also plot the magnitude spectrogram (labeling the axes appropriately 
# Note: You may use the NumPy fft, hanning and Matplotlib specgram methods. 
# You can use the generateBlocks and computeSpectrum methods which you created earlier.

def mySpecgram(x,  block_size, hop_size, sampling_rate_Hz, window_type):
    t, X = generateBlocks(x, sampling_rate_Hz, block_size, hop_size)
    magnitude_spectrogram = np.zeros((len(X), int(block_size/2)))
    for i in range(len(X)):
        f,XAbs,XPhase,XRe,XIm = computeSpectrum(X[i], sampling_rate_Hz)
        if window_type == 'hann':
            XRe = np.hanning(block_size/2) * XRe
        magnitude_spectrogram[i] = np.abs(XRe)
    time_vector = np.transpose(t)
    freq_vector = np.transpose(f)

    plotSpecgram(freq_vector, time_vector, magnitude_spectrogram, window_type)
    
    return freq_vector, time_vector, magnitude_spectrogram

def plotSpecgram(freq_vector, time_vector, magnitude_spectrogram, window_type):
    if len(freq_vector) < 2 or len(time_vector) < 2:
        return

    Z = np.where(magnitude_spectrogram > 0.0000000001, 20. * np.log10(magnitude_spectrogram), -10)
    Z = np.flipud(Z)
    
    pad_xextent = (time_vector[1] - time_vector[0]) / 2
    xmin = np.min(time_vector) - pad_xextent
    xmax = np.max(time_vector) + pad_xextent
    extent = xmin, xmax, freq_vector[0], freq_vector[-1]
    
    im = plt.imshow(Z, None, extent=extent, origin='upper')
    plt.axis('auto')
    plt.xlabel('Time')
    plt.ylabel('Frequency')
    if window_type == 'hann':
        plt.title('Square Spectrogram - Hanning')
        plt.savefig('results/04-hannWin.png')
    else:
        plt.title('Square Spectrogram - Rectangle')
        plt.savefig('results/04-rectWin.png')


def main():
    time_sine,sine = generateSinusoidal(1.0, 44100, 400, 0.5, np.pi/2)
    increment = int(.005 * 44100)
    plt.figure(0)
    plt.plot(time_sine[0:increment], sine[0:increment])
    plt.title('Sine Wave')
    plt.xlabel('Seconds')
    plt.ylabel('Amplitude')
    plt.savefig('results/01-sine.png')

    time_square,square = generateSquare(1.0, 44100, 400, 0.5, 0)
    increment = int(.005 * 44100)
    plt.figure(1)
    plt.plot(time_square[0:increment], square[0:increment])
    plt.title('Square Wave')
    plt.xlabel('Seconds')
    plt.ylabel('Amplitude')
    plt.savefig('results/02-square.png')

    f_sine,XAbs_sine,XPhase_sine,XRe_sine,XIm_sine = computeSpectrum(sine,44100)
    plt.figure(2)
    plt.subplot(3, 1, 1)
    plt.plot(f_sine, XPhase_sine)
    plt.title('Phase - Sine')
    plt.xlabel('Frequency')
    plt.xlim(right=np.max(f_sine))
    plt.ylabel('Phase')
    plt.subplot(3, 1, 2)
    plt.plot(f_sine, XAbs_sine)
    plt.plot(['Magnitude'])
    plt.title('Real Magnitude Spectrum - Sine')
    plt.xlabel('Frequency')
    plt.xlim(right=np.max(f_sine))
    plt.ylabel('Amplitude')
    plt.subplot(3, 1, 3)
    plt.plot(f_sine, XIm_sine)
    plt.plot(['Magnitude'])
    plt.title('Imaginary Magnitude Spectrum - Sine')
    plt.xlabel('Frequency')
    plt.xlim(right=np.max(f_sine))
    plt.ylabel('Amplitude')
    plt.tight_layout(pad=3.0)
    plt.savefig('results/03-sine_spec.png')
    

    f_square,XAbs_square,XPhase_square,XRe_square,XIm_square = computeSpectrum(square,44100)
    plt.figure(3)
    plt.subplot(3, 1, 1)
    plt.plot(f_square, XPhase_square)
    plt.title('Phase - Square')
    plt.xlabel('Frequency')
    plt.xlim(right=np.max(f_square))
    plt.ylabel('Phase')
    plt.subplot(3, 1, 2)
    plt.plot(f_square, XAbs_square)
    plt.plot(['Magnitude'])
    plt.title('Real Magnitude Spectrum - Square')
    plt.xlabel('Frequency')
    plt.xlim(right=np.max(f_square))
    plt.ylabel('Amplitude')
    plt.subplot(3, 1, 3)
    plt.plot(f_square, XIm_square)
    plt.plot(['Magnitude'])
    plt.title('Imaginary Magnitude Spectrum - Square')
    plt.xlabel('Frequency')
    plt.xlim(right=np.max(f_square))
    plt.ylabel('Amplitude')
    plt.tight_layout(pad=3.0)
    plt.savefig('results/03-square_spec.png')

    plt.figure(4)
    #freq_vector, time_vector, magnitude_spectrogram = mySpecgram(square,  2048, 1024, 44100, "rect")
    plt.figure(5)
    #freq_vector, time_vector, magnitude_spectrogram = mySpecgram(square,  2048, 1024, 44100, "hann")
main()
