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


BUTTON_GPIO = 16


def convert_to_degrees(raw_value):
    decimal_value = raw_value/100.00
    degrees = int(decimal_value)
    mm_mmmm = (decimal_value - int(decimal_value))/0.6
    position = degrees + mm_mmmm
    position = "%.4f" %(position)
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
            print("NMEA Time: ", nmea_time,'\n')
            print ("NMEA Latitude:", nmea_latitude,"NMEA Longitude:", nmea_longitude,'\n')
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


def callback():
     countn+=1
     status=False





        



if __name__ == '__main__':
    GPIO.setmode(GPIO.BCM)
    
    GPIO.setup(BUTTON_GPIO, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(BUTTON_GPIO, GPIO.FALLING, 
            callback=callback, bouncetime=200)
    
    while(True):
        if status is True:
            df = pd.DataFrame(columns=['Time', 'Lat', 'Long'])
            record_data(df)
            sleep(2)
        else:
             
    
         

    


k=0
while k<5:
    print(get_gps_data())
    data=get_gps_data()
    df=df.append(data,ignore_index=True)
    sleep(1)
    k+=1

print(df)

