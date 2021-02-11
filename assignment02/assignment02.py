import numpy as np
import scipy
from scipy import signal
import matplotlib
from matplotlib import pyplot as plt
from scipy.io.wavfile import read
import time
from tqdm import tqdm

# if x is len 200 and h is len 100 then y will be len 299
# len(y) = len(x) + len(h) - 1

def myTimeConv(x,h):
    #find the longer signal
    longer = [x, h][np.argmax((len(x), len(h)))]
    shorter = [h, x][np.argmin((len(h), len(x)))]
    #flip the shorter impulse
    shorter = np.flip(shorter)
    # len(y) = len(x) + len(h) - 1
    totSamples = len(longer)+len(shorter)-1
    y = np.zeros(totSamples, longer.dtype)
    count = 0
    #find center section that can't be indexed from the front or back of the array
    center = totSamples - (2 * len(shorter))

    for i in range(len(shorter)):
        #find the product and sum of the overlapping array sections at the front of the longer array
        y[count] = np.dot(longer[:i+1], shorter[-(i+1):])
        #find the product and sum of the overlapping array sections at the back of the longer array
        rev = (len(shorter) - i) - 1
        y[count + center + len(shorter)] = np.dot(longer[-(rev+1):], shorter[:rev+1])
        count += 1
    for i in range(1, (center+1), 1):
        #find the product and sum of the overlapping array sections in the center section of the longer array
        y[count] = np.dot(longer[i:(i + len(shorter))], shorter[:])
        count += 1
    return y

### I understand that the above approach is more unusual with the use of the dot product.
### I did this for the purpose of effiency, however, below I have provided the more conventional solution with nested loops.
def mySlowerTimeConv(x,h):
    lenX = len(x)
    lenH = len(h)
    x = np.concatenate((x, np.zeros(lenH))) 
    h = np.concatenate((h, np.zeros(lenX))) 
    totSamples = lenX + lenH - 1
    y = np.zeros(totSamples)
    for i in tqdm(range(totSamples)):
        for j in range(lenX):
            if i - j + 1 >= 0:
                y[i] = y[i] + (x[j] * h[i-j])
    return y

def CompareConv(x,h):
    start = time.time()
    myConv = myTimeConv(x,h)
    end = time.time()
    myTime = end - start

    start = time.time()
    theirConv = signal.convolve(x,h)
    end = time.time()
    theirTime = end - start

    m = myConv.mean() - theirConv.mean()
    # np.mean(np.absolute(diff - np.mean(diff)))
    diff = myConv - theirConv
    mabs = np.mean(np.absolute(diff - np.mean(diff)))
    stdev = np.std(myConv-theirConv)
    # you can't return the variable as time because it is a keyword in python
    return m, mabs, stdev, [myTime, theirTime]

def CompareConvIneffecient(x,h):
    start = time.time()
    myConv = mySlowerTimeConv(x,h)
    end = time.time()
    myTime = end - start

    start = time.time()
    theirConv = signal.convolve(x,h)
    end = time.time()
    theirTime = end - start

    m = myConv.mean() - theirConv.mean()
    # np.mean(np.absolute(diff - np.mean(diff)))
    diff = myConv - theirConv
    mabs = np.mean(np.absolute(diff - np.mean(diff)))
    stdev = np.std(myConv-theirConv)
    # you can't return the variable as time because it is a keyword in python
    return m, mabs, stdev, [myTime, theirTime]


def loadSoundFile(filename):
    sr, sig = read(filename)
    #left channel only
    # sig = sig[:, 0]
    x = np.array(sig, dtype=float)
    return x

def main():
    # dc signal
    x = np.ones(200)
    #symmetric triangular signal
    h =  np.concatenate((np.linspace(0, 1, 26), np.linspace(1, 0, 26)[1:]), axis=None)
    y = myTimeConv(x,h)
    plt.plot(y)
    plt.title('My Convolution')
    plt.xlabel('Time')
    plt.ylabel('Response')
    plt.savefig('02-myConv.png')
    
    x = loadSoundFile('audio/piano.wav')
    h = loadSoundFile('audio/impulse-response.wav')
    m, mabs, stdev, time = CompareConv(x,h)
    m1, mabs1, stdev1, time1 = CompareConvIneffecient(x,h)
    results_file = open("02-results.txt","w") 
    results_file.write('Results for my efficient convolution: ')
    results_file.write(str(m) + ', ' + str(mabs) + ', ' + str(stdev) + ', ' + str(time) + '\n')
    results_file.write('Results for my inefficient convolution: ' + str(m1) + ', ' + str(mabs1) + ', ' + str(stdev1) + ', ' + str(time1))
    results_file.close()


# # dc signal
# x = np.ones(200)
# #symmetric triangular signal
# h =  np.concatenate((np.linspace(0, 1, 26), np.linspace(1, 0, 26)[1:]), axis=None)
    
# print(CompareConv(x,h))
main()
