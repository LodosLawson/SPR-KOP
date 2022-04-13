import krpc 

class ActivVesselControlSystem:
    def __init__(self, ConnectName = "DefRoot", Active_Vessel = None):
        self.con = krpc.connect(ConnectName)
        self.Active_Vessel = Active_Vessel

    def SetVesselSpeed(self, Speed):
        self.Active_Vessel.control.throttle = Speed
        return str(self.Active_Vessel.control.throttle)
    
    def GetVesselInfo(self):
        return str("Name : "+self.Active_Vessel.name+"\n"+"Signal : "+str(self.Active_Vessel.comms.signal_strength))

    def ActiveGrup(self):
        return str("_"+self.Active_Vessel.activate_next_stage())
    
    def GetResources(self):
        resc = ""
        for xv in self.Active_Vessel.resources.all:
            resc += xv.name+" - "+str(xv.amount)+"\n"
        return str(resc+"\n")
    

class ActivVesselControlSystem:
    def __init__(self, ConnectName = "DefRoot", Active_Vessel = None):
        self.con = krpc.connect(ConnectName)
        self.Active_Vessel = Active_Vessel

    def SetVesselSpeed(self, Speed):
        self.Active_Vessel.control.throttle = Speed
        return str(self.Active_Vessel.control.throttle)
    
    def GetVesselInfo(self):
        return str("Name : "+self.Active_Vessel.name+"\n"+"Signal : "+str(self.Active_Vessel.comms.signal_strength))

    def ActiveGrup(self):
        return str("_"+self.Active_Vessel.activate_next_stage())
    
    def GetResources(self):
        resc = ""
        for xv in self.Active_Vessel.resources.all:
            resc += xv.name+" - "+str(xv.amount)+"\n"
        return str(resc+"\n")

class SingleConnect:
    def __init__(self, ConnectName):
        self.con = krpc.connect(ConnectName)

    def get(self):
        return self.con

