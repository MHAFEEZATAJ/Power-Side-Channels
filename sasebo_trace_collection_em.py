import numpy as np
import sys
import ftd2xx
import time
import random
import win32com.client

def log_hex(data):
    """Helper function to format byte data as hex string."""
    return '-'.join(f'{b:02X}' for b in data)

def generate_random_np_array(UL,size):
    """To create a numpy array\n.
       1. Based on the number of bits being operated, UL corresponds to the upper limit
       2. size is the size of the array"""
    return np.random.randint(0, 256, size=16)

def get_user_input():
    """Function to take key inputs as a single string."""
    key_input = input("Enter 16 hex values for the key (e.g., 0x01 0x4E 0x4A ...): ")
    # Split the input string and convert each hex value to integer
    key_values = [int(x, 16) for x in key_input.split()]
    if len(key_values) != 16:
        raise ValueError("You must enter exactly 16 hex values.")
    return key_values


def main():

    numtraces=int(input("Enter number of traces"))
    scope = win32com.client.Dispatch("LeCroy.ActiveDSOCtrl.1")
    #scope.MakeConnection("IP:10.21.234.70")
    scope.MakeConnection("IP:169.254.196.20")
    scope.WriteString("buzz beep", 1)
    #scope.WriteString(r"""vbs 'return=app.saverecall.setup.recallfrom = "file" ' """, 1)
    #print(scope.ReadString(10000))
    scope.WriteString(r"""vbs 'app.acquisition.triggermode = "auto" ' """, 1)
    print("Connected to DSO")

    # Open the FTDI device
    devices = ftd2xx.listDevices()
    #print(f"Number of FTDI devices: {len(devices)}")

    if not devices:
        print("No FTDI devices found.")
        return
            
    # Open the first FTDI device
    dev = ftd2xx.open(0)

    print(f"FTDI device opened: {devices[0]}")

    try:
        for i in range(numtraces):
            print(f"Trace Number {i}")        
            # Get user input for key values
            #user_key = get_user_input()
            user_key = [0x01, 0x4E, 0x4A, 0x4C, 0x4E, 0x4A, 0x4C, 0x4E, 0x4A, 0x4C, 0x4E, 0x4A, 0x4C, 0x4E, 0x4A, 0x4C] 
            k1, k2, k3, k4, k5, k6, k7, k8 = user_key[:8]
            k9, k10, k11, k12, k13, k14, k15, k16 = user_key[8:]

            # Writing to address 0002 with data 0004
            write_data_1 = [0x01, 0x00, 0x02, 0x00, 0x04]
            #print(f"Writing to address 0002 with data 0004: {write_data_1}")
            dev.write(bytes(write_data_1))
            # print(f"Written {len(write_data_1)} bytes to FTDI: {log_hex(write_data_1)}")

            # Writing to address 0002 with data 0000
            write_data_2 = [0x01, 0x00, 0x02, 0x00, 0x00]
            #print(f"Writing to address 0002 with data 0000: {write_data_2}")
            dev.write(bytes(write_data_2))
            # print(f"Written {len(write_data_2)} bytes to FTDI: {log_hex(write_data_2)}")

            # Plaintext with user key values
            key_from_user = [
                0x01, 0x01, 0x00, k1, k2, 0x01, 0x01, 0x02,
                k3, k4, 0x01, 0x01, 0x04, k5, k6, 0x01,
                0x01, 0x06, k7, k8, 0x01, 0x01, 0x08, k9,
                k10, 0x01, 0x01, 0x0A, k11, k12, 0x01, 0x01,
                0x0C, k13, k14, 0x01, 0x01, 0x0E, k15, k16
            ]
            #print(f"Writing user key to FTDI: {key_from_user}")
            dev.write(bytes(key_from_user))
            # print(f"Written {len(key_from_user)} bytes to FTDI: {log_hex(key_from_user)}")

            # Writing to address 0002 with data 0002
            write_data_3 = [0x01, 0x00, 0x02, 0x00, 0x02]
            #print(f"Writing to address 0002 with data 0002: {write_data_3}")
            dev.write(bytes(write_data_3))
            # print(f"Written {len(write_data_3)} bytes to FTDI: {log_hex(write_data_3)}")

            # Writing more data
            write_data_4 = [0x00, 0x00, 0x02]
            #print(f"Writing to FTDI: {write_data_4}")
            dev.write(bytes(write_data_4))
            # print(f"Written {len(write_data_4)} bytes to FTDI: {log_hex(write_data_4)}")

            # Reading response
            response_1 = dev.read(2)
            #print(f"Read 2 bytes from FTDI: {log_hex(response_1)}")

            # Generate random values for p1 to p16
            pt_int = generate_random_np_array(255,16)
            

            # Add the p1 p2 p3 ... p16 to a list
            
                    
            # Modify the plaintext with random hex values
            plaintext_2 = [
                0x01, 0x01, 0x40, pt_int[0], pt_int[1], 0x01, 0x01, 0x42,
                pt_int[2], pt_int[3], 0x01, 0x01, 0x44, pt_int[4], pt_int[5], 0x01,
                0x01, 0x46, pt_int[6], pt_int[7], 0x01, 0x01, 0x48, pt_int[8],
                pt_int[9], 0x01, 0x01, 0x4A, pt_int[10], pt_int[11], 0x01, 0x01,
                0x4C, pt_int[12], pt_int[13], 0x01, 0x01, 0x4E, pt_int[14], pt_int[15]
            ]
            #print(f"Writing modified plaintext to FTDI: {plaintext_2}")
            dev.write(bytes(plaintext_2))
            # print(f"Written {len(plaintext_2)} bytes to FTDI: {log_hex(plaintext_2)}")

            # Start cipher processing
            #print("Starting cipher processing...")
            
            # Write to address 0002 with data 0001
            write_data_5 = [0x01, 0x00, 0x02, 0x00, 0x01]
            #print(f"Writing to address 0002 with data 0001: {write_data_5}")
            dev.write(bytes(write_data_5))
            #print(f"Written {len(write_data_5)} bytes to FTDI: {log_hex(write_data_5)}")

            # Writing more data
            write_data_6 = [0x00, 0x00, 0x02]
            # print(f"Writing to FTDI: {write_data_6}")
            dev.write(bytes(write_data_6))
            # print(f"Written {len(write_data_6)} bytes to FTDI: {log_hex(write_data_6)}")

            # Reading response
            response_2 = dev.read(2)
            #print(f"Read 2 bytes from FTDI: {log_hex(response_2)}")

            # Final writes after cipher processing
            final_data = [
                0x00, 0x01, 0x80, 0x00, 0x01, 0x82, 0x00, 0x01,
                0x84, 0x00, 0x01, 0x86, 0x00, 0x01, 0x88, 0x00,
                0x01, 0x8A, 0x00, 0x01, 0x8C, 0x00, 0x01, 0x8E
            ]
            # print(f"Writing final data to FTDI: {final_data}")
            dev.write(bytes(final_data))
            # print(f"Written {len(final_data)} bytes to FTDI: {log_hex(final_data)}")

            # Reading final response
            response_3 = dev.read(16)
            #print(f"Read 16 bytes from FTDI: {log_hex(response_3)}")
            #print(type(response_3))
            #print(list(response_3))
            ct_int=np.array(list(response_3))
            print(ct_int)

            print("Starting Acquisition")
            scope.WriteString(r"""vbs 'app.acquisition.triggermode = "normal" ' """, 1)
            #scope.WriteString(r"""vbs? 'return=app.acquisition.triggermode' """, 1)
            #print(scope.ReadString(10000))
            #scope.WriteString(r"""vbs? 'return=app.acquisition.triggermode' """, 1)
            val=[]
            val = np.array(scope.GetIntegerWaveform("C3", 13000, 0))
            # print(type(scope.GetNativeWaveform("C1", 13000, 0)))
            # val=scope.ReadString(100000)
            pt_int = np.array(pt_int).flatten()
            val = np.array(val).flatten()
            ct_int = np.array(ct_int).flatten()
            user_key = np.array(user_key).flatten()
            print(user_key)
            print(pt_int)
            print(val)
            #print(val)
            #print(ct_int)

            #output = np.vstack([pt_int, val, ct_int, user_key])
            np.savez("enc{}.npz".format(i), pt_int=pt_int, ct_int=ct_int, trace=val, user_key=user_key)

            #np.save("enc{}.npy".format(str(i)),output)
            # filename = str(i)+".txt"
            # print(val)
            # print(i,len(val),type(val))
            
            # with open(filename,'w+')as f:
            #     for i in val:
            #         f.write(str(i))
            #         f.write("\n")
        
    finally:
    # Close the FTDI device
        dev.close()
        print("FTDI device closed.")
        scope.Disconnect()
if __name__ == "__main__":
    main()
