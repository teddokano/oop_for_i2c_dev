import	machine
import	utime

def read_temp():
	v		= list( i2c.readfrom( 72, 2 ) )
	return ((v[ 0 ] << 8) | v[ 1 ]) / 256



i2c		= machine.I2C( 0 )

while True:
	print( read_temp() )
	utime.sleep( 1 )
