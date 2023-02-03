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

ts_list		= [	temp_sensor( i2c_0, 72 ), 
				temp_sensor( i2c_0, 73 ),
				temp_sensor( i2c_0, 74 ),
				temp_sensor( i2c_1, 72 ),
				temp_sensor( i2c_1, 73 ),
				temp_sensor( i2c_1, 74 )
			  ]
			  
while True:
	for ts in ts_list:
		print( ts.read() )
		utime.sleep( 1 )
