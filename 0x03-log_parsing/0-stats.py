#!/usr/bin/python3
"""Module containing script that reads stdin line by line and computes metrics."""
import sys
import signal

# Initialize a dictionary to store counts of status codes
status_codes = {"200": 0, "301": 0, "400": 0, "401": 0,
                "403": 0, "404": 0, "405": 0, "500": 0}
# Initialize a variable to store the total file size
total_size = 0
# Initialize a counter for the number of lines processed
line_count = 0

def print_stats():
    """Prints the accumulated metrics."""
    print("File size: {}".format(total_size))
    for key in sorted(status_codes.keys()):
        if status_codes[key] > 0:
            print("{}: {}".format(key, status_codes[key]))

try:
    for line in sys.stdin:
        # Split the line into parts
        parts = line.split()

        # Check if the line has at least 7 elements (IP, -, date, request method, URL, protocol, status code, file size)
        if len(parts) >= 7:
            # Attempt to extract the status code and file size
            try:
                status_code = parts[-2]
                file_size = int(parts[-1])
                total_size += file_size

                if status_code in status_codes:
                    status_codes[status_code] += 1

            except ValueError:
                continue  # If file size is not an integer, skip the line

            line_count += 1

            # Every 10 lines, print the statistics
            if line_count == 10:
                print_stats()
                line_count = 0

except KeyboardInterrupt:
    # In case of keyboard interruption (CTRL + C), print the statistics
    print_stats()
    raise

finally:
    # Always print the statistics when the program ends
    print_stats()

