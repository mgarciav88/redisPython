import multiprocessing
import time
from multiprocessing import Process
from threading import Thread

from flask import Flask

from src.constants import LIST_KEY, EXIT_EVENT
from src.redis_client import client, initialize_client, RedisClient

app = Flask(__name__)

memory_db = list()

initialize_client(client)


@app.route('/')
def index():
    t = Thread(target=run_multi_process, args=(client,), kwargs={})
    t.start()
    return 'Running multiprocessing + redis in the background'


def run_multi_process(redis_client):
    manager = multiprocessing.Manager()
    receive_queue = manager.Queue()
    out_queue = manager.Queue()

    num_consumers = multiprocessing.cpu_count()
    num_producers = multiprocessing.cpu_count()

    producers_process_list = list()
    for prod_num in range(num_producers):
        process = Process(target=producer, args=(redis_client, prod_num, receive_queue,))
        process.start()
        producers_process_list.append(process)

    consumers_list = list()
    for cons_num in range(num_consumers):
        process = Process(target=consumer, args=(redis_client, receive_queue, out_queue,))
        process.start()
        consumers_list.append(process)

    receive_queue.join()

    for process in producers_process_list:
        process.join()

    for _ in range(num_producers):
        receive_queue.put(EXIT_EVENT)

    out_queue.join()
    for process in consumers_list:
        process.join()

    results = list()
    while not out_queue.empty():
        results.append(out_queue.get())
        out_queue.task_done()

    print(results)


def producer(redis_client: RedisClient, prod_num, proc_queue: multiprocessing.Queue, list_key: str = LIST_KEY):
    time.sleep(1)
    redis_client.client.lpush(list_key, prod_num / 100)
    proc_queue.put(prod_num)


def consumer(redis_client: RedisClient, in_queue: multiprocessing.Queue, out_queue: multiprocessing.Queue,
             list_key: str = LIST_KEY):
    while True:
        input_data = in_queue.get()
        if input_data != EXIT_EVENT:
            time.sleep(2)
            out_queue.put(input_data)
            in_queue.task_done()
            redis_client.client.lpush(list_key, 2 * input_data / 100)
        else:
            in_queue.task_done()
            return


if __name__ == '__main__':
    # run_multi_process()
    app.run(host='0.0.0.0', port=81)
