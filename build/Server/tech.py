

import threading
import queue
import cv2 # OpenCV for image processing
from mpi4py import MPI # MPI for distributed computing

"""
Image Techniques To Apply
"""

def edgeDetection(img): # Canny
    return cv2.Canny(img,100,200)
    

def colorInversion(img):
    return cv2.bitwise_not(img)

def convertToGray(img):
    return cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

def applyBlurring(img):
    return cv2.blur(img,(5,5))

def applyGaussianBlur(img):
    return cv2.GaussianBlur(img,(5,5),3)

def ApplyTechnique(img,method):

    if method == "edgeDetection":
        return edgeDetection(img.copy())

    elif method == "colorInversion":
        return colorInversion(img.copy())

    elif method == "convertToGray":
        return convertToGray(img.copy())
    
    elif method == "applyBlurring":

        return applyBlurring(img.copy())

    elif method == "applyGaussianBlur":
        return applyGaussianBlur(img.copy())

    else:
        print(f"Technique '{method}' not found.")


class WorkerThread(threading.Thread):
    def __init__(self, task_queue):
        threading.Thread.__init__(self)
        self.task_queue = task_queue
        self.comm = MPI.COMM_WORLD
        self.rank = self.comm.Get_rank()

    def run(self):
        while True:
            task = self.task_queue.get()
            if task is None:
                break
            image, operation = task
            result = self.process_image(image, operation)
            self.send_result(result)

    def process_image(self, image, operation):
        # Load the image
        img = cv2.imread(image, cv2.IMREAD_COLOR)
        # Perform the specified operation
        result = ApplyTechnique(img,operation)
        return result
    
    def send_result(self, result):
        # Send the result to the master node
        self.comm.send(result, dest=0)
        # Create a queue for tasks

task_queue = queue.Queue()
# Create worker threads
for i in range(MPI.COMM_WORLD.Get_size() - 1):
    WorkerThread(task_queue).start()
