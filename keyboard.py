import atexit
import sys
import termios
from select import select


class KBHit:
    def __init__(self):
        # Save the terminal settings
        self.fd = sys.stdin.fileno()
        self.new_term = termios.tcgetattr(self.fd)
        self.old_term = termios.tcgetattr(self.fd)

        # New terminal setting unbuffered
        self.new_term[3] = (self.new_term[3] & ~termios.ICANON & ~termios.ECHO)
        termios.tcsetattr(self.fd, termios.TCSAFLUSH, self.new_term)

        # Support normal-terminal reset at exit
        atexit.register(self.set_normal_term)


    def set_normal_term(self):
        '''Resets to normal terminal.'''
        termios.tcsetattr(self.fd, termios.TCSAFLUSH, self.old_term)


    def getch(self):
        '''
        Returns a keyboard character after kbhit() has been called.
        
        This should not be called in the same program as getarrow().
        '''
        return sys.stdin.read(1)


    def getarrow(self):
        '''
        Returns an arrow-key code after kbhit() has been called.

        Codes are:
        0: up
        1: right
        2: down
        3: left
        
        This should not be called in the same program as getch().
        '''
        c = sys.stdin.read(3)[2]
        vals = [65, 67, 66, 68]

        return vals.index(ord(c))


    def kbhit(self):
        ''' Returns True if keyboard character was hit, False otherwise.'''
        dr, _, _ = select([sys.stdin], [], [], 0)
        return dr != []