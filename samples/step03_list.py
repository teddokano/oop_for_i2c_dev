import	machine
import	utime

pin		= machine.Pin( "D4", machine.Pin.OUT )
pattern	= [1,1,1,0,1,1,1,0,1,1,1,0,1]

for v in pattern:
	pin.value( v )
	utime.sleep(0.1)

	pin.value( 0 )
	utime.sleep(0.1)
