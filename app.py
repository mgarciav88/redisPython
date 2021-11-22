import multiprocessing
import queue
import time
from multiprocessing import Process
from threading import Thread

from flask import Flask

app = Flask(__name__)

memory_db = list()


@app.route('/')
def index():
    t = Thread(target=run_multi_process, args=(), kwargs={})
    t.start()
    return 'Web App with Python Flask!'


def run_multi_process():
    manager = multiprocessing.Manager()
    receive_queue = manager.Queue()
    out_queue = manager.Queue()

    num_consumers = multiprocessing.cpu_count()
    num_producers = multiprocessing.cpu_count()

    producers_process_list = list()
    for prod_num in range(num_producers):
        process = Process(target=producer, args=(prod_num, receive_queue,))
        process.start()
        producers_process_list.append(process)

    consumers_list = list()
    for cons_num in range(num_consumers):
        process = Process(target=consumer, args=(receive_queue, out_queue,))
        process.start()
        consumers_list.append(process)

    receive_queue.join()
    for process in producers_process_list:
        process.join()

    out_queue.join()
    for process in consumers_list:
        process.join()

    results = list()
    while not out_queue.empty():
        results.append(out_queue.get())
        out_queue.task_done()

    print(results)


def producer(prod_num, proc_queue: multiprocessing.Queue):
    # time.sleep(1)
    # r.lpush("Counter", prod_num)
    proc_queue.put(prod_num)


def consumer(in_queue: multiprocessing.Queue, out_queue: multiprocessing.Queue):
    while not in_queue.empty():
        try:
            input_data = in_queue.get()
            time.sleep(1)
            out_queue.put(input_data)
            in_queue.task_done()
        except queue.Empty:
            pass


if __name__ == '__main__':
    # run_multi_process()
    app.run(host='0.0.0.0', port=81)
