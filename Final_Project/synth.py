import synth_helpers
import mido
import string
import numpy as np
import scipy
from scipy import interpolate
from scipy import signal
from IPython.display import Audio
import scipy
from scipy.io.wavfile import write


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

def parse_MIDI(midi_file, user_tempo=120):
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

# def init():
#     sample_rate = 48000
#     t = np.arange(0,128/sample_rate,1/sample_rate)
#     freq = 375
#     sine_wavetable = np.sin(2 * np.pi * freq * t)
#     saw_wavetable = scipy.signal.sawtooth(2 * np.pi * freq * t)
#     square_wavetable = scipy.signal.square(2 * np.pi * freq * t)
#     tri_wavetable = scipy.signal.sawtooth(2 * np.pi * freq * t, width=0.5)



# def main():
#     # init()
#     note_list = parse_MIDI('Saw.mid', 8)
#     play_list = np.array([])
#     for i in note_list:
#         note_sine = synth_helpers.genSine(i[0], i[2], i[1])
#         #note_sine = wavetable(i[0], i[2], i[1])
#         note_sine = synth_helpers.adsr(note_sine)
#         play_list = np.concatenate((play_list, note_sine))
#         # play_list = lfo(play_list, 2)
#         # play_list = lowpass(play_list, cutoff=440)
#         # play_list = flanger(play_list, .004, 0.11, 0.57)
#         # play_list = wahwah(play_list)
#     print(play_list)

def main():
    midi_input = input("Please input MIDI file path: ")
    tempo_input = input("Please input tempo in BPM: ")
    midi_info = parse_MIDI(midi_input, tempo_input)
    gen_type = input("Additive Synthesis or Wavetable Sythesis. Type 'add' for Additive and 'wav' for Wavetable: ")
    if (gen_type == 'add'):
        wave_type = input("Choose wave type. Type 'sine', 'saw', 'square', or 'triangle'")
        num_harmonics = input("Type the number of harmonics:")
        try:
            if wave_type == 'sine':
                play_list = np.array([])
                for i in midi_info:
                    note_sine = synth_helpers.additive('sine', i[0], i[2], num_harmonics, i[1])
                    play_list = np.concatenate((play_list, note_sine))
            elif wave_type == 'saw':
                play_list = np.array([])
                for i in midi_info:
                    note_sine = synth_helpers.additive('saw', i[0], i[2], num_harmonics, i[1])
                    play_list = np.concatenate((play_list, note_sine))
            elif wave_type == 'square':
                play_list = np.array([])
                for i in midi_info:
                    note_sine = synth_helpers.additive('square', i[0], i[2], num_harmonics, i[1])
                    play_list = np.concatenate((play_list, note_sine))
            elif wave_type == 'triangle':
                play_list = np.array([])
                for i in midi_info:
                    note_sine = synth_helpers.additive('triangle', i[0], i[2], num_harmonics, i[1])
                    play_list = np.concatenate((play_list, note_sine))
        except:
            wave_type = input("Choose wave type. Type 'sine', 'saw', 'square', or 'triangle'")
    else: 
        wave_type = input("Choose wave type. Type 'sine', 'saw', 'square', or 'triangle'")
        try:
            if wave_type == 'sine':
                play_list = np.array([])
                for i in midi_info:
                    note_sine = synth_helpers.wavetable(i[0], i[2], i[1], 'sine')
                    play_list = np.concatenate((play_list, note_sine))
            elif wave_type == 'saw':
                play_list = np.array([])
                for i in midi_info:
                    note_sine = synth_helpers.wavetable(i[0], i[2], i[1], 'saw')
                    play_list = np.concatenate((play_list, note_sine))
            elif wave_type == 'square':
                play_list = np.array([])
                for i in midi_info:
                    note_sine = synth_helpers.wavetable(i[0], i[2], i[1], 'saw')
            elif wave_type == 'triangle':
                play_list = np.array([])
                for i in midi_info:
                    note_sine = synth_helpers.wavetable(i[0], i[2], i[1], 'triangle')
                    play_list = np.concatenate((play_list, note_sine))
        except:
            wave_type = input("Choose wave type. Type 'sine', 'saw', 'square', or 'triangle'")
    user_complete = False
    while not user_complete:
        input("Choose an effect. Type 'adsr', 'saw', 'square', or 'triangle'")

        

main()

# from IPython.display import Audio
# import scipy
# from scipy.io.wavfile import write
# write("test.wav", 48000, play_list)