import	machine
import	utime

class temp_sensor:
	def __init__( self, bus, address ):
		self.__bus	= bus
		self.__adr	= address
	
	def read( self ):
		v		= list( self.__bus.readfrom( self.__adr, 2 ) )
		return ((v[ 0 ] << 8) | v[ 1 ]) / 256
		

i2c		= machine.I2C( 0 )
ts		= temp_sensor( i2c, 72 )

while True:
	print( ts.read() )
	utime.sleep( 1 )
