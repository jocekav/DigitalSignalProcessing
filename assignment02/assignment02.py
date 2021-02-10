import numpy as np
import scipy
from scipy import signal
import matplotlib
from matplotlib import pyplot as plt
from scipy.io.wavfile import read

def myTimeConv(x,h):
    longer = [x, h][np.argmax((len(x), len(h)))]
    shorter = [h, x][np.argmin((len(h), len(x)))]
    shorter = np.flip(shorter)
    totSamples = len(longer)+len(shorter)-1
    y = np.zeros(totSamples, longer.dtype)
    count = 0
    center = totSamples - (2 * len(shorter))
    for i in range(len(shorter)):
        # y[i] = np.dot(longer[i:len(shorter)+i], shorter[::-1])
        y[count] = np.dot(longer[:i+1], shorter[-(i+1):])
        rev = (len(shorter) - i) - 1
        y[count + center + len(shorter)] = np.dot(longer[-(rev+1):], shorter[:rev+1])
        count += 1
    for i in range(1, (center+1), 1):
        y[count] = np.dot(longer[i:(i + len(shorter))], shorter[:])
        count += 1
    # if len(shorter) == len(longer):
    #     for i in reversed(range(len(shorter)-1)):
    #     #puts numbers in backwards
    #         y[count] = np.dot(longer[-(i+1):], shorter[:i+1])
    #         count += 1
    # else:
    #     for i in reversed(range(len(shorter))):
    #         #puts numbers in backwards
    #         y[count] = np.dot(longer[-(i+1):], shorter[:i+1])
    #         count += 1
    return y


def loadSoundFile(filename):
    sr, sig = read(filename)
    #left channel only
    # sig = sig[:, 0]
    x = np.array(sig, dtype=float)
    return x

#####
# if x is len 200 and h is len 100 then y will be len 299
# len(y) = len(x) + len(h) - 1

# dc signal
x = np.ones(200)
#symmetric triangular signal
h =  np.concatenate((np.linspace(0, 1, 26), np.linspace(1, 0, 26)[1:]), axis=None)

# x = np.linspace(1,55,55)
# h = np.linspace(1,10,10)
x = loadSoundFile('piano.wav')
h = loadSoundFile('impulse-response.wav')
y = myTimeConv(x,h)
plt.plot(y)
# # plt.title('Cross-correlated snare and drum loop')
# # plt.xlabel('Samples')
# # plt.ylabel('Correlation')
plt.savefig('02-myConv.png')
z = signal.convolve(x,h)
plt.plot(z)
# plt.title('Cross-correlated snare and drum loop')
# plt.xlabel('Samples')
# plt.ylabel('Correlation')
plt.savefig('02-conv.png')
print(y)
print(z)
