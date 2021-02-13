import general

# Very simple packet structure.
# Header contains the id (file metadata)
# Packet contains the payload (file binary)

class Header:
    def __init__(self, id):
        self.id = id

    def from_raw(self, raw):
        self.id = int.from_bytes(raw[0:1], "big")

    def raw(self):
        raw = self.id.to_bytes(2, "big")
        return raw

    def from_dict(self, dict):
        self.id = dict["id"]

class Packet:
    # def __init__(self, header, payload):
    #     self.header = header
    #     self.payload = payload

    def from_raw(self, raw):
        self.payload = raw[general.SCU_HEADER_LENGTH:]

    def raw(self):
        raw = self.header.raw()
        raw += self.payload
        return raw

    def from_dict(self, dict):
        self.header = dict["header"]
        self.payload = dict["payload"]
