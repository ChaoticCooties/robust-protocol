from queue import Queue
import socket
import threading
from enum import Enum
from packet import Header, Packet
import utils
import general

from reedsolo import RSCodec
rsc = RSCodec(general.ECCSymbol)

class SCUMode(Enum):
    SendMode = 0
    RecvMode = 1

class SCU:
    def __init__(self, mtu=1500):
        self.mtu = mtu

    def bind_as_sender(self, receiver_address):
        self.mode = SCUMode.SendMode
        self.connection_manager = {}

        self.socket =  socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.receiver_address = receiver_address
        self.lock = threading.Lock()

        sender_packet_loop_thread = threading.Thread(target=self._sender_packet_loop)
        sender_packet_loop_thread.setDaemon(True)
        sender_packet_loop_thread.start()

    def bind_as_receiver(self, receiver_address):
        self.mode = SCUMode.RecvMode
        self.received_files_data = {}

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind(receiver_address)

        self.file_received = Queue()

        receiver_packet_loop_thread = threading.Thread(target=self._receiver_packet_loop)
        receiver_packet_loop_thread.setDaemon(True)
        receiver_packet_loop_thread.start()

    def drop(self):
        if self.mode == SCUMode.SendMode:
            self.connection_manager.clear()
            self.socket.close()

    def _sender_packet_loop(self):
        if self.mode == SCUMode.RecvMode:
            raise Exception
        while True:
            try:
                packet = Packet()
                packet.from_raw(self.socket.recv(2048))
                if packet.header.id not in self.connection_manager:
                    continue
                self.connection_manager[packet.header.id].put((True, packet.header.seq))
            except Exception as e: # recvが失敗した時とputが失敗した時は(適当)
                if e == KeyboardInterrupt:
                    raise KeyboardInterrupt
                else:
                    import traceback
                    traceback.print_exc()

    def send(self, filepath, id): # will lock the thread
        if self.mode == SCUMode.RecvMode:
            raise Exception
        queue = Queue()
        self.connection_manager[id] = queue # コネクションを登録

        data_fragments = utils.split_file_into_mtu(filepath, self.mtu)

        all_packets = []
        for (seq, df) in enumerate(data_fragments):
            # create header
            header = Header(id)

            # create packet
            packet = Packet()
            payload = rsc.encode(df)
            packet.from_dict({ "header": header, "payload": payload, })

            all_packets.append(packet)

        while True:
            try:
                while True:
                    try:
                        del(self.connection_manager[id]) # コネクションを解除
                        return
                    except Exception as e: # キューが空の時
                        if e == KeyboardInterrupt:
                            raise KeyboardInterrupt
                        else:
                            break
                with self.lock: # 複数のsendメソッドが並列に同時実行されている可能性があるため，ロックが必要
                    self.socket.sendto(all_packets[seq].raw(), self.receiver_address) # パケット送信
            except Exception as e: # sendtoが失敗した時は(適当)
                if e == KeyboardInterrupt:
                    raise KeyboardInterrupt
                else:
                    import traceback
                    traceback.print_exc()



    def _receiver_packet_loop(self):
        if self.mode == SCUMode.SendMode:
            raise Exception
        received_files_flag = {}
        received_files_length = {}
        while True:
            try:
                data, from_addr = self.socket.recvfrom(2048)
                packet = Packet()
                packet.from_raw(data)

                key = utils.endpoint2str(from_addr, packet.header.id)
                if key not in self.received_files_data:
                    self.received_files_data[key] = [b""]*100
                    received_files_flag[key] = False

                    self.received_files_data[key][packet.header.seq] = rsc.decode(packet.payload)
                    if key in received_files_length and self.is_all_received(key, received_files_length[key]): #  ファイル受信完了
                        received_files_flag[key] = True
                        self.file_received.put((key, received_files_length[key]))

            except Exception as e: # recvが失敗した時とputが失敗した時は(適当)
                if e == KeyboardInterrupt:
                    raise KeyboardInterrupt
                else:
                    import traceback
                    traceback.print_exc()

    def is_all_received(self, key, length):
        for i in range(0, length):
            if not self.received_files_data[key][i]:
                return False
        return True

    def recv(self):
        if self.mode == SCUMode.SendMode:
            raise Exception
        key, length = self.file_received.get()
        return utils.fold_data(self.received_files_data[key], length)
