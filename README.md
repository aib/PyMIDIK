PyMIDIK
=======

PyMIDIK is a simple MIDI keyboard emulator for Linux/evdev.

How to Use
----------

Simply supplying an input device (/dev/input/eventX) as a command line parameter will launch PyMIDIK and create a MIDI output device. However, it is probably easier to use the `-o` option to connect to an existing MIDI input device:

	fluidsynth -a alsa /usr/share/sounds/sf2/FluidR3_GM.sf2
	python3 pymidik.py -o FLUID /dev/input/event0

You can use the `-l` option to see a list of the available input devices. Make sure you have read access to the /dev device nodes; add your user to the `input` group or use `sudo` in a pinch.

The default key mapping is ZSXD CVGBHNJM / Q2W3E R5T6Y7U / I9O0P for octaves 3/4/5, which seems to be some sort of standard.
