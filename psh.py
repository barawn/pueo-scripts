#!/usr/bin/env python3

import cmd
import argparse
import os.path
import sys
from functools import partial

try:
    import readline
except ImportError:
    readline = None

from pueo.common.term import Term
from HskSerial import HskEthernet, HskSerial, HskPacket

histfile = os.path.expanduser('~/.psh_history')
histfile_size = 1000

# argument this
hsk = HskEthernet()

class HskShell(cmd.Cmd):
    TITLE = 'PUEO Housekeeping Shell'
    
    PREFIX = Term.CURSOR_SAVE + Term.CURSOR_POS(1,1) + Term.BLACK + Term.BG_WHITE
    POSTFIX = Term.END + Term.CURSOR_RESTORE

    @property
    def prompt(self):
        sz = os.get_terminal_size()
        width = sz.columns
        prefill = width//2 - len(self.TITLE)//2
        postfill = width - len(self.TITLE) - prefill
        return self.PREFIX + ' '*prefill + self.TITLE + ' '*postfill + self.POSTFIX + f'HSK ({self.target})> '
    
    def preloop(self):        
        if readline and os.path.exists(histfile):
            readline.read_history_file(histfile)

        print(Term.CLEAR_SCREEN)


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
        ll = argline.lstrip(' ').split(' ')
        if ll[0] == 'target':
            self.target = ll[1]

    def __init__(self):
        self.target = None
        # get list of commands
        cmds = list(HskPacket.cmds.keys())
        # remove eError
        cmds.remove('eError')
        # patch in all of them that might not have a definition
        for key in HskPacket.cmds.keys():
            if not getattr(self, f'do_{key}', None):
                f = partial(self._basic_command, cmd=key)
                f.__doc__ = HskPacket.cmds[key][1]
                setattr(HskShell, f'do_{key}', f)
            else:
                pass
            
        super().__init__()
        
        
    def do_eIdentify(self, argline:str):
        if self.target:
            addr = int(self.target, 0)
            hsk.send(HskPacket(addr, 'eIdentify'))
            pkt = self.try_receive()
            if pkt:
                print(pkt.pretty(asString=True))

    def do_eTemps(self, argline:str):
        if self.target:
            addr = int(self.target, 0)
            hsk.send(HskPacket(addr, 'eTemps'))
            pkt = self.try_receive()
            if pkt:
                print(pkt.pretty())

    def do_eCurrents(self, argline:str):
        if self.target:
            addr = int(self.target, 0)
            hsk.send(HskPacket(addr, 'eCurrents'))
            pkt = self.try_receive()
            if pkt:
                print(pkt.pretty())                
                
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

    def _basic_command(self, argline:str, cmd=None):
        """ this is the base method used for basic commands """
        if self.target:
            addr = int(self.target, 0)
            args = argline.lstrip(' ')
            if len(args):
                data = list(map(lambda x : int(x,0), args.split(' ')))
            else:
                data = None
            hsk.send(HskPacket(addr, cmd, data=data))
            pkt = self.try_receive()
            if pkt:
                print(pkt.pretty())
                
if __name__ == "__main__":
    sz = os.get_terminal_size()
          
    shell = HskShell()
            
    shell.cmdloop()

