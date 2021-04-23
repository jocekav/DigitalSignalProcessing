import mido
import string
import numpy as np
import scipy
from scipy import interpolate
#mid = mido.MidiFile('.mid', clip=True)
mid = mido.MidiFile('Saw.mid', clip=True)
mid.tracks

def convert_clocks_per_click(clocks_per_click, user_tempo):
    sec_per_click = .6 / (user_tempo * clocks_per_click)
    return sec_per_click

def convert_velocity(midi_vel):
    velocity = midi_vel / 127.0
    return velocity

def convert_frequency(midi_val):
    reference = 440
    frequency = (reference / 32) * (2 ** ((midi_val - 9) / 12))
    return frequency

def parse_MIDI(midi_file, user_tempo):
    # ticks_per_quarter = <PPQ from the header>
    # µs_per_quarter = <Tempo in latest Set Tempo event>
    # µs_per_tick = µs_per_quarter / ticks_per_quarter
    # seconds_per_tick = µs_per_tick / 1.000.000
    # seconds = ticks * seconds_per_tick
    clocks_per_click = 0
    midi_info = []
    note_value = 0
    note_velocity = 0
    note_dur = 0
    sec_per_click = 0


    mid = mido.MidiFile(midi_file, clip=True)
    for i in range(0, len(mid.tracks)):
        for m in mid.tracks[i][:]:
            # print(m)
            m = str(m)
            if 'clocks_per_click' in m and clocks_per_click == 0:
                # midi.append(m)
                temp = m.partition("clocks_per_click=")[2]
                clocks_per_click = temp.partition(" ")[0]
                sec_per_click = convert_clocks_per_click(int(clocks_per_click), user_tempo)
            if 'note_on' in m:
                temp = m.partition("note=")[2]
                note_value = temp.partition(" ")[0]
                #convert to frequency
                note_value = convert_frequency(int(note_value))
                temp = m.partition("velocity=")[2]
                note_velocity = temp.partition(" ")[0]
                #convert to 0-1 amplitude
                note_velocity = convert_velocity(int(note_velocity))
            if 'note_off' in m:
                note_dur = m.partition("time=")[2]
                #convert to seconds
                note_dur = sec_per_click * int(note_dur)
                if note_dur != 0:
                    midi_info.append((note_value, note_velocity, note_dur))
                # print(midi_info)
    return midi_info



def adsr(x,a=.25,d=.25,s=.25,r=.25,fs=48000):
    total_len = len(x)
    a_len = int(.25 * len(x))
    d_len = int(.25 * len(x))
    r_len = int(.25 * len(x))
    s_len = int(len(x) - a_len - d_len - r_len)

    xa= np.arange(0, a_len)                                                     #sets up size of attack portion
    ya= np.linspace(0,np.max(x),xa.size)                                       #creates attack envelope

    xd= np.arange(a_len, a_len+d_len)                                                 #sets up size of decay portion
    yd= np.linspace(np.max(x),.5,xd.size)                                        #creates attack envelope

    xs= np.arange(a_len+d_len, a_len+d_len+s_len)                               #sets up size of sustain portion
    ys= np.linspace(.5,.5,xs.size)                                            #creates sustain envelope

    xr= np.arange(a_len+d_len+s_len, a_len+d_len+s_len+r_len)               #sets up size of release portion
    yr= np.linspace(.5,0,xr.size)

    env=np.concatenate((ya,yd,ys,yr))                                          #creates full adsr envelope array
    adsrnote=x*env[0:x.size]               
                                               #applies adsr envelope to input array
    return adsrnote

def genSine(frequency, duration, amplitude = 1, sampleRate = 48000, phase = 0):
    
    #creates a sine wave
    
    import numpy as np
    
    time = np.arange(0, duration, 1/sampleRate)
    return amplitude * np.sin((2*np.pi * frequency * time) + phase)


def wavetable(frequency, dur, amp, fs=48000):
    from matplotlib import pyplot as plt
    # choose the wave type
    t = np.arange(0,128/fs,1/fs)
    wave = np.sin(2 * np.pi * 375 * np.arange(0,128/fs,1/fs))

    interp = scipy.interpolate.CubicSpline(np.arange(0, len(wave)), wave,bc_type='natural')

    # plt.plot(t, wave)
    wave = wave / max(wave)
    # frequency to step size
    step = (round(frequency) * 128) / fs
    # time to desired sample length (array length)
    length = dur * fs
    ind_arr = np.arange(0, step * length, step)
    # ind_arr = np.linspace(0, step * length, length)
    out = np.array([])
    #read table
    for i in ind_arr:
        i = i % 128
        if i != int(i):
            # floored = int(i)
            # next = floored + 1
            # decimal = i - floored
            # out = np.append(out, wave[floored] + decimal * (wave[next] - wave[floored]))
            out = np.append(out, interp(i))
        elif i == int(i):
            out = np.append(out, wave[int(i)])
    out = out * amp
    return out


note_list = parse_MIDI('Saw.mid', 8)
play_list = np.array([])
for i in note_list:
    note_sine = genSine(i[0], i[2], i[1])
    #note_sine = wavetable(i[0], i[2], i[1])
    note_sine = adsr(note_sine)
    play_list = np.concatenate((play_list, note_sine))
    # play_list = lfo(play_list, 2)
    # play_list = lowpass(play_list, cutoff=440)
    # play_list = flanger(play_list, .004, 0.11, 0.57)
    # play_list = wahwah(play_list)
print(play_list)

from IPython.display import Audio
import scipy
from scipy.io.wavfile import write
write("test.wav", 48000, play_list)