import os
import time

# Function to get list of files in a directory
def get_files(directory):
    return os.listdir(directory)

# Directory to monitor
directory_to_watch = 'D:/Downloads/DistProject/emad'

# Initial list of files
initial_files = get_files(directory_to_watch)

print("Monitoring directory for file additions...")

while True:
    # Get current list of files
    current_files = get_files(directory_to_watch)
    
    # Check for new files
    new_files = [file for file in current_files if file not in initial_files]
    
    # If new files found, print them
    if new_files:
        print("New file(s) added:")
        for file in new_files:
            print(file)
    
    # Update initial list for the next iteration
    initial_files = current_files
    
    # Add a delay before checking again
    time.sleep(1)