### this code has a bug. need to fix to run :)

import	machine
import	utime

pin		= machine.Pin( "D4", machine.Pin.OUT )
state	= 0

while True:
	if state:
		state	= 0
	else
		state	= 1

	pin.value( state )
	utime.sleep(0.1)
