import	machine

i2c			= machine.I2C( 0 )
dev_list	= i2c.scan()
print( dev_list )
