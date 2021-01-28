import numpy
import scipy
from scipy import signal
from scipy.signal import find_peaks
from scipy.io.wavfile import read
import matplotlib
from matplotlib import pyplot as plt

def crossCorr(x,y):
    z = signal.correlate(x, y)
    return z

def loadSoundFile(filename):
    sr, sig = read(filename)
    #left channel only
    sig = sig[:, 0]
    x = numpy.array(sig, dtype=float)
    return x

def main():
    x = loadSoundFile('snare.wav')
    y = loadSoundFile('drum_loop.wav')
    z = crossCorr(x,y)
    plt.plot(z)
    plt.title('Cross-correlated snare and drum loop')
    plt.xlabel('Samples')
    plt.ylabel('Correlation')
    plt.savefig('01-correlation.png')
    findSnarePosition('snare.wav','drum_loop.wav')

def findSnarePosition(snareFilename, drumloopFilename):
    x = loadSoundFile('snare.wav')
    y = loadSoundFile('drum_loop.wav')
    z = crossCorr(x,y)
    peaks = find_peaks(z, height=1.75e11, distance=40000)
    results_file = open("02-snareLocation.txt","w") 
    results_file.write(str(peaks[0]))
    results_file.close()

main()

