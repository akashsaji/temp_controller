import os
import time
import serial

# A library for connection with serial port. Should run fine on computer, Raspberry Pi and Arduino Uno
class MTD415T_temperature_stabilization_module:

    def __init__(self, serial_file_name = "/dev/serial0", baud_rate = 115200):

        self.serial_file_name = serial_file_name
        self.baud_rate = baud_rate
        self.serial_port = serial.Serial (self.serial_file_name, self.baud_rate) # Don't forget this

    '''
    def run_command_on_module(self, command_name, no_of_attempts = 100):

        os.system("echo "+command_name+" >> "+self.serial_file_name) # Send command to module
        # Receive data from module 
        for i in range(0, no_of_attempts):        
            time.sleep(1)  # Crucial to wait for the data to be received by the Raspberry Pi
            with open(self.serial_file_name, "rb") as serial_port:
                received_data = serial_port.readline().decode()
                if(len(received_data) > 0):
                    return received_data.replace('\n','')
        
        return "No Output received"
    '''
    
    def run_command_on_module(self, command_name, no_of_attempts = 100):

        os.system("echo "+command_name+" >> "+self.serial_file_name) # Send command to module
        # Receive data from module
        received_data = ""
        for i in range(0, no_of_attempts):        
            time.sleep(0.01)  # Crucial to wait for the data to be received by the Raspberry Pi
            with open(self.serial_file_name, "rb") as serial_port:
                received_data += serial_port.readline().decode()
                if(received_data.find('\n') > 0):
                    return received_data.replace('\n','')
        
        return "No Output received"

    def save_configuration_to_flash_memory_of_module(self):

        self.run_command_on_module("M", 100) # Not implemented yet

    def set_temperature(self, laser_temperature = 25000): #Temperature is set in millikelvin

        self.run_command_on_module("T"+str(laser_temperature), 100) 

    def set_temperature_status_LED_delay(self, temperature_status_LED_delay = 6): 

        self.run_command_on_module("d"+str(temperature_status_LED_delay), 100) 

    def get_temperature_status_LED_delay(self, temperature_status_LED_delay = 6): 

        return self.run_command_on_module("d?", 100) 

    def set_PID_loop_cycle_time(self, PID_loop_cycle_time = 50):

        return self.run_command_on_module("C"+str(PID_loop_cycle_time), 100)
        
    def set_PID_values(self, proportional = 1000, integral = 200, differential = 100):

        if(proportional != None):
            self.run_command_on_module("P"+str(proportional), 100) 
        if(integral     != None):
            self.run_command_on_module("I"+str(integral), 100) 
        if(differential != None):
            self.run_command_on_module("D"+str(differential), 100)

    def get_PID_values(self):
     
        return [self.run_command_on_module("P?", 100), self.run_command_on_module("I?", 100), self.run_command_on_module("D?", 100)]

    def set_thermoelectric_cooler_current_limit(self, thermoelectric_cooler_current_limit = 1000):

        self.run_command_on_module("L"+str(thermoelectric_cooler_current_limit), 100) 
        
    def set_stable_temperature_window(self, stable_temperature_window = 500):

        self.run_command_on_module("W"+str(stable_temperature_window), 100) 
        
    def switch_ON_thermoelectric_cooler(self):

        self.run_command_on_module("m?", 100) # Not implemented yet

    def switch_OFF_thermoelectric_cooler(self):

        self.run_command_on_module("m?", 100) # Not implemented yet

    def clear_the_error_registor_on_module(self):
        
        self.run_command_on_module("c", 100)

    def get_thermoelectric_cooler_current_limit(self):

        return self.run_command_on_module("L?", 100)

    def get_thermoelectric_cooler_current_actual(self):

        return self.run_command_on_module("A?", 100)

    def get_thermoelectric_cooler_voltage_actual(self):

        return self.run_command_on_module("U?", 100)

    def get_temperature_setpoint(self):

        return self.run_command_on_module("T?", 100)

    def get_temperature_actual(self):

        return self.run_command_on_module("Te?", 100)

    def get_stable_temperature_window(self):

        return self.run_command_on_module("W?", 100)    

    def get_temperature_stabilization_module_model(self):

        return self.run_command_on_module("m?", 100)    

    def get_temperature_stabilization_module_ID(self):

        return self.run_command_on_module("u?", 100)

    def get_PID_loop_cycle_time(self):

        return self.run_command_on_module("C?", 100)

    def get_module_status_full(self):

        pid_values = self.get_PID_values()
        print("MINIATURE LASER DIODE CONTROLLER  ("+self.get_temperature_stabilization_module_model()+")\n")
        print("PID values: P =\t\t{} mA/K\tI =\t{} mA/Ks\tD =\t{} mAs/K".format(pid_values[0], pid_values[1], pid_values[2]))
        print("PID loop cycle time:\t{} ms\t| Temperature window: {} °C".format(float(self.get_PID_loop_cycle_time()), float(self.get_stable_temperature_window())/1000))
        print("TEC current limit:\t{} A\t| Actual TEC current: {} A\t| TEC voltage: {} V".format(float(self.get_thermoelectric_cooler_current_limit())/1000, float(self.get_thermoelectric_cooler_current_actual())/1000, float(self.get_thermoelectric_cooler_voltage_actual())/1000))        
        self.get_module_status_temperature()

    def get_module_status_temperature(self):

        print("Temperature setpoint:\t{} °C\t| Actual Temperature: {} °C".format(float(self.get_temperature_setpoint())/1000, float(self.get_temperature_actual())/1000))        

    def get_module_status_actual_temperature(self):

        print("Actual Temperature: {} °C".format(float(self.get_temperature_actual())/1000))        


temp_controller_module = MTD415T_temperature_stabilization_module()

temp_controller_module.set_PID_loop_cycle_time(5) # loop cycle time in milliseconds
temp_controller_module.set_PID_values(800, 500, 20)
temp_controller_module.set_temperature(25000)  #14444 for methane line
temp_controller_module.set_thermoelectric_cooler_current_limit(1200)
#temp_controller_module.get_temperature_status_LED_delay())
#print(temp_controller_module.run_command_on_module_fast("u?", 100))
temp_controller_module.set_stable_temperature_window(10)
temp_controller_module.set_temperature_status_LED_delay(1)

temp_controller_module.get_module_status_full()

while(True):
    temp_controller_module.get_module_status_actual_temperature()
    time.sleep(1)

