# A simple simulation of master-slave-trigger in a register
# just for my personal practice and comprehension
# True = 1, False = 0
import time
from pynput import keyboard
#nor gate
def nor_gate(input1, input2):
    return not(bool(input1) or bool(input2))
#and gate
def and_gate(input1, input2):
    return (input1 and input2)
#not gate
def not_gate(input):
    return not input 
#latch_function
def latch_function(input1 = None, input2 = None, latch_data= None):
    if input2 == True:
        latch_data[1] = nor_gate(latch_data[0], input2) 
        latch_data[0] = nor_gate(input1, latch_data[1]) 
    else:
        latch_data[0] = nor_gate(input1, latch_data[1])
        latch_data[1] = nor_gate(latch_data[0], input2)
    latch_data[2] = latch_data[0]
    return latch_data[2]

#data
DATA = True
#Interval of clock
INTERVAL_MS = 1000
#period of clock
half_period = (INTERVAL_MS / 1000.0) / 2
#master_latch
input_from_nor_1_master = False
input_from_nor_2_master = True
output_master = False
master_latch = [input_from_nor_1_master, input_from_nor_2_master, output_master]

#slave_latch
input_from_nor_1_slave = False
input_from_nor_2_slave = True
output_slave = False
slave_latch = [input_from_nor_1_slave,input_from_nor_2_slave, output_slave]
#latch
def latch(input, enable,latch):
    input1 = and_gate(not_gate(input), enable)
    input2 = and_gate(input, enable)
    return latch_function(input1,input2, latch)

#initial clock
clock = True
#data
def get_data():

    return 


def on_press(key):
    global DATA
    if key == keyboard.Key.space:
        if not DATA:
            DATA = True
def on_release(key):
    global DATA
    if key == keyboard.Key.space:
        DATA = False
        
    if key == keyboard.Key.esc:
        print("\nend simulation...")
        global running
        running = False
        return False

listener = keyboard.Listener(on_press=on_press, on_release=on_release)
listener.start()
print("==================================================")
print(" Press [space] to change Data (1-press/0-release)")
print(" Press [esc] to end")
print("==================================================")
print("clock status (Clock) | actual data (Data)")
print("--------------------------------------------------")
#running status
running = True  
try:
    while running: 
        clock = not clock
        print(f"Clock: {int(clock)} | Data: {int(DATA)}")
        master_out = latch(DATA, not clock, master_latch)
        slave_out = latch(master_out, clock, slave_latch)
        print(f"Output : {int(slave_out)}")
        print("--------------------------------------------------")
        time.sleep(half_period)
except KeyboardInterrupt:
    pass                              
finally:
    listener.stop()