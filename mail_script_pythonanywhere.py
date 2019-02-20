from flask import Flask, render_template, request
import threading
import time
import stock_library as SL

class Processer_thread(threading.Thread):
    #12 seconds is because QUANDL website supports only 5 calls per minute
    def __init__(self, name, interval=10):
        threading.Thread.__init__(self, name=name)
        self.interval = interval
        self.daemon = True
        self.start()

    def run(self):
        while True:
            SL.thread_fun()
            time.sleep(self.interval)

    
if __name__ == '__main__':
    thread_start = Processer_thread("READ_THREAD")
    while(True):
        time.sleep(1000)

