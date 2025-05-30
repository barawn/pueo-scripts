#!/usr/bin/env python3

import cmd
import argparse
    
from HskSerial import HskEthernet, HskSerial, HskPacket

# argument this
hsk = HskEthernet()

class HskShell(cmd.Cmd):
    prompt = f'HSK (None)> '
    def try_receive(self):
        try:
            pkt = hsk.receive()
            return pkt
        except KeyboardInterrupt:
            print('Interrupted')
            return None
        

    def do_quit(self, argline:str) -> bool:
        return self.do_exit(argline)

    def do_exit(self, argline:str) -> bool:
        return True

    def do_shell(self, argline:str):
        self.target = argline
        self.prompt = f'HSK ({self.target})> '

    def do_eEnable(self, argline:str):
        if self.target:
            addr = int(self.target, 0)
            data = list(map(lambda x : int(x,0), argline.split(' ')))
            hsk.send(HskPacket(addr, 'eEnable', data=data))
            pkt = self.try_receive()
            if pkt:
                print(pkt.pretty())

    def do_eIdentify(self, argline:str):
        if self.target:
            addr = int(self.target, 0)
            hsk.send(HskPacket(addr, 'eIdentify'))
            pkt = self.try_receive()
            if pkt:
                print(pkt.pretty(asString=True))
                
    def do_ePingPong(self, argline:str):
        if self.target:
            addr = int(self.target, 0)
            hsk.send(HskPacket(addr, 'ePingPong', data=argline))
            pkt = self.try_receive()
            if pkt:
                print(pkt.pretty(asString=True))
                
    def do_eFwNext(self, argline:str):
        if self.target:
            addr = int(self.target, 0)
            if len(argline):
                data = argline
            else:
                data = None
            hsk.send(HskPacket(addr, 'eFwNext', data=data))
            pkt = self.try_receive()
            if pkt:
                print(pkt.pretty(asString=True))

    def do_eSoftNext(self, argline:str):
        if self.target:
            addr = int(self.target, 0)
            if len(argline):
                data = argline
            else:
                data = None
            hsk.send(HskPacket(addr, 'eSoftNext', data=data))
            pkt = self.try_receive()
            if pkt:
                print(pkt.pretty(asString=True))
                
if __name__ == "__main__":
    HskShell().cmdloop()

