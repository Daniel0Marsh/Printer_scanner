# Printer Scanner

This Python script scans a specified IP range to find network printers and saves the printer information to a file named printers.txt. The script uses multithreading to improve performance by scanning multiple IP addresses simultaneously.

# How to use

1. Install the required packages:

`pip install tqdm`

2. Run the script:

`python printer_scanner.py`


By default, the script scans the IP range 192.168.1.1/24. You can specify a different IP range by entering it when prompted.

3. Wait for the scan to complete. The script will display a progress bar indicating the number of IP addresses scanned and the number of printers found.
4. Once the scan is complete, the printer information will be saved to a file named  `printers.txt` in the same directory as the script.

# Explanation of the code

The script performs the following steps:

1. The script prompts the user to enter the IP range to scan. If no range is entered, the default range 192.168.1.1/24 is used.

2. The script defines the command to get printer information and a queue to hold the IP addresses that need to be scanned.

3. The script adds all of the IP addresses in the specified range to the queue.

4. The script defines a lock to synchronize access to the console output, a list to hold the printer information, and a function to scan a single IP address and check for printer information.

5. The script defines a function to run in each thread, which dequeues IP addresses and scans them.

6. The script starts the specified number of threads and waits for all of the IP addresses to be scanned.

7. The script adds sentinel values to the queue to tell the threads to exit and waits for all of the threads to exit.

8. The script writes the printer information to a file named printers.txt.

9. The script prints a message indicating that the scan is complete.

The script uses the 'socket' and 'subprocess' modules to scan the specified IP addresses and get printer information, respectively. The`queue` and `threading` modules are used to implement multithreading and improve performance. The `tqdm` module is used to display a progress bar during the scan.

In summary, the script is a simple but effective tool to quickly scan a network for network printers and retrieve their IP addresses and names.
