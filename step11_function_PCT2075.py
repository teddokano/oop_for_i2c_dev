import	machine
import	utime

def read_temp():
	value	= i2c.readfrom( 72, 2 )
	v		= list( value )
	temp	= ((v[ 0 ] << 8) | v[ 1 ]) / 256

	return temp	



i2c		= machine.I2C( 0 )

# trying to get temp every second

while True:
	t	= read_temp()
	print( t )
	utime.sleep( 1 )
