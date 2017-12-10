#!/usr/bin/env python
# -*- coding: utf-8 -*-
from BeautifulSoup import BeautifulSoup
import requests
import re
from multiprocessing.pool import ThreadPool
import DB


class MyThreadPool:
    """ Pool of threads consuming tasks from a queue """
    def __init__(self, num_threads ):
        self._pool = ThreadPool(num_threads)
        self._ClientMap = {}
        self._db = DB.DB()

    def add_task(self,socket ,id):
        """ Add a task to the queue """
        self._ClientMap[id] = socket
        self._pool.apply(self.search,(id,))


    def search(self , id):
        try:
            ans = None
            self._db.connect()
            self._db.execute("UPDATE public.ex2 SET status = 1 WHERE id = %s",(id,))
            url = self._db.execute("SELECT public.ex2.url FROM public.ex2 WHERE public.ex2.id= %s",(id,))
            string = self._db.execute("SELECT public.ex2.value FROM public.ex2 WHERE public.ex2.id= %s",(id,))
            r = requests.get(url)
            html = r.text
            soup = BeautifulSoup(html)
            de_string = string.decode('UTF-8')
            found = soup.findAll(text=re.compile(de_string))
            if len(found) == 0:
                ans = False
            else:
                ans = True
        except Exception as exp:
            print(exp)
        self._ClientMap[id].send("ans: " + str(ans))
        self._db.execute("UPDATE public.ex2 SET status = 2, finish_timestamp = current_timestamp WHERE id = %s", (id,))
        self._ClientMap[id].shutdown()
        self._ClientMap[id].close()
        self._ClientMap.pop(id)

"""
if __name__ == '__main__':
    print(search('http://www.ariel.ac.il/' , "מידע אישי"))
    print(search('http://www.ariel.ac.il/' , "גן בוטני"))
    print(search('https://www.python.org/' , "Django"))
    tp = MyThreadPool(2)

    print(tp.add_task("http://www.ariel.ac.il/", "מידע אישי"))
    print(tp.add_task('http://www.ariel.ac.il/', "גן בוטני"))
    print(tp.add_task('https://www.python.org/', "מידע אישי"))"""