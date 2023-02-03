import	machine
import	utime

pin	= machine.Pin( "D4", machine.Pin.OUT )

while True:
	pin.value( 1 )
	utime.sleep(0.1)

	pin.value( 0 )
	utime.sleep(0.1)
