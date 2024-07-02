import pexpect
import time
import sys
import argparse
import utils.basic_commands as bc

TELNET_USER = 'admin'
TELNET_PWD = 'parks'
TELNET_PORT = 23
DEFAULT_DURATION = 172800 # 48hours, two days sending requests.

def debug_listener(args):

    child = pexpect.spawn(f"telnet {args.host} {args.telnet_port}")
    child.logfile = sys.stdout.buffer 
    start_time = time.time() 
    end_time = start_time + args.duration 
 
    
    while start_time < end_time:
        try:
            child.timeout = 10
            child.expect('Press <RETURN> to get started')
            child.sendline("\r")
            child.expect("Username:")
            child.sendline(args.telnet_user)
            child.expect("Password:")
            child.sendline(args.telnet_password)
            child.expect(r"#")
            child.sendline("terminal length 0")
            child.expect(r"#")
            child.sendline("debug gpon onu")
            child.expect(r"#")
            child.sendline("configure terminal")
            child.expect(r"#")
            child.sendline("logging terminal priority 7")
        except Exception as error:
            print(child.before.decode("utf-8"))
            pass

def main():
    parser = create_parser()
    args = parser.parse_args()
    debug_listener(args)

def create_parser():
    parser = argparse.ArgumentParser()
    parser.formatter_class = lambda prog: argparse.RawTextHelpFormatter(prog, max_help_position=30)
    parser.add_argument('-H', '--host', help='Host', required=True)
    parser.add_argument('-u','--telnet-user', help='Telnet user', default=TELNET_USER)
    parser.add_argument('-t','--telnet-port', help='Telnet Port', default=TELNET_PORT)
    parser.add_argument('-p','--telnet-password', help='Telnet Password', default=TELNET_PWD)
    parser.add_argument("-d", "--duration", help="Duration of requests ", type=int, default= DEFAULT_DURATION)
    return parser

if __name__ == "__main__":
    main()