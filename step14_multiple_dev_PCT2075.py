import	machine
import	utime

def read_temp( address ):
	v		= list( i2c.readfrom( address, 2 ) )
	return ((v[ 0 ] << 8) | v[ 1 ]) / 256



i2c		= machine.I2C( 0 )

while True:
	print( read_temp( 72 ) )
	print( read_temp( 73 ) )
	print( read_temp( 74 ) )
	utime.sleep( 1 )
