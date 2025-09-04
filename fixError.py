import sys
import ..pueo-utils.HskSerial.HskSerial import HskEthernet, HskPacket
def handle_error(code):
    hsk = HskEthernet()
    if code == 1:
        print("Handling GTP link 0 error: Restarting GTP interface...")
        hsk.send(HskPacket(0x58, 'eReloadFirmware', data=[0,0,0,0]))
    elif code ==2: 
        print("Handling GTP link 1 error: Restarting GTP interface...")
        hsk.send(HskPacket(0x50, 'eReloadFirmware', data=[0,0,0,0]))
    elif code ==3: 
        print("Handling GTP link 2 error: Restarting GTP interface...")
        hsk.send(HskPacket(0x40, 'eReloadFirmware', data=[0,0,0,0]))
    elif code ==23: 
        print("Handling GTP link 3 error: Restarting GTP interface...")
        hsk.send(HskPacket(0x48, 'eReloadFirmware', data=[0,0,0,0]))
    elif code == 99:
        print("General command failure: Logging and alerting...")
        # Add your actual fix logic here
    else:
        print(f"Unknown error code: {code}. No action taken.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 fix_error.py <error_code>")
        sys.exit(1)
    try:
        error_code = int(sys.argv[1])
        handle_error(error_code)
    except ValueError:
        print("Error: Invalid error code. Must be an integer.")
        sys.exit(1)