#!/usr/bin/env python3

import cmd
import argparse
import os.path

try:
    import readline
except ImportError:
    readline = None
    
from HskSerial import HskEthernet, HskSerial, HskPacket

histfile = os.path.expanduser('~/.psh_history')
histfile_size = 1000

# argument this
hsk = HskEthernet()

class HskShell(cmd.Cmd):
    prompt = f'HSK (None)> '
    def preloop(self):
        if readline and os.path.exists(histfile):
            readline.read_history_file(histfile)

    def postloop(self):
        if readline:
            readline.set_history_length(histfile_size)
            readline.write_history_file(histfile)
            
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

    # I need to parse the available HskPackets and
    # automatically build a dumb version of this for
    # ones that aren't already defined.
    # do_eEnable is probably the default for that.
        
    def do_eEnable(self, argline:str):
        if self.target:
            addr = int(self.target, 0)
            args = argline.lstrip(' ')
            if len(args):
                data = list(map(lambda x : int(x,0), args.split(' ')))
            else:
                data = None
            hsk.send(HskPacket(addr, 'eEnable', data=data))
            pkt = self.try_receive()
            if pkt:
                print(pkt.pretty())

    def do_eRestart(self, argline:str):
        if self.target:
            addr = int(self.target, 0)
            args = argline.lstrip(' ')
            if len(args):
                data = list(map(lambda x : int(x,0), args.split(' ')))
            else:
                data = None
            hsk.send(HskPacket(addr, 'eRestart', data=data))
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

    def do_eStartState(self, argline:str):
        if self.target:
            addr = int(self.target, 0)
            if len(argline):
                data = int(argline, 0)
            else:
                data = None
            hsk.send(HskPacket(addr, 'eStartState', data=data))
            pkt = self.try_receive()
            if pkt:
                print(pkt.pretty())
                
if __name__ == "__main__":
    HskShell().cmdloop()

