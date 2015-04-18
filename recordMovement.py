#Get acceleration data from Chronos watch.
#Taken from info posted at: http://e2e.ti.com/support/microcontrollers/msp43016-bit_ultra-low_power_mcus/f/166/t/32714.aspx
#x, y, and z values may not be "in order". The first three bytes from the packet
#of data sent from the watch seemed to be different than what was listed
#on the page, though the datatype byte was in the correct place. So YMMV.
#
#Written by Sean Brewer (seabre)
#seabre986@gmail.com
#

import serial
import array
import os
import random
import time
import mp3play

def startAccessPoint():
    return array.array('B', [0xFF, 0x07, 0x03]).tostring()

def accDataRequest():
    return array.array('B', [0xFF, 0x08, 0x07, 0x00, 0x00, 0x00, 0x00]).tostring()

PATTERN_LENGTH = 10

volume = 20

clip = mp3play.load(r'C:\Users\Mahesh\Desktop\mp3 files\Guns_N_Roses_-_Sweet_Child_O_Mine.mp3')
#Open COM port 6 (check your system info to see which port
#yours is actually on.)
#argments are 5 (COM6), 115200 (bit rate), and timeout is set so
#the serial read function won't loop forever.
ser = serial.Serial('COM8',115200,timeout=0)

#Start access point
ser.write(startAccessPoint())

"""
x_pattern_swipe_right = [-36, -36, -43, -41, -37, -30, -34, -33, -32]
y_pattern_swipe_right = [-34, -35, -41, -32, -15, -17, -25, -30, -29]
z_pattern_swipe_right = [12, 11, -3, -4, 37, 45, 32, 28, 25]
"""

x_pattern = []
y_pattern = []
z_pattern = []

"""
print "Recording pattern - start"
p1 = open('C:\Users\Mahesh\Desktop\HackRice\log files\swipe_down.txt', 'a')
for i in range(0, PATTERN_LENGTH):
    time.sleep(0.1)
    print "Scanning record ", i
    ser.write(accDataRequest())
    accel = ser.read(7)

    if len(accel) != 7 or (ord(accel[0]) == 0 and ord(accel[1]) == 0 and ord(accel[2]) == 0):
        continue

    x_pattern.append(ord(accel[4]) - 256 if ord(accel[4]) > 127 else ord(accel[4]))
    y_pattern.append(ord(accel[5]) - 256 if ord(accel[5]) > 127 else ord(accel[5]))
    z_pattern.append(ord(accel[6]) - 256 if ord(accel[6]) > 127 else ord(accel[6]))
    p1.write("x_pattern[%d]: %d y_pattern[%d]: %d z_pattern[%d]: %d\n" % (i-1, x_pattern[i-1], i-1, y_pattern[i-1], i-1, z_pattern[i-1]))

p1.close()
print "Recording pattern - end"
"""

x_pattern_right = [-55, -53, -32, -36, -39, -35, -37, -36, -38]
y_pattern_right = [-46, 2, -11, -23, -28, -26, -28, -29, -29]
z_pattern_right = [-65, 22, 54, 27, 20, 21, 20, 21, 20]

x_pattern_left = [-37, -41, -50, -40, -45, -39, -39, -40, -41]
y_pattern_left = [-25, -14, -20, -31, -29, -28, -27, -28, -29]
z_pattern_left = [75, -1, -22, -2, 7, 15, 16, 13, 12]

x_pattern_up = [-43, -42, -46 ,-113, -54, 0, -2, -16, -23]
y_pattern_up = [-26, -27, -32, -85, -22, 3, -26, -40, -45]
z_pattern_up = [11, 11, 13, 55, 19, -6, 9, 17, 20]

x_pattern_down = [-30, -30, -29, 4, -22, -110, -71, -50, -45]
y_pattern_down = [-33, -31, -29, 23, -4, -10, 7, 12, 11]
z_pattern_down = [26, 26, 24, -8, 3, 53, 34, 13, 16]

x_data = []
y_data = []
z_data = []

for i in range(0, PATTERN_LENGTH):
    #Send request for acceleration data
    time.sleep(0.1)
    ser.write(accDataRequest())
    accel = ser.read(7)

    if len(accel) != 7 or (ord(accel[0]) == 0 and ord(accel[1]) == 0 and ord(accel[2]) == 0):
        continue

    x_actual = ord(accel[4]) - 256 if ord(accel[4]) > 127 else ord(accel[4])
    y_actual = ord(accel[5]) - 256 if ord(accel[5]) > 127 else ord(accel[5])
    z_actual = ord(accel[6]) - 256 if ord(accel[6]) > 127 else ord(accel[6])

    x_data.append(x_actual)
    y_data.append(y_actual)
    z_data.append(z_actual)


print x_data
print y_data
print z_data

data_insertion_index = 0
data_count = 0
data_comparison_index = 0

sample_counter = 0

last_match_timestamp = 0

while True:
    sample_counter += 1
    x_right_error = 0
    y_right_error = 0
    z_right_error = 0

    x_left_error = 0
    y_left_error = 0
    z_left_error = 0

    x_up_error = 0
    y_up_error = 0
    z_up_error = 0

    x_down_error = 0
    y_down_error = 0
    z_down_error = 0

    data_count = 0
    data_comparison_index = data_insertion_index

    while True:
        if(data_count == PATTERN_LENGTH-1 or data_comparison_index >= 9):
            break

        #print data_comparison_index
        #print x_data[data_comparison_index]
        #print x_pattern_right[data_count]

        x_right_error += abs(x_data[data_comparison_index] - x_pattern_right[data_count])
        y_right_error += abs(y_data[data_comparison_index] - y_pattern_right[data_count])
        z_right_error += abs(z_data[data_comparison_index] - z_pattern_right[data_count])

        x_left_error += abs(x_data[data_comparison_index] - x_pattern_left[data_count])
        y_left_error += abs(y_data[data_comparison_index] - y_pattern_left[data_count])
        z_left_error += abs(z_data[data_comparison_index] - z_pattern_left[data_count])

        x_up_error += abs(x_data[data_comparison_index] - x_pattern_up[data_count])
        y_up_error += abs(y_data[data_comparison_index] - y_pattern_up[data_count])
        z_up_error += abs(z_data[data_comparison_index] - z_pattern_up[data_count])

        x_down_error += abs(x_data[data_comparison_index] - x_pattern_down[data_count])
        y_down_error += abs(y_data[data_comparison_index] - y_pattern_down[data_count])
        z_down_error += abs(z_data[data_comparison_index] - z_pattern_down[data_count])

        data_comparison_index = (data_comparison_index + 1) %( PATTERN_LENGTH - 1)
        data_count += 1

    #Send request for acceleration data
    time.sleep(0.1)
    ser.write(accDataRequest())
    accel = ser.read(7)

    if len(accel) != 7 or (ord(accel[0]) == 0 and ord(accel[1]) == 0 and ord(accel[2]) == 0):
        continue

    x_actual = ord(accel[4]) - 256 if ord(accel[4]) > 127 else ord(accel[4])
    y_actual = ord(accel[5]) - 256 if ord(accel[5]) > 127 else ord(accel[5])
    z_actual = ord(accel[6]) - 256 if ord(accel[6]) > 127 else ord(accel[6])

    print "x_error: %d y_error: %d z_error: %d" % (x_left_error, y_left_error, z_left_error)
    #f = open('C:\Users\Mahesh\Desktop\HackRice\log files\log.txt', 'a')
    #f.write("x_error: %d y_error: %d z_error: %d\n" % (x_error, y_error, z_error))

    x_data[data_insertion_index] = x_actual
    y_data[data_insertion_index] = y_actual
    z_data[data_insertion_index] = z_actual

    data_insertion_index = (data_insertion_index + 1) % (PATTERN_LENGTH-1)

    if(x_right_error < 180 and y_right_error < 160 and z_right_error < 120):
        if (time.time() - last_match_timestamp >= 3):
            print "\t\t\tRIGHT PATTERN DETECTED"
            clip = mp3play.load(r'C:\Users\Mahesh\Desktop\mp3 files\\' + random.choice(os.listdir('C:\Users\Mahesh\Desktop\mp3 files')))
            #print new_track
            clip.play()
            clip.volume(volume)
        last_match_timestamp = time.time()

    if(x_left_error < 180 and y_left_error < 160 and z_left_error < 120):
        if (time.time() - last_match_timestamp >= 3):
            print "\t\t\tLEFT PATTERN DETECTED"
            if (clip.isplaying()):
                clip.pause()
            else:
                clip.unpause()
        last_match_timestamp = time.time()

    if(x_up_error < 180 and y_up_error < 160 and z_up_error < 120):
        if(time.time() - last_match_timestamp >= 3):
            print "\t\t\tUP PATTERN DETECTED"
            volume += 40
            if (volume > 100): volume = 100
            clip.volume(volume)
        last_match_timestamp = time.time()

    if(x_down_error < 180 and y_down_error < 160 and z_down_error < 120):
        if(time.time() - last_match_timestamp >= 3):
            print "\t\t\tDOWN PATTERN DETECTED"
            volume -= 40
            if (volume < 0): volume = 0
            clip.volume(volume)
        last_match_timestamp = time.time()

ser.close()