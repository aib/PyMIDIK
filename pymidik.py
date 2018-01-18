#!/usr/bin/env python3

import argparse
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

args = None

def key_code_to_midi_note(code):
	try:
		return keyMap[code]
	except KeyError:
		return None

def list_ports_and_devices():
	print("MIDI input ports:")
	with rtmidi.MidiOut() as mo:
		ports = mo.get_ports()
	for port in ports:
		print("    %s" % (port,))

	print("Devices:")
	devs = [evdev.InputDevice(fn) for fn in evdev.list_devices()]
	for dev in devs:
		print("    %s %s" % (dev.fn, dev.name))

def parse_channel(string):
	val = int(string)
	if val < 1 or val > 16:
		raise argparse.ArgumentTypeError("Invalid channel number %r" % string)
	return val - 1

def parse_transpose(string):
	val = int(string)
	if val <= -127 or val >= 127:
		raise argparse.ArgumentTypeError("Invalid transpose amount %r" % string)
	return val

def _send_message(port, msg):
	if args.verbose:
		print("Sent", msg)
	port.send_message(msg)

def main():
	parser = argparse.ArgumentParser(description="Virtual MIDI keyboard")

	parser.add_argument(
		'device', help="Evdev input device",
		nargs='?')

	parser.add_argument(
		'-l', '--list', help="List MIDI input ports, input devices and quit",
		dest='list', action='store_true')

	parser.add_argument('-n', '--port-name', help="MIDI output port name to create",
		dest='port_name', default="PyMIDIK")

	parser.add_argument('-o', '--connect', help="MIDI input port to connect to",
		dest='connect_port')

	parser.add_argument('-c', '--channel', help="MIDI channel number (1-16)",
		dest='channel', type=parse_channel, default=0)

	parser.add_argument('-t', '--transpose', help="Transpose MIDI notes by amount (+/- 0-126)",
		dest='transpose', type=parse_transpose, default=0)

	parser.add_argument('-g', '--grab', help="Grab input device, swallow input events",
		dest='grab', action='store_true')

	parser.add_argument('-v', '--verbose', help="Print MIDI messages",
		dest='verbose', action='store_true')

	global args
	args = parser.parse_args()

	if args.list:
		list_ports_and_devices()
		sys.exit(0)

	if args.device is None:
		parser.print_help()
		sys.exit(1)

	midiout = rtmidi.MidiOut()

	if args.connect_port is None:
		midiout.open_virtual_port(args.port_name)
		print("Opened virtual port \"%s\"" % (args.port_name,))
	else:
		ports = list(filter(lambda p: p[1].startswith(args.connect_port), enumerate(midiout.get_ports())))
		if len(ports) == 0:
			print("No MIDI input ports found matching \"%s\"" % (args.connect_port,))
			sys.exit(3)
		else:
			port = ports[0]
			midiout.open_port(port[0])
			print("Connected to port \"%s\"" % (port[1]))

	dev = evdev.InputDevice(args.device)

	if args.grab:
		dev.grab()

	for ev in dev.read_loop():
		if ev.type == evdev.ecodes.EV_KEY:
			if ev.value == 1:
				note = key_code_to_midi_note(ev.code)
				if note is not None:
					_send_message(midiout, [
						midiconstants.NOTE_ON + args.channel,
						(note + args.transpose) % 127,
						127
					])
			elif ev.value == 0:
				note = key_code_to_midi_note(ev.code)
				if note is not None:
					_send_message(midiout, [
						midiconstants.NOTE_OFF + args.channel,
						(note + args.transpose) % 127,
						0
					])
	if args.grab:
		dev.ungrab()

if __name__ == '__main__':
	main()
