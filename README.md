# Telnet Command Runner

This Python script enables the execution of Telnet commands on a remote device and saves the output to files with timestamps. It offers functionalities to display memory and CPU usage, as well as to save configurations.

## Features

    Execute Telnet commands on a remote device.
    Save the output of commands with timestamps.
    Support for displaying memory and CPU usage.
    Option to save device configurations periodically.

## Usage

    Execution:
        Run the script with the required arguments:


        python3 command_runner.py -H <host> [-u <telnet_user>] [-t <telnet_port>] [-p <telnet_password>] [-i <interval>] [-T <Type>]

    
    Arguments:
        -H, --host: Specifies the host IP address.
        -u, --telnet-user: Sets the Telnet username (default: admin).
        -t, --telnet-port: Specifies the Telnet port (default: 23).
        -p, --telnet-password: Sets the Telnet password (default: parks).
        -i, --interval: Sets the interval for saving configurations, in seconds (default: 30).
        -T, --Type: Changes the type of command sent to the device (default: save_config). Options: show_memory, show_cpu, save_config.

## Example

To run the script and save CPU usage information:
```shell

python3 command_runner.py -H 192.168.1.100 -u admin -t 23 -p parks -i 60 -T show_cpu
```


### Notes

    Output files are saved with timestamps.
    The script uses the pexpect library for handling Telnet interactions.
    It supports basic error handling and logging.
    Ensure proper permissions and network access for Telnet communication.