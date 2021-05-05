
import mido
import string
import numpy as np
import scipy
from scipy import interpolate
from scipy import signal
from IPython.display import Audio
from scipy.io.wavfile import read
from scipy.io.wavfile import write
import random

SAMPLE_RATE = 48000
t = np.arange(0,128/SAMPLE_RATE,1/SAMPLE_RATE)
freq = 375
SINE_WAVETABLE = np.sin(2 * np.pi * freq * t)
SAW_WAVETABLE = scipy.signal.sawtooth(2 * np.pi * freq * t)
SQUARE_WAVETABLE = scipy.signal.square(2 * np.pi * freq * t)
TRI_WAVETABLE = scipy.signal.sawtooth(2 * np.pi * freq * t, width=0.5)

def adsr(x,a=.25,d=.25,s=.5,r=.25,fs=48000):
    total_len = len(x)
    a_len = int(.25 * len(x))
    d_len = int(.25 * len(x))
    r_len = int(.25 * len(x))
    s_len = int(len(x) - a_len - d_len - r_len)

    xa= np.arange(0, a_len)                                                     #sets up size of attack portion
    ya= np.linspace(0,np.max(x),xa.size)                                       #creates attack envelope

    xd= np.arange(a_len, a_len+d_len)                                                 #sets up size of decay portion
    yd= np.linspace(np.max(x),s,xd.size)                                        #creates attack envelope

    xs= np.arange(a_len+d_len, a_len+d_len+s_len)                               #sets up size of sustain portion
    ys= np.linspace(s,s,xs.size)                                            #creates sustain envelope

    xr= np.arange(a_len+d_len+s_len, a_len+d_len+s_len+r_len)               #sets up size of release portion
    yr= np.linspace(s,0,xr.size)

    env=np.concatenate((ya,yd,ys,yr))                                          #creates full adsr envelope array
    adsrnote=x*env[0:x.size]               
                                                                                #applies adsr envelope to input array
    return adsrnote

def genSine(frequency, duration, amplitude = 1, sampleRate = 48000, phase = 0):
    
    #creates a sine wave
    
    import numpy as np
    
    time = np.arange(0, duration, 1/sampleRate)
    return amplitude * np.sin((2*np.pi * frequency * time) + phase)

def genSaw(frequency, duration, numSine = 10, amplitude = 1, sampleRate = 44800, phase = 0):
    
    #creates a saw wave out of a sum of sine waves
    
    import numpy as np
    
    time = np.arange(0, duration, 1/sampleRate)
    initSine = np.sin((2*np.pi * frequency * time) + phase)
    for i in range(2, numSine + 1):
        addSine = (1/i) * np.sin((2*np.pi * (frequency * i) * time) + phase)
        initSine = initSine + addSine
    return amplitude * initSine

def genSquare(frequency, duration, numSine = 10, amplitude = 1, sampleRate = 44800, phase = 0):
    
    #creates a square wave out of a sum of sine waves
    
    import numpy as np
    
    time = np.arange(0, duration, 1/sampleRate)
    initSine = 0
    for i in range(1, numSine + 1, 2):
        addSine = (1/i) * np.sin((2*np.pi * (frequency * i) * time) + phase)
        initSine = initSine + addSine
    return amplitude * initSine

def genTriangle(frequency, duration, numSine = 10, amplitude = 1, sampleRate = 44800, phase = 0):
    
    #creates a triangle wave out of a sum of sine waves
    
    import numpy as np
    
    time = np.arange(0, duration, 1/sampleRate)
    amps = [(1/j**2) for j in range(1,numSine+1)]
    count = 1
    initSine = 0
    for i in range(1, numSine + 1):
        if (i % 2 == 0):
            addSine = 0
        else:
            addSine = (-(-1**count)/(i**2) * np.sin((2*np.pi * (frequency * i) * time) + phase))
        initSine = initSine + addSine
        count = count + 1
    return amplitude * initSine

def additive(type, freq, duration, num_harmonics, amplitude=1, fs=48000, phase_shift=0):
    summed_wave = np.array([])
    if type == 'sine':
        summed_wave = genSine(freq, duration, phase=(phase_shift))
        for i in range(2, num_harmonics+1):
            add = genSine((freq * i), duration, phase=(phase_shift*i))
            summed_wave = summed_wave + add
    elif type == 'square':
        summed_wave = genSquare(freq, duration, phase=(phase_shift))
        for i in range(2, num_harmonics+1):
            add = genSquare((freq * i), duration, phase=(phase_shift*i))
            summed_wave = summed_wave + add
    elif type == 'triangle':
        summed_wave = genTriangle(freq, duration, phase=(phase_shift))
        for i in range(2, num_harmonics+1):
            add = genTriangle((freq * i), duration, phase=(phase_shift*i))
            summed_wave = summed_wave + add
    elif type == 'saw':
        summed_wave = genSaw(freq, duration, phase=(phase_shift))
        for i in range(2, num_harmonics+1):
            add = genSaw((freq * i), duration, phase=(phase_shift*i))
            summed_wave = summed_wave + add
    summed_wave *= amplitude
    summed_wave = summed_wave / np.max(summed_wave)
    return summed_wave
    

def wavetable(frequency, dur, amp, type='sine', fs=48000):
    # choose the wave type
    try:
        if (type == 'sine'):
            wave = SINE_WAVETABLE
        elif (type == 'square'):
            wave = SQUARE_WAVETABLE
        elif (type == 'saw'):
            wave = SAW_WAVETABLE
        elif (type == 'triangle'):
            wave = TRI_WAVETABLE
    except:
        print("Please input a valid waveform")

    interp = scipy.interpolate.CubicSpline(np.arange(0, len(wave)), wave,bc_type='natural')


    wave = wave / max(wave)
    # frequency to step size
    step = (round(frequency) * 128) / fs
    # time to desired sample length (array length)
    length = dur * fs
    ind_arr = np.arange(0, step * length, step)

    out = np.array([])
    #read table
    for i in ind_arr:
        i = i % 128
        if i != int(i):

            out = np.append(out, interp(i))
        elif i == int(i):
            out = np.append(out, wave[int(i)])
    out = out * amp
    return out

def ring_modulation(x, rate=0.5, blend=0.5, block_size=512):
    remainder = len(x) % block_size
    pad = np.zeros(remainder)
    print(len(pad))
    x = np.concatenate((x, pad))
    total_blocks = len(x) / block_size
    for j in range(int(total_blocks)):
        t = 0
        for i in range(block_size):
            ring_factor = np.sin(t)
            t += (rate * 0.2)
            x[i + (block_size * j)] = ((1-blend) * x[i + (block_size * j)]) + (blend * ring_factor * x[i + (block_size * j)])
    x = x[0:(len(x)-remainder)]
    return x

def lfo(x, freq, blend, amplitude=1, fs=48000):
    t = np.arange(0,len(x)/fs,1/fs)
    lfo = x * amplitude * np.cos(2*np.pi*freq*t)
    out = ((1 - blend) * x) + (blend * out)
    return out


def reverb(x, impulse_in, blend):
    print(impulse_in)
    fs, impulse = read(impulse_in)
    impulse = np.transpose(impulse)[0]

    impulse = np.concatenate((impulse, np.zeros(len(x)-len(impulse))))
    impulse = impulse / np.max(impulse)
    # x = np.real(impulse)

    fft_sig = scipy.fft.fft(x)
    fft_impulse = scipy.fft.fft(impulse)
    conv = fft_impulse * fft_sig

    out = np.real(scipy.fft.ifft(conv))
    out = out / np.max(out)
    out = ((1 - blend) * x) + (blend * out)
    return out

def lowpass(x, cutoff, blend, filter_block='default', fs=48000):
    if filter_block == 'default':
        filter_block = int (fs / cutoff) 
        if filter_block % 2 == 0:
            filter_block += 1

    cutoff = cutoff / fs  # Cutoff frequency as a fraction of the sampling rate.

    coeffs = np.sinc(2 * cutoff * (np.arange(filter_block) - (filter_block - 1) / 2))

    coeffs *= np.hamming(filter_block)

    coeffs /= np.sum(coeffs)
    out = np.convolve(x, coeffs)
    out = ((1 - blend) * x) + (blend * out)
    return out


def highpass(x, cutoff, blend, filter_block='default', fs=48000):
    if filter_block == 'default':
        filter_block = int (fs / cutoff) 
        if filter_block % 2 == 0:
            filter_block += 1

    cutoff = cutoff / fs  # Cutoff frequency as a fraction of the sampling rate.

    coeffs = np.sinc(2 * cutoff * (np.arange(filter_block) - (filter_block - 1) / 2))

    coeffs *= np.hamming(filter_block)

    coeffs /= np.sum(coeffs)

    coeffs = -coeffs
    coeffs[(filter_block - 1) // 2] += 1

    out = np.convolve(x, coeffs)
    out = ((1 - blend) * x) + (blend * out)
    return out

def flanger(x, delay_time, rate, feedback_percent, blend, fs=48000):
    import math
    ind = np.arange(0, len(x))
    sine_osc = np.sin(2 * np.pi * ind * (rate/fs))
    delay_samples = int(delay_time*fs)
    x_zero = np.zeros(len(x))
    x_zero[:delay_samples] = x[:delay_samples]
    for i in range(delay_samples, len(x)):
        abs_sin = abs(sine_osc[i])
        cur_delay = math.ceil(abs_sin*delay_samples)
        x_zero[i] = (feedback_percent * x[i]) + (feedback_percent * x[i-cur_delay])
    out = ((1 - blend) * x) + (blend * x_zero)
    return out


def downSample(x, new_rate):
    if new_rate == 48000:
        return x
    interp = scipy.interpolate.CubicSpline(np.arange(0, len(x)), x,bc_type='natural')
    curr_rate = 48000
    sample_steps = curr_rate / new_rate
    ind_arr = np.arange(0, len(x), sample_steps)
    out = np.zeros(len(ind_arr))
    #read table
    for ind, i in enumerate(ind_arr):
        if i != int(i):
            out[ind] = interp(i)
        elif i == int(i):
            out[ind] = x[int(i)]
    return out

def quantize_dither(x, bit_depth):
    sample_max = 2**(bit_depth-1)-1
    y_quantized = np.floor(x*sample_max)
    y_quantized = y_quantized[:int(len(y_quantized)/2)]
    # for i in range(len(y_quantized)):
    #     noise = random.triangular(-1, 1)
    #     y_quantized[i] = y_quantized[i] + noise
    return y_quantized / np.max(y_quantized)

