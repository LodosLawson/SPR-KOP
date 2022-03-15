import krpc 

class ConnectSetting:
    
    def __init__(self, ConnectName, IP, RPCPort, Port, Protocol ) -> None:

        try:
            self.ConnectName = krpc.connect(
                name=ConnectName,
                address=IP,
                rpc_port=int(RPCPort), stream_port=int(Port))
        
            self.Protocol = Protocol
        except:
            print("CONNECT ERROR")


    def getStatus(self):
        try:
            print(self.ConnectName.space_center)
            return True
        except ValueError:
            return False

    