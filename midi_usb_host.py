import subprocess
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)
GPIO.setup(10, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

hardware_ports = []

def getConnectedDevices():
	midi_connections = subprocess.check_output(["aconnect", "-l"])
	components = midi_connections.split("client ")
	relevant_connections = components[3:] 

	print('Found ' + str(len(relevant_connections)) + ' connected devices')
	print(relevant_connections)
	print('\n')

	global hardware_ports
	hardware_ports = map(lambda c: c.split(":")[0], relevant_connections)

def disconnectAllDevices():
	output = subprocess.call(["aconnect", "-x"])
	print('Disconnecting all devices')

def connectDevices():
	if len(hardware_ports) < 2:
		print('Not enough connected devices\n')
		return

	
	input_device = hardware_ports[0] + ':0'
	output_device = hardware_ports[1] + ':0'

	print('Connecting device ' + input_device + ' -> ' + output_device)
	subprocess.call(["aconnect", input_device, output_device])

	print('Connecting device ' + output_device + ' -> ' + input_device + '\n')
	subprocess.call(["aconnect", output_device, input_device])
	

def lookForButtonPress():
	while True:
		try:
			channel = GPIO.wait_for_edge(10, GPIO.RISING, timeout=3000)
			if channel is None:
				print('Timeout occurred')
			else:
				print('Edge detected on channel', channel)
				getConnectedDevices()
				disconnectAllDevices()
				connectDevices()

		except KeyboardInterrupt:
			print("*** Ctrl+C pressed, exiting")
			break


lookForButtonPress()

GPIO.cleanup()