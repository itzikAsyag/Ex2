import socket


class Client_Class:

    def __init__(self, ip="127.0.0.1", port=12345):  # initialize , getting username from user
        self._ip = ip
        self._port = port
        self._ans = None

    def connect(self, website , value):  # create connection to server with host and ip variables from user
        try:
            server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            # Connect the socket to the port where the server is listening
            server.connect((self._ip, self._port))
            msg = "website: "+website+"|value: "+value
            server.send(msg)
        except Exception, error:
            print error

        while True:
            try:
                data = server.recv(1024)
                if 'ok' == data:
                    server.close()
                    return True

                if 'bad' == data:
                    server.close()
                    return False
                else:
                    try:
                        ans = data[5:]
                        self._ans = ans
                        server.close()
                        return True
                    except:
                        pass
            except:
                pass

    def get_ans(self , website , value):
        if self.connect(website , value):
            print 'Got new ans'
            return self._ans
        else:
            print("bad get_ans")
