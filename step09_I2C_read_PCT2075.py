import	machine

i2c		= machine.I2C( 0 )

value	= i2c.readfrom( 72, 2 )
v		= list( value )
temp	= ((v[ 0 ] << 8) | v[ 1 ]) / 256
print( temp )
