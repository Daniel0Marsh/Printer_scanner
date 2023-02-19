import threading
import socket
import subprocess
import queue
from tqdm import tqdm

# Define the IP range to scan
default_ip_range = "192.168.1.1/24"
ip_range = input(f"Enter the IP range to scan (default: {default_ip_range}): ") or default_ip_range

# Define the command to get printer information
printer_cmd = "lpinfo -v"

# Define the queue to hold the IP addresses that need to be scanned
queue = queue.Queue()

# Add all of the IP addresses in the specified range to the queue
for ip in ip_range.split("."):
    if "/" in ip:
        # This is the subnet mask - add all possible values to the queue
        for i in range(int(ip.split("/")[1])):
            queue.put(".".join(ip_range.split(".")[:3] + [str(i)]))
    else:
        queue.put(ip)

# Define a lock to synchronize access to the console output
print_lock = threading.Lock()

# Define a list to hold the printer information
printers = []

# Define a function to scan a single IP address and check for printer information
def scan_ip_address(ip):
    # Create a socket to connect to the IP address on port 9100 (the default port for network printers)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(1)
    try:
        result = sock.connect_ex((ip, 9100))
        if result == 0:
            # The IP address is in use, so try to get printer information
            with print_lock:
                print(f"Scanning {ip}...")
            proc = subprocess.Popen(printer_cmd.split(), stdout=subprocess.PIPE)
            output = proc.communicate()[0].decode("utf-8")
            for line in output.split("\n"):
                if line.startswith("network") and ip in line:
                    # This line contains printer information for the specified IP address
                    printer_name = line.split()[1]
                    with print_lock:
                        print(f"Found printer {printer_name} at {ip}")
                    printers.append((printer_name, ip))
    except socket.error:
        pass
    finally:
        sock.close()

# Define a function to run in each thread, which dequeues IP addresses and scans them
def thread_function(pbar):
    while True:
        ip = queue.get()
        if ip is None:
            # This is a sentinel value indicating that there are no more IP addresses to scan
            break
        scan_ip_address(ip)
        queue.task_done()
        pbar.update(1)

# Define the number of threads to use
num_threads = 20

# Start the threads
threads = []
with tqdm(total=queue.qsize(), desc="Scanning IP addresses") as pbar:
    for i in range(num_threads):
        thread = threading.Thread(target=thread_function, args=(pbar,))
        thread.start()
        threads.append(thread)

    # Wait for all of the IP addresses to be scanned
    queue.join()

    # Add sentinel values to the queue to tell the threads to exit
    for i in range(num_threads):
        queue.put(None)

    # Wait for all of the threads to exit
    for thread in threads:
        thread.join()

# Write the printer information to a file
with open("printers.txt", "w") as f:
    for printer in printers:
        f.write(f"{printer[0]}\t{printer[1]}\n")

# Print a message indicating that the scan is complete
print("Scan complete! Printer information saved to printers")
