import time

def save_results(filename, output):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    with open(filename, "a") as f:
        f.write("\n")
        f.write(f"Timestamp: {timestamp}\n\n")
        f.write(output)