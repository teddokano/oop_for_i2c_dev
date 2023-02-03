import	machine

i2c		= machine.I2C( 0 )
value	= i2c.readfrom( 72, 2 )
print( value )	# read value is in bytearray format

v	= list( value )
print( v )
