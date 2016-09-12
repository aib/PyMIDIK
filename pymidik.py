#!/usr/bin/env python3

import sys

import evdev
from evdev import ecodes

import rtmidi
from rtmidi import midiconstants

kcodes = ecodes.ecodes
keyMap = {
	kcodes['KEY_Q']: 72,
	kcodes['KEY_2']: 73,
	kcodes['KEY_W']: 74,
	kcodes['KEY_3']: 75,
	kcodes['KEY_E']: 76,

	kcodes['KEY_R']: 77,
	kcodes['KEY_5']: 78,
	kcodes['KEY_T']: 79,
	kcodes['KEY_6']: 80,
	kcodes['KEY_Y']: 81,
	kcodes['KEY_7']: 82,
	kcodes['KEY_U']: 83,

	kcodes['KEY_I']: 84,
	kcodes['KEY_9']: 85,
	kcodes['KEY_O']: 86,
	kcodes['KEY_0']: 87,
	kcodes['KEY_P']: 88,

	kcodes['KEY_Z']: 60,
	kcodes['KEY_S']: 61,
	kcodes['KEY_X']: 62,
	kcodes['KEY_D']: 63,
	kcodes['KEY_C']: 64,

	kcodes['KEY_V']: 65,
	kcodes['KEY_G']: 66,
	kcodes['KEY_B']: 67,
	kcodes['KEY_H']: 68,
	kcodes['KEY_N']: 69,
	kcodes['KEY_J']: 70,
	kcodes['KEY_M']: 71
}

def key_code_to_midi_note(code):
	try:
		return keyMap[code]
	except KeyError:
		return None

def list_devices():
	devs = [evdev.InputDevice(fn) for fn in evdev.list_devices()]
	for dev in devs:
		print("%s %s" % (dev.fn, dev.name))

def main():
	if len(sys.argv) < 2:
		list_devices()
		sys.exit(1)

	dev_path = sys.argv[1]

	midiout = rtmidi.MidiOut()
	midiout.open_virtual_port("PyMIDIK")

	dev = evdev.InputDevice(dev_path)

	for ev in dev.read_loop():
		if ev.type == evdev.ecodes.EV_KEY:
			if ev.value == 1:
				note = key_code_to_midi_note(ev.code)
				if note is not None:
					midiout.send_message([midiconstants.NOTE_ON, note, 127])
			elif ev.value == 0:
				note = key_code_to_midi_note(ev.code)
				if note is not None:
					midiout.send_message([midiconstants.NOTE_OFF, note, 0])

if __name__ == '__main__':
	main()
