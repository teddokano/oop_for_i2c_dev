import	machine
import	utime

def read_temp( bus, address ):
	v		= list( bus.readfrom( address, 2 ) )
	return ((v[ 0 ] << 8) | v[ 1 ]) / 256



i2c_0		= machine.I2C( 0 )
i2c_1		= machine.I2C( 1 )

while True:
	print( read_temp( i2c_0, 72 ) )
	print( read_temp( i2c_0, 73 ) )
	print( read_temp( i2c_0, 74 ) )
	print( read_temp( i2c_1, 72 ) )
	print( read_temp( i2c_1, 73 ) )
	print( read_temp( i2c_1, 74 ) )
	utime.sleep( 1 )
