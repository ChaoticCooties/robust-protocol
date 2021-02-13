import general
from reedsolo import RSCodec, ReedSolomonError
rsc = RSCodec(general.ECCSymbol)

def split_file_into_mtu(filepath, mtu):
    data_fragments = []
    try:
        fd = open(filepath, "rb")
        while True:
            df = fd.read(mtu - general.IP_HEADER_LENGTH - general.UDP_HEADER_LENGTH - general.SCU_HEADER_LENGTH)
            if not df:
                break
            encoded_df = bytes(rsc.encode(df))
            #print(filepath)
            #print("df = ",len(df))
            #print("encoded_df = ",len(encoded_df))
            data_fragments.append(encoded_df)
            #data_fragments.append(df)
        fd.close()
    except:
        fd.close()
        print("error")
        return None

    return data_fragments

def write_file(filename, data):
    with open(filename, mode='wb') as f:
        f.write(data)

def endpoint2str(addr, fileid):
    return f"{addr[0]}:{addr[1]}:{fileid}"

def fold_data(l, length):
    filedata = b""
    for i in range(0, length):
        filedata += l[i]
    return filedata

if __name__ == "__main__":
    df = split_file_into_mtu("test.txt",1500)
    print(df[0])
    print("This is decoded!!!")
    print(bytes(rsc.decode(df[0])[0]))
    

