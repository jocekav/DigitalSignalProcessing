DSP Final Project
Davis House and Jocelyn Kavanagh

Required libraries/modules
- Mido (https://mido.readthedocs.io/en/latest/midi_files.html)
- NumPy
- SciPy

Synth Engines
- Additive Synth (control number of harmonics)
- Wavetable (control type of wave form)
    ** Note, this takes a long time to run. For demo purposes, use additive synth. **
Convolution
- Reverb (3 presets and ability to upload wav file with impulse response)
Modulated Effects
- ADSR 
- Amplitude LFO (control rate)
- Flanger (feedback effect) (control delay, depth, feedback%)
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
