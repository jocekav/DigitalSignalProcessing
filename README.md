# DigitalSignalProcessing

DSP Final Project
Davis House and Jocelyn Kavanagh

Required libraries/modules
- Mido (https://mido.readthedocs.io/en/latest/midi_files.html)
- NumPy
- SciPy

How to run:
- Run synth.py 
    - Follow CLI input instructions
    - Reference list below for any parameter confusion
- Use 'saltarello2.mid' with a tempo of 600 and additive synth for smooth/quick demo purposes

Synth Engines
- Additive Synth (control number of harmonics)
- Wavetable (control type of wave form)
    ** Note, this takes a long time to run. For demo purposes, use additive synth. **
Convolution
- Reverb (3 presets and ability to upload wav file with impulse response)
Modulated Effects
- ADSR 
- Amplitude LFO (control rate)
- Flanger (feedback effect) (control delay, rate, feedback%)
- Ring Modulation (control rate)
Filters
- Highpass
- Lowpass

    ** Note, this uses convolution to apply sinc function generated coefficients. You can specify filter length, but it defaults to sampling rate (48000) / cutoff frequency **
Musical Data
- MIDI input
    ** Note, the tempo calculation seems to vary depending on the MIDI file. The conversion calculation is correct, however, you may need to experiment with the appropriate tempo as it does not always map directly to BPM. **
    ** Note, only input monophonic MIDI files. You can use the MIDI files in our repo, specifically 'saltarello2.mid' with a tempo of 600 yields good results. **
Audio Output
- File output


Command Line Examples:
MIDI info prompts: 
- 'saltarello2.mid' with tempo of 600
- 'Saw.mid' with a tempo of 140
- 'scale.mid' with a tempo of 4000 (use this especially if you are doing wavetable)
Generation prompts:
- type 'add' for additive synthesis
    - choose any type of oscillator by typing 'sine' for sine, 'saw' for saw, 'square' for square, and 'triangle' for triangle
    - choose any range of harmonics to be added as an int, eg. 1, 2, 3, 7, 10
        - the more harmonics the slower it runs
    - type 'wav' for wavetable synthesis
        - choose any type of oscillator by typing 'sine' for sine, 'saw' for saw, 'square' for square, and 'triangle' for triangle
    - ADSR
        - type a decimal between 0-1 for the percentage of the attack, decay, release and type the sustain amplitude level
            - .25 for attack, .25 for decay, .8 for sustain, .25 for release
    - Note the generation may take a second, especially if you use wavetable
    
Effects:
  - type 'effect' to add effects
  - add ring modulation by typing 'ring' with parameters rate and blend
    - type .5 for rate and .75 for blend
  - add an LFO by typing 'lfo' with parameters rate and blend
      - type 20 for rate and .75 for blend
  - add a flanger by typing 'flanger' with parameters delay time, rate, feedback %, and blend
      - type 0.003 for delay time, 0.1 for rate, .5 for feedback, and .5 for blend
  - add high pass by typing 'high' with parameters cutoff frequency, filter length, and blend
      - type 1500 for cutoff, 'default' for filter length, and .8 for blend
  - add low pass by typing 'low' with parameters cutoff frequency, filter length, and blend
      - type 200 for cutoff, 'default' for filter length, and .8 for blend
  - add reverb by typing 'reverb' with parameters preset and blend
      - type 'room' for preset and blend .6
      - type 'church' for preset and blend .6

Output:
  - type 'generate' to stop adding effects
  - type a name for your wav file (we usually use 'test') (you don't need to put .wav)
  - type the output sampling rate
      - type 48000 or type 24000
  - type the output bit depth
      - type 32 or type 16 or type 8
  - file will write to the directory of the python file folder

