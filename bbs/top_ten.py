from bbs import db
import threading, time
from icecream import ic

class Top_ten:
    '''
    Maintain top 10 hot threads. Update per minute.

    Never directly access attributes in this class,
    for they are not thread-safe.
    Use getter method instead.
    '''
    def __init__(self, delay_factor = 0.99):
        self.delay_factor = delay_factor
        self.comments = db.get_all_threads_comment_num()
        self.temperature = {threadid: 0 for threadid in self.comments.keys()}
        self.lock = threading.Lock()
        self.top_ten = []

        update_thread = threading.Thread(target=self.update)
        update_thread.start()

    def get_top_ten(self):
        self.lock.acquire()
        ret = self.top_ten.copy()
        self.lock.release()
        return ret
        
    def update(self):
        while 1:
            cur_comments = db.get_all_threads_comment_num()
            delta_comments = {
                threadid: cur_comments[threadid] - self.comments.get(threadid, 0)
                for threadid in cur_comments.keys()
            }
            self.comments = cur_comments
            new_temperature = {
                threadid: self.temperature.get(threadid, 0) * self.delay_factor + delta_comments[threadid] * (1-self.delay_factor)
                for threadid in delta_comments.keys()
            }
            self.temperature = new_temperature

            self.lock.acquire()
            self.top_ten = sorted(self.temperature.keys(), key=self.temperature.get, reverse=True)[:10]
            self.lock.release()
            time.sleep(60)
