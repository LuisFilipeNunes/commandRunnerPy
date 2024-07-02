import pexpect
import time
import sys
import utils.save_results as sr

SAVE_CONFIG_INTERVAL= 86400 

def handle_ctrl_c(sig, frame):
    print("\nProgram terminated by the user.")
    sys.exit(0)
        
def get_max_gpon_interfaces(model):
    gpon_models = {
        40000:16,
        30000:8
    }
    return gpon_models.get(model, 0)
    
def go_to_int_gpon(proc, model):
    for i in range(1, get_max_gpon_interfaces(model)):
        proc.sendline(f"int gpon {i}")
        proc.expect(r"#")
        time.sleep(1)
    pass
    
def go_to_configure_terminal(proc):
    proc.sendline("con t")
    proc.expect(r"#")
    return proc

def save_config(proc, args):
        save_interval = 86400
        if args.interval != 30:
            save_interval = int(args.interval)
        command = "copy r s"
        filename = "save_config.txt"
        proc.sendline(command)
        proc.expect(r"#")
        output = proc.before.decode('utf-8')

        sr.save_results(filename, output)
        proc.close()
        time.sleep(save_interval)


def send_command(proc, command, filename):
    try:
        proc.sendline(command)
        proc.expect(r"#")
        output = proc.before.decode('utf-8')
        sr.save_results(filename, output)
    except (pexpect.TIMEOUT, pexpect.EOF) as error:
        sr.save_results(filename, f"ERROR ------ No response from OLT.\n -------- Command sent: {command}")
        return

def save_config(proc, args):
        save_interval = SAVE_CONFIG_INTERVAL
        if args.interval != 30:
            save_interval = int(args.interval)
        command = "copy r s"
        filename = "save_config.txt"
        proc.sendline(command)
        proc.expect(r"#")
        output = proc.before.decode('utf-8')
        sr.save_results(filename, output)
        proc.close()
        time.sleep(save_interval)
        
def login_OLT(proc, args):
    try:
        proc.timeout = 10
        proc.expect('Press <RETURN> to get started')
        proc.sendline("\r")
        proc.expect("Username:")
        proc.sendline(args.telnet_user)
        proc.expect("Password:")
        proc.sendline(args.telnet_password)
        proc.expect(r"#")
        return True
    
    except Exception as error:
        print(f"There was an a error: \n {error}")