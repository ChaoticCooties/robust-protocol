import sys
import threading
import utils
import general
from rs import RS

def main():
    if len(sys.argv) != 3:
        print("\n main.py [receiver/sender] ip-address \n")
        exit()
    if sys.argv[1] == "sender":
        rs = RS(mtu=general.MTU)
        rs.bind_as_sender(receiver_address=(sys.argv[2], 8888))
        try:
            # parallel
             threads = []
             for id in range(0, 1000):
                 threads.append(threading.Thread(target = rs.send(f"data/data{id}", id)))
                 threads[-1].setDaemon(True)
                 threads[-1].start()

             for th in threads:
                 th.join()
        except Exception as e:
            print(e)
            rs.drop() # なくても大丈夫だとは思うけど一応安全のため

    elif sys.argv[1] == "receiver":
        rs = RS(mtu=general.MTU)
        rs.bind_as_receiver(receiver_address = (sys.argv[2], 8888))
        for i in range(0, 1000):
            filedata = rs.recv()
            utils.write_file(f"./data/data{i}", filedata)
            print(f"file received: {i}", end="\r")

if __name__ == '__main__':
    main()
