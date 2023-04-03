import pandas as pd
import serial           
from time import sleep       
from datetime import datetime
import RPi.GPIO as GPIO

# Initilize 
df = pd.DataFrame(columns=['Time', 'Lat', 'Long'])
gpgga_info = "$GPGGA,"
ser = serial.Serial ("/dev/ttyS0")              #Open port with baud rate
GPGGA_buffer = 0
NMEA_buff = 0
lat_in_degrees = 0
long_in_degrees = 0
countn=0
global status
status=1
df = pd.DataFrame(columns=['Time', 'Lat', 'Long'])

# GPIO Setup
BUTTON_GPIO = 16
GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTON_GPIO, GPIO.IN, pull_up_down=GPIO.PUD_UP)




def convert_to_degrees(raw_value):
    decimal_value = raw_value/100.00
    degrees = int(decimal_value)
    mm_mmmm = (decimal_value - int(decimal_value))/0.6
    position = degrees + mm_mmmm
    position = "%.8f" %(position) #changed from 4 to 8
    return position

def get_gps_data():
    n=0
    while n<1:
        received_data = (str)(ser.readline())                   #read NMEA string received
        GPGGA_data_available = received_data.find(gpgga_info)   #check for NMEA GPGGA string                 
        if (GPGGA_data_available>0):
            GPGGA_buffer = received_data.split("$GPGGA,",1)[1]  #store data coming after "$GPGGA," string 
            NMEA_buff = (GPGGA_buffer.split(','))               #store comma separated data in buffer
            nmea_time = NMEA_buff[0]                    #extract time from GPGGA string
            nmea_latitude = NMEA_buff[1]                #extract latitude from GPGGA string
            nmea_longitude = NMEA_buff[3]               #extract longitude from GPGGA string
            time=0
            # print("NMEA Time: ", nmea_time,'\n')
            # print ("NMEA Latitude:", nmea_latitude,"NMEA Longitude:", nmea_longitude,'\n')
            time=datetime.strptime(nmea_time[:-3], "%H%M%S").time()
            lat = float(nmea_latitude)                  #convert string into float for calculation
            longi = float(nmea_longitude)               #convertr string into float for calculation
            
            lat_in_degrees = convert_to_degrees(lat)    #get latitude in degree decimal format
            long_in_degrees = convert_to_degrees(longi) #get longitude in degree decimal format
            # sleep(1)
            n+=1
    return {"Time": time, "Lat": lat_in_degrees, "Long":long_in_degrees}

def record_data(df):
        data=get_gps_data()
        df=df.append(data,ignore_index=True)
        return df


def callback_fall(a):
    print(str(a)+"  Switch Triggered")
    global status
    global countn
    global double_flick
    countn+=1
    double_flick+=1
    if double_flick == 2:
        status=2
    elif countn % 2 ==0:
        status=1
    elif countn %2 == 1:
        status=0
    
# This sets up the interrupt mechanism to operate the switch
GPIO.add_event_detect(BUTTON_GPIO, GPIO.BOTH, 
        callback=callback_fall, bouncetime=50)

while(True):
    if status == 0:
        print("Recording Data")
        print(get_gps_data())
        df=record_data(df)
        sleep(2)
        double_flick=0
    if status == 1:
        print("Paused Recording Data")
        get_gps_data() #just to dump buffer
        sleep(2)
        double_flick=0
    if status == 2:
        print("Saved and Reset \n#\n#\n#\n#")
        df.to_csv(f"{datetime.now()}_GPS_LOG")
        df= pd.DataFrame(columns=['Time', 'Lat', 'Long'])
        sleep(2)
        status=1
        countn=0



