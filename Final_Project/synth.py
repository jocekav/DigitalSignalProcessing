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

def parse_MIDI(midi_file, user_tempo):
    clocks_per_click = 0
    midi_info = []
    note_value = 0
    note_velocity = 0
    note_dur = 0
    sec_per_click = 0
    curr_message = ''
    prev_message = ''


    mid = mido.MidiFile(midi_file, clip=True)
    for i in range(0, len(mid.tracks)):
        for m in mid.tracks[i][:]:
            m = str(m)
            if 'clocks_per_click' in m:
                temp = m.partition("clocks_per_click=")[2]
                clocks_per_click = temp.partition(" ")[0]
            if 'note_on' in m:
                curr_message = 'note_on'
                if curr_message != prev_message:
                    temp = m.partition("note=")[2]
                    note_value = temp.partition(" ")[0]
                    #convert to frequency
                    note_value = convert_frequency(int(note_value))
                    temp = m.partition("velocity=")[2]
                    note_velocity = temp.partition(" ")[0]
                    #convert to 0-1 amplitude
                    note_velocity = convert_velocity(int(note_velocity))
                    # rests
                    note_dur = m.partition("time=")[2]
                    #convert to seconds
                    note_dur = mido.tick2second(int(note_dur), int(clocks_per_click), mido.bpm2tempo(user_tempo))
                    if note_dur > 0:
                        midi_info.append((440, 0, note_dur))


            if 'note_off' in m:
                curr_message = 'note_off'
                if curr_message != prev_message:
                    note_dur = m.partition("time=")[2]
                    note_dur = mido.tick2second(int(note_dur), int(clocks_per_click), mido.bpm2tempo(user_tempo))
                    if note_dur > 0:
                        midi_info.append((note_value, note_velocity, note_dur))

            prev_message = curr_message
    return midi_info


def main():
    midi_input = input("Please input MIDI file path: ")
    tempo_input = input("Please input tempo in BPM: ")
    midi_info = parse_MIDI(midi_input, int(tempo_input))
    gen_type = input("Additive Synthesis or Wavetable Sythesis. Type 'add' for Additive and 'wav' for Wavetable: ")
    if (gen_type == 'add'):
        wave_type = input("Choose wave type. Type 'sine', 'saw', 'square', or 'triangle': ")
        num_harmonics = input("Type the number of harmonics: ")
        num_harmonics = int(num_harmonics)
        print('\nDefine the ADSR envelope parameters as percentages (0-1) of each note')
        attack = input('Type attack percentage (0-1): ')
        attack = float(attack)
        decay = input('Type decay percentage (0-1): ')
        decay = float(decay)
        sustain = input('Type sustained amplitude (0-1): ')
        sustain = float(sustain)
        release = input('Type release percentage (0-1): ')
        release = float(release)
        wave_valid = False
        while (not wave_valid):
            if wave_type == 'sine':
                wave_valid = True;
                play_list = np.array([])
                for i in midi_info:
                    note_sine = synth_helpers.additive('sine', i[0], i[2], num_harmonics, i[1])
                    note_sine = synth_helpers.adsr(note_sine, attack, decay, sustain, release)
                    play_list = np.concatenate((play_list, note_sine))
            elif wave_type == 'saw':
                wave_valid = True;
                play_list = np.array([])
                for i in midi_info:
                    note_sine = synth_helpers.additive('saw', i[0], i[2], num_harmonics, i[1])
                    note_sine = synth_helpers.adsr(note_sine, attack, decay, sustain, release)
                    play_list = np.concatenate((play_list, note_sine))
            elif wave_type == 'square':
                wave_valid = True;
                play_list = np.array([])
                for i in midi_info:
                    note_sine = synth_helpers.additive('square', i[0], i[2], num_harmonics, i[1])
                    note_sine = synth_helpers.adsr(note_sine, attack, decay, sustain, release)
                    play_list = np.concatenate((play_list, note_sine))
            elif wave_type == 'triangle':
                wave_valid = True;
                play_list = np.array([])
                for i in midi_info:
                    note_sine = synth_helpers.additive('triangle', i[0], i[2], num_harmonics, i[1])
                    note_sine = synth_helpers.adsr(note_sine, attack, decay, sustain, release)
                    play_list = np.concatenate((play_list, note_sine))
            else:
                wave_type = input("Choose wave type. Type 'sine', 'saw', 'square', or 'triangle': ")
    else: 
        synth_helpers.init()
        wave_type = input("Choose wave type. Type 'sine', 'saw', 'square', or 'triangle': ")
        print('\nDefine the ADSR envelope parameters as percentages (0-1) of each note')
        attack = input('Type attack percentage (0-1): ')
        attack = float(attack)
        decay = input('Type decay percentage (0-1): ')
        decay = float(decay)
        sustain = input('Type sustained amplitude (0-1): ')
        sustain = float(sustain)
        release = input('Type release percentage (0-1): ')
        release = float(release)
        wave_valid = False
        while not wave_valid:
            if wave_type == 'sine':
                play_list = np.array([])
                for i in midi_info:
                    note_sine = synth_helpers.wavetable(i[0], i[2], i[1], 'sine')
                    note_sine = synth_helpers.adsr(note_sine, attack, decay, sustain, release)
                    play_list = np.concatenate((play_list, note_sine))
            elif wave_type == 'saw':
                play_list = np.array([])
                for i in midi_info:
                    note_sine = synth_helpers.wavetable(i[0], i[2], i[1], 'saw')
                    note_sine = synth_helpers.adsr(note_sine, attack, decay, sustain, release)
                    play_list = np.concatenate((play_list, note_sine))
            elif wave_type == 'square':
                play_list = np.array([])
                for i in midi_info:
                    note_sine = synth_helpers.wavetable(i[0], i[2], i[1], 'square')
                    note_sine = synth_helpers.adsr(note_sine, attack, decay, sustain, release)
                    play_list = np.concatenate((play_list, note_sine))
            elif wave_type == 'triangle':
                play_list = np.array([])
                for i in midi_info:
                    note_sine = synth_helpers.wavetable(i[0], i[2], i[1], 'triangle')
                    note_sine = synth_helpers.adsr(note_sine, attack, decay, sustain, release)
                    play_list = np.concatenate((play_list, note_sine))
            else:
                wave_type = input("Choose wave type. Type 'sine', 'saw', 'square', or 'triangle': ")
    user_complete = False
    while not user_complete:
        add_effect = input("Type 'effect' to add an effect or type 'generate' to generate a .wav file: ")
        if add_effect == 'generate':
            user_complete = True
            file_name = input("Type a name for the generated .wav file: ")
            sample_rate = input("Type the output sampling rate (highest 48000): ")
            downsampled = synth_helpers.downSample(play_list, int(sample_rate))
            bit_depth = input("Type the bit depth (32 bit and below): ")
            quantized = synth_helpers.quantize_dither(downsampled, int(bit_depth))
            write((file_name + '.wav'), int(sample_rate), quantized)
        else:
            effect = input("Type 'ring' to add a ring modulation, type 'lfo' to add a low frequency oscillator, type 'reverb' to add reverb, type, type 'low' to add a lowpass filter, type 'high' to add a highpass filter, or type 'flanger' to add a flanger: ")
            if effect == 'ring':
                rate = input("Type the rate of the modulator (try 0.5): ")
                blend = input("Type the blend amount from 0-1 (try 0.5): ")
                play_list = synth_helpers.ring_modulation(play_list, rate=float(rate), blend=float(blend), block_size=512)
            elif effect == 'lfo':
                rate = input("Type the frequency of the oscillator (try 20): ")
                blend = input("Type the blend amount from 0-1 (try 0.5): ")
                play_list = synth_helpers.lfo(play_list, float(rate), float(blend))
            elif effect == 'reverb':
                preset = input("Choose a reverb preset: 'church', 'room', 'opera', or upload your own impulse response with the complete file path: ")
                blend = input("Type the blend amount from 0-1 (try 0.5): ")
                if preset == 'opera':
                    play_list = synth_helpers.reverb(play_list, "OperaHall.wav", float(blend))
                elif preset == 'church':
                    play_list = synth_helpers.reverb(play_list, "StNicolaesChurch.wav", float(blend))
                elif preset == 'room':
                    play_list = synth_helpers.reverb(play_list, "SmallDrumRoom.wav", float(blend))
                else:
                    play_list = synth_helpers.reverb(play_list, preset, float(blend))
            elif effect == 'low':
                cutoff = input("Type the cutoff frequency: ")
                filter_length = input("Type the filter length or type 'default' to use sampling rate / cutoff")
                blend = input("Type the blend amount from 0-1 (try 0.5): ")
                play_list = synth_helpers.lowpass(play_list, float(cutoff), float(blend), filter_length)
            elif effect == 'high':
                cutoff = input("Type the cutoff frequency: ")
                filter_length = input("Type the filter length or type 'default' to use sampling rate / cutoff")
                blend = input("Type the blend amount from 0-1 (default 0.5): ")
                play_list = synth_helpers.highpass(play_list, float(cutoff), float(blend), filter_length)
            elif effect == 'flanger':
                delay_time = input('Type the delay time in seconds (try 0.003): ')
                rate = input('Type the rate (try 0.1): ')
                feedback_percent = input('Type the amount of feedback between 0-1 (try 0.5): ')
                blend = input("Type the blend amount from 0-1 (try 0.5): ")
                play_list = synth_helpers.flanger(play_list, float(delay_time), float(rate), float(feedback_percent), float(blend))

        

main()

# note = synth_helpers.wavetable(440, 1, 1)
# write(('test.wav'), 48000, note)