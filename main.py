import threading
from ui import run
from cloudloop2 import run2
big_queue=queue.Queue()
big_queue2=queue.Queue()

def main():
    ui_thread=threading.Thread(run(800,600))
    camera_thread=threading.Thread(run2())
    
    ui_thread.start()
    camera_thread.start()
    ui_thread.join()
    camera_thread.join()
main()