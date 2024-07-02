import pexpect
from utils.parse_onu_list import parse_onu_file

def save_onu_list(output):
    try:
        with open("ONU_LIST", "a") as f:
            f.write("\n")
            f.write(output)
            return True
    except Exception as error:
        print(f"There was an a error: \n {error}")

def list_onus(proc):
    try:
        proc.sendline("sh gpon onu unconfi")
        proc.expect(r"#")
        output = proc.before.decode('utf-8')
        try :
            save_onu_list(output)
        except Exception as error:
            print(f"There was an a error: \n {error}")
    except Exception as error:
        print(f"There was an a error: \n {error}")
    try :
        onu_list = parse_onu_file("ONU_LIST")
        return onu_list
    except Exception as error:
        print(f"There was an a error: \n {error}")
    
