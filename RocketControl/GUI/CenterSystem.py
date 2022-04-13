import ThreadConnect

#RocketControl <<WIDGET BACKEDN SYSTEM>>
class CenterSystem:

    THREADOBJECTVISIBLE = 0
    ConnectEvent = False
    def __init__(self, CenterConnect, root, Uproot) -> None:
        self.CCS = CenterConnect
        self.root = root
        self.Uproot = Uproot        
        
        while True:

            try:
                self.ACV = self.CCS.ConnectName.space_center.active_vessel
                break
            except:
                print("NO ACTIVE VESSEL")
        
     
               
        self.root.SelectedConnect.bind("<Button-1>", self.selectedvessel)

    def selectedvessel(self, event):
        if self.root.Listbox1.curselection() != ():
            if str(self.CCS.ConnectName.space_center.vessels[self.root.Listbox1.curselection()[0]].comms.signal_strength) != "0.0":            #    print("current vessel")
            #    print(self.con.space_center.vessels[self.root.Listbox1.curselection()[0]].name)
            #else:
                self.ConnectedEvent = True
                print(self.CCS.ConnectName.space_center.vessels[self.root.Listbox1.curselection()[0]])
                self.CCS.ConnectName.space_center.active_vessel = self.CCS.ConnectName.space_center.vessels[self.root.Listbox1.curselection()[0]]
                self.connectvessel(self.CCS.ConnectName.space_center.vessels[self.root.Listbox1.curselection()[0]])
                
                self.getVessels()
                self.ACV_THREAD = ThreadConnect.Connect(self.activevesselgetinfo, (""))
                self.ACV_THREAD.Run()
            else:
                print("NO CONNECT NO SIGNAL")
                
    def activevesselgetinfo(self):
        while True:
            self.root.CommSignalStatus.config(text=self.ACV.comms.signal_strength)
            self.root.VesselType.config(text=self.ACV.type)
            self.root.vesselname.config(text=self.ACV.name)
    
    def connectvessel(self, vessel):
        if str(vessel.type) == 'VesselType.debris': 
            pass
            print(str(vessel.type)+" <<< NO CONNECT 'NO PIC-PC', <<GARBER>>?")
        elif str(vessel.type) == 'VesselType.lander':
            pass
            print(str(vessel.type)+" <<< NO CONNECT 'NO PIC-PC', <<LANDING>>?")
        else:
            if vessel.comms.signal_strength > 0.0:
                #self..space_center.active_vessel = vessel
                self.ACV = vessel
                #self.activevesselgetinfo()
            else:
                print("NOT CONNECT VESSEL")

            if vessel.comms.signal_strength > 0.0:
                self.CCS.ConnectName.space_center.active_vessel = vessel
                self.ACV = vessel

                #self.activevesselgetinfo()
            else:
                print("NOT CONNECT VESSEL")
    
    def CS_Disconnect(self):
        self.CCS.ConnectName.close()
        self.Uproot.destroy()


    def getVessels(self):
        for index in range(self.root.Listbox1.size()):
            self.root.Listbox1.delete(0)
        i = 1
        for vessel in self.CCS.ConnectName.space_center.vessels:
            print(vessel.name)
            if str(vessel.type) == 'VesselType.debris': 
                self.root.Listbox1.insert(i,([vessel.name, " <name - signal> ", str(vessel.type)+" <<< NO CONNECT 'NO PIC-PC', <<GARBER>>?"]))#print(str(vessel.type)+" <<< NO CONNECT 'NO PIC-PC', <<GARBER>>?")
                i += 1
            elif str(vessel.type) == 'VesselType.lander':
                self.root.Listbox1.insert(i,([vessel.name, " <name - signal> ", str(vessel.type)+" <<< NO CONNECT 'NO PIC-PC', <<GARBER>>?"]))#print(str(vessel.type)+" <<< NO CONNECT 'NO PIC-PC', <<LANDING>>?")
                i += 1
            else:
                self.root.Listbox1.insert(i,([vessel.name, " <name - signal> ", vessel.comms.signal_strength]))
                i += 1
