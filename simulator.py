'''
Adrian Arcilla
Resources:
	http://stackoverflow.com/questions/20955543/python-writing-binary
	http://stackoverflow.com/questions/1035340/reading-binary-file-in-python

PLEASE NOTE THAT YOU NEED TO GIVE 3 INPUTS WHEN RUNNING THIS FILE:
1) Packet Size to read
2) Probability threshold of success
3) Policy to use for lost packets
'''

import sys
import random


def main():
	if(len(sys.argv) != 4):
		sys.stderr.write('ERROR: Invalid number of args. Terminating.\n')
		return 0

	packetSize = int(sys.argv[1]) #packet size
	probability = int(sys.argv[2]) #probability threshold of success
	policy = str(sys.argv[3]) #policy


	if(policy != "silence" and policy != "replay" and policy != "lastPacket"):
		sys.stderr.write('ERROR: Not a valid policy. Terminating\n')
		return 0

	pa = str(packetSize)
	pr = str(probability)

	originalFile = open("pink_panther.au", "rb")
	newFile = open("new_panther_" + pa + "_" + pr + "_" + policy + ".au", "wb")

	output = bytearray()
	try:
		byte = originalFile.read(24)
		for b in byte:
			output.append(b)

		while byte != "":
			if(probability > random.randint(0,99)):
				byte = originalFile.read(packetSize)

			else:
				if(policy == "silence"):
					byte = bytearray(packetSize)

				elif(policy == "replay"):
					b = chr(output[len(output)-1])
					byte = bytearray(packetSize)
					for i in range(0, packetSize):
						byte.append(b)

				else: #policy is "lastPacket"
					byte = bytearray(packetSize)
					for i in range(packetSize, 1, -1):
						z = len(output)
						if(z < packetSize):
							b = b'\x00'
						else:
							b = chr(output[len(output)-(i%(len(output)-23))])
						byte.append(b)

				originalFile.read(packetSize)
			for b in byte:
				output.append(b)
		newFile.write(output)

	finally:
		originalFile.close()
		newFile.close()

main()
