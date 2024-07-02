import pexpect
import signal
import argparse
import time
import utils.basic_commands as bc
import utils.debug_watcher as dl
import utils.get_onus as gt
import utils.parse_onu_list as onu_parse

TELNET_USER = 'admin'
TELNET_PWD = 'parks'
TELNET_PORT = 23
DEFAULT_DURATION = 172800 # 48hours, two days sending requests.
DEFAULT_INTERVAL = 3 # 30 seconds between each request. 


signal.signal(signal.SIGINT, bc.handle_ctrl_c)

def list_onus(args):
    ###WORKING IN PROGRESS
    proc = pexpect.spawn(f"telnet {args.host} {args.telnet_port}")
    if (bc.login_OLT(proc, args)):
        gt.list_onus(proc)
        onu_parse.parse_onu_file("ONU_LIST")
            

def show_memory(proc, args):
        command = "sh me"
        filename = "sh_me_output.txt"
        bc.send_command(proc, command, filename)
        proc.close()
        time.sleep(int(args.interval))

def show_cpu(proc, args):
        command = "sh cpu"
        filename = "sh_cpu_output.txt"
        bc.send_command(proc, command, filename)
        proc.close()
        time.sleep(int(args.interval))
   
def run_watcher_mode_basic(args):
    start_time = time.time() 
    end_time = start_time + args.duration

    while time.time() < end_time:
        proc = pexpect.spawn(f"telnet {args.host} {args.telnet_port}")
        if (bc.login_OLT(proc, args)):
        
            (command_function := bc.save_config if args.Type == 'save_config' else 
                                 show_cpu if args.Type == 'show_cpu' else 
                                 show_memory if args.Type == 'show_memory' else 
                                 (lambda proc, args: print("Invalid command type specified.")))(proc, args)

def main():
    parser = create_parser()
    args = parser.parse_args()
    if args.Type == 'debug_listener':
        dl.debug_listener(args)
    elif args.Type == 'get_onus':
        list_onus(args)
    else:
        run_watcher_mode_basic(args)

def create_parser():
    parser = argparse.ArgumentParser()
    parser.formatter_class = lambda prog: argparse.RawTextHelpFormatter(prog, max_help_position=30)
    parser.add_argument('-H', '--host', help='Host', required=True)
    parser.add_argument('-u','--telnet-user', help='Telnet user', default=TELNET_USER)
    parser.add_argument('-t','--telnet-port', help='Telnet Port', default=TELNET_PORT)
    parser.add_argument('-p','--telnet-password', help='Telnet Password', default=TELNET_PWD)
    parser.add_argument('-i','--interval', help='Interval, in seconds.', default=DEFAULT_INTERVAL)
    parser.add_argument("-d", "--duration", help="Duration of requests ", type=int, default= DEFAULT_DURATION)
    parser.add_argument('-f', '--file', help='File with command list.')
    parser.add_argument('-T','--Type', help='''Changes the command sent to the device. 
    Options: 
            -show_memory  
            -show_cpu      
            -save_config
            -debug_listener''', default='save_config')
    return parser

if __name__ == "__main__":
    main()
 