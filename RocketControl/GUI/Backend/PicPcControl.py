
class PicPcControl:
    def __init__(self, ConnectName = "DefRoot", active_vessel = None, root = tkinter, UpRoot = None) -> None:
        self.con = krpc.connect(ConnectName)
        self.active_vessel = active_vessel
        self.root = root
        self.UpRoot = UpRoot
        
        self.Control = ActivVesselControlSystem("ActiveVesselControl", self.active_vessel)
        
        self.UpRoot.bind("<Return>", self.OnClick)

    def OnClick(self, event):
        #exec("self.root.OutConsol.insert('end', str("+self.active_vessel+".self.root.InputConsol.get()))")
        
        exec("self.root.OutConsol.insert('end',"+str(self.root.InputConsol.get())+")")

        if str(self.root.InputConsol.get()) == "VInfo":
            self.root.OutConsol.insert('end', "VESSEL INFO--- \n"+str(self.Control.GetVesselInfo()))
        elif str(self.root.InputConsol.get()) == "GActiv":
            self.root.OutConsol.insert('end', "GRUP ACTIVE--- \n"+str(self.Control.ActiveGrup()))
        elif str(self.root.InputConsol.get()) == "Vresc":
            self.root.OutConsol.insert('end', "VESSEL RESOURCES--- \n"+str(self.Control.GetResources()))
        elif str(self.root.InputConsol.get()) == "VSpeed":
            self.root.OutConsol.insert('end', "VESSEL SPEED--- \n"+str(self.Control.SetVesselSpeed()))