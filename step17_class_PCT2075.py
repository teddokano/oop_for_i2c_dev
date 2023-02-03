import	machine
import	utime

class temp_sensor:
	def __init__( self, bus, address ):
		self.__bus	= bus
		self.__adr	= address
	
	def read( self ):
		v		= list( self.__bus.readfrom( self.__adr, 2 ) )
		return ((v[ 0 ] << 8) | v[ 1 ]) / 256
		

i2c_0		= machine.I2C( 0 )
i2c_1		= machine.I2C( 1 )

ts0		= temp_sensor( i2c_0, 72 )
ts1		= temp_sensor( i2c_0, 73 )
ts2		= temp_sensor( i2c_0, 74 )
ts3		= temp_sensor( i2c_1, 72 )
ts4		= temp_sensor( i2c_1, 73 )
ts5		= temp_sensor( i2c_1, 74 )

while True:
	print( ts0.read() )
	print( ts1.read() )
	print( ts2.read() )
	print( ts3.read() )
	print( ts4.read() )
	print( ts5.read() )
	utime.sleep( 1 )
