import	machine

i2c		= machine.I2C( 0 )
value	= i2c.readfrom( 72, 2 )
print( value )	# read value is in bytearray format

v	= list( value )
print( v )


temp16bit	= (v[ 0 ] << 8) | v[ 1 ]
print( temp16bit )
print( temp16bit / 256 )
