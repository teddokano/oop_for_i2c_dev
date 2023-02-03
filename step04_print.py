import	machine
import	utime

pin		= machine.Pin( "D4", machine.Pin.OUT )
pattern	= [ 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1 ]

print( "Hello, world!" )
print( pattern )

pat2	= [ 1, 2**32, 3.14, "Strawberry", "fields", True, False ]
print( pat2 )


for v in pattern:
	pin.value( v )
	utime.sleep(0.1)

	pin.value( 0 )
	utime.sleep(0.1)
