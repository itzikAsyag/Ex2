#!/usr/bin/env python
# -*- coding: utf-8 -*-
import socket
import DB
import select
import Search



class MyServer:

    def __init__(self, ip="127.0.0.1", port=12345 , numOfThreads=5):
        self._ip = ip
        self._port = port
        self._server = None
        self._ClientMap = {}
        self._db = DB.DB()
        self._threadPool = Search.MyThreadPool(numOfThreads)

    def run(self):
        self.__activate_server()
        read_list = [self._server]
        #self.pushClientToDB("http://www.ariel.ac.il/", "מידע אישי")
        while True:
            readable, writable, errored = select.select(read_list, [], [], 10)
            for s in readable:
                if s is self._server:
                    client_socket, address = self._server.accept()
                    read_list.append(client_socket)
                    print "Connection from", address
                else:
                    data = s.recv(1024)
                    if data:
                        #print data
                        try:
                            if "website: " == data[:9]:
                                arr_values = data.split("|")
                                website = (arr_values[0])[9:]
                                value = (arr_values[1])[7:]
                                ##################################
                                #connect and send to DB and wait for Search answer
                                self.pushClientToDB(client_socket, website , value)
                                ##################################
                                s.close()
                                read_list.remove(s)
                            else:
                                s.send('bad')
                                s.close()
                                read_list.remove(s)

                        except Exception, error:
                            print error.args
                            s.send('bad')
                            s.close()
                            read_list.remove(s)


                    else:
                        s.close()
                        read_list.remove(s)

    def __activate_server(self):
        # Create a TCP/IP socket
        self._server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._server.bind((self._ip, self._port))
        self._server.setblocking(False)
        # Listen for incoming connections
        self._server.listen(5)

    def pushClientToDB(self ,socket , url , string):
        self._db.connect()
        nextID = self._db.execute("INSERT INTO public.ex2 (url, value) VALUES (%s,%s) RETURNING id;",(url, string))
        self._db.disconnect()
        self._threadPool.add_task(socket , nextID)
        return 0

if __name__ == '__main__':
    try:
        temp = MyServer()
        temp.run()

    except KeyboardInterrupt:
        print 'Done!'
        exit()
