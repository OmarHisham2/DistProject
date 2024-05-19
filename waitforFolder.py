import os
import time

import cv2
import ImageTech as imgtech
# Function to get list of files in a directory
def get_files(directory):
    return os.listdir(directory)

# Directory to monitor
directory_to_watch = 'D:/Dist Repo/DistProject'

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
        for file in new_files:
            id = file.split(".")[0] 
            if file.endswith(".txt"):
                with open(file,'r') as file:
                    techToApply = file.read()
                    file.close()
            elif ( ( file.endswith(".jpg")) or (file.endswith(".png")) or ( file.endswith(".jpeg")) ):
                if techToApply != None:
                    img = cv2.imread(file,0)
                    resultingImage = imgtech.ApplyTechnique(img,techToApply)
                    cv2.imwrite(id+"_fixed.png",resultingImage)
                    print('Image has been fixed')
                    break
    
    # Update initial list for the next iteration
    initial_files = current_files
    
    # Add a delay before checking again
    time.sleep(1)