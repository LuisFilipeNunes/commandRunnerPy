import pexpect
import argparse
import logging
import time

TELNET_USER = 'admin'
TELNET_PWD = 'parks'
TELNET_PORT = 23
INTERVAL = 30
logfile = open('/tmp/telnet_log.txt', 'wb')



def save_results(filename, output):
    # Save the output with timestamp to a text file, in append mode. 
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    with open(filename, "a") as f:
        f.write(f"Timestamp: {timestamp}\n\n")
        f.write(output)
        
def show_memory(proc, args):
        command = "sh me"
        filename = "sh_me_output.txt"
        proc.sendline(command)
        proc.expect(r"#")
        output = proc.before.decode('utf-8')

        save_results(filename, output)
        
        proc.close()
        time.sleep(int(args.interval))

def show_cpu(proc, args):
        command = "sh cpu"
        filename = "sh_cpu_output.txt"
        proc.sendline(command)
        proc.expect(r"#")
        output = proc.before.decode('utf-8')

        save_results(filename, output)
        proc.close()
        time.sleep(int(args.interval))

def save_config(proc, args):
        save_interval = 86400
        if args.interval != 30:
            save_interval = int(args.interval)
        command = "copy r s"
        filename = "save_config.txt"
        proc.sendline(command)
        proc.expect(r"#")
        output = proc.before.decode('utf-8')

        save_results(filename, output)
        proc.close()
        time.sleep(save_interval)

def run(args):
    start_time = time.time() 
    end_time = start_time + 48 * 3600 # 48hours from start_time

    while time.time() < end_time:
        try:
            proc = pexpect.spawn(f"telnet {args.host} {args.telnet_port}")
            proc.logfile = logfile
            proc.expect('Press <RETURN> to get started')
            proc.sendline("\r")
            proc.expect("Username:")
            proc.sendline(args.telnet_user)
            proc.expect("Password:")
            proc.sendline(args.telnet_password)
            proc.expect(r"#")

            (command_function := save_config if args.Type == 'save_config' else 
                                 show_cpu if args.Type == 'show_cpu' else 
                                 show_memory if args.Type == 'show_memory' else 
                                 (lambda proc, args: print("Invalid command type specified.")))(proc, args)
        except Exception as error:
            logging.exception(f"An error ocurred: {error}")

def main():
    parser = create_parser()
    args = parser.parse_args()
    run(args)

def create_parser():
    parser = argparse.ArgumentParser()
    parser.formatter_class = lambda prog: argparse.RawTextHelpFormatter(prog, max_help_position=30)
    parser.add_argument('-H', '--host', help='Host', required=True)
    parser.add_argument('-u','--telnet-user', help='Telnet user', default=TELNET_USER)
    parser.add_argument('-t','--telnet-port', help='Telnet Port', default=TELNET_PORT)
    parser.add_argument('-p','--telnet-password', help='Telnet Password', default=TELNET_PWD)
    parser.add_argument('-i','--interval', help='Interval, in seconds.', default=INTERVAL)
    parser.add_argument('-T','--Type', help='''Changes the command sent to the device. 
    Options: 
            -show_memory  
            -show_cpu      
            -save_config''', default='save_config')
    return parser

if __name__ == "__main__":
    main()
