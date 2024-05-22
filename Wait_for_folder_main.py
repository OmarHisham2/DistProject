import os
import time
import cv2
import queue
from mpi4py import MPI
import ImageTech as imgtech
import stat

class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    RESET = '\033[0m'

class WorkerThread:
    def __init__(self, rank):
        self.rank = rank
        self.comm = MPI.COMM_WORLD

    def run(self):
        while True:
            try:
                print(f"Worker {self.rank} requesting task", flush=True)
                self.comm.send(None, dest=0, tag=0)
                task = self.comm.recv(source=0, tag=1)
                print(f"Worker {self.rank} received task: {task}", flush=True)

                if task is None:
                    print(f"Worker {self.rank} received shutdown signal", flush=True)
                    break

                result = self.process_task(task)
                self.send_result(result)
            except Exception as e:
                print(f"Worker {self.rank} encountered an error: {e}", flush=True)

    def process_task(self, task):
        try:
            image_path, technique = task
            print(f"Worker {self.rank} processing task: {task}", flush=True)
            img = cv2.imread(image_path, 0)
            resulting_image = imgtech.ApplyTechnique(img, technique)
            output_path = os.path.splitext(image_path)[0] + "_fixed.png"
            cv2.imwrite(output_path, resulting_image)
            print(f"Worker {self.rank} completed processing task: {task}", flush=True)
            return output_path
        except Exception as e:
            print(f"Worker {self.rank} encountered an error during processing: {e}", flush=True)
            return None

    def send_result(self, result):
        try:
            print(f"Worker {self.rank} sending result", flush=True)
            self.comm.send(result, dest=0, tag=2)
        except Exception as e:
            print(f"Worker {self.rank} encountered an error while sending result: {e}", flush=True)

def get_files(directory):
    return os.listdir(directory)

def check_file_permissions(file_path):
    file_stat = os.stat(file_path)
    permissions = oct(file_stat.st_mode)[-3:]
    owner = file_stat.st_uid
    group = file_stat.st_gid
    return permissions, owner, group

def change_permissions_recursive(directory):
    for root, dirs, files in os.walk(directory):
        for d in dirs:
            dir_path = os.path.join(root, d)
            os.chmod(dir_path, stat.S_IRUSR | stat.S_IWUSR | stat.S_IRGRP | stat.S_IROTH)
        for f in files:
            file_path = os.path.join(root, f)
            os.chmod(file_path, stat.S_IRUSR | stat.S_IWUSR | stat.S_IRGRP | stat.S_IROTH)

def main():
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()

    if rank == 0:
        task_queue = queue.Queue()
        directory_to_watch = '/home/mpiuser/cloud/'
        
        # Change permissions of the directory and its contents
        change_permissions_recursive(directory_to_watch)
        
        initial_files = get_files(directory_to_watch)
        technique = None

        print("Monitoring directory for file additions...")

        while True:
            current_files = get_files(directory_to_watch)
            new_files = [file for file in current_files if file not in initial_files]

            if new_files:
                for file in new_files:
                    file_path = os.path.join(directory_to_watch, file)
                    try:
                        print(f"Checking permissions for {file_path}")
                        permissions, owner, group = check_file_permissions(file_path)
                        print(f"Permissions: {permissions}, Owner: {owner}, Group: {group}")

                        if file.endswith(".txt"):
                            print(f"Trying to open {file_path}")
                            with open(file_path, 'r') as f:
                                technique = f.read().strip()
                                print(f"Technique read: {technique}")
                        elif file.endswith((".jpg", ".jpeg", ".png")) and technique is not None:
                            task_queue.put((file_path, technique))
                            print(f"Task added to queue: {file_path}, {technique}")
                    except PermissionError as e:
                        print(f"Permission denied: {e}")
                    except FileNotFoundError as e:
                        print(f"File not found: {e}")
                    except IOError as e:
                        print(f"IO error: {e}")
                    except Exception as e:
                        print(f"Unexpected error reading file {file_path}: {e}")

                initial_files.extend(new_files)

            while not task_queue.empty():
                task = task_queue.get()
                for worker_rank in range(1, size):
                    comm.send(task, dest=worker_rank, tag=1)
                    print(f"Master sent task to worker {worker_rank}: {task}", flush=True)

            while comm.Iprobe(source=MPI.ANY_SOURCE, tag=2):
                result = comm.recv(source=MPI.ANY_SOURCE, tag=2)
                print(f"Master received result from worker: {result}", flush=True)

            time.sleep(1)

    else:
        worker_thread = WorkerThread(rank)
        worker_thread.run()

    MPI.Finalize()

if __name__ == "__main__":
    main()
