from asyncio import selector_events
from threading import Thread
import krpc

import time
import tkinter as tk

import ThreadConnect

class PicPcControl:
    def __init__(self, CCS = "DefRoot", active_vessel = None, root = None, UpRoot = None, ROOT = None, RootInner = None) -> None:
        #self.con = krpc.connect(ConnectName)
        self.ROOT = ROOT
        self.CCS = CCS
        self.active_vessel = active_vessel
        self.root = root
        self.UpRoot = UpRoot
        self.RootInner = RootInner

        self.root.Disconnect.bind("<Button-1>", self.DisconnectAV)
        self.root.NextActiveGrup.bind("<Button-1>", self.NextGrupRocket)

        try:
            self.Control = ActivVesselControlSystem("ActiveVesselControl", self.active_vessel)
            self.HELP()
            self.UpRoot.bind("<Return>", self.OnClick)

        except:
            self.root.OutConsol.insert('end',"ERROR PICPC ROCKET CONNECT NOT WORK COMAND")
        


    def OnClick(self, event):
        #exec("self.root.OutConsol.insert('end', str("+self.active_vessel+".self.root.InputConsol.get()))")
        
        self.root.NextActiveGrup['state']  = tk.NORMAL
        self.ACV = self.Control.con.space_center.active_vessel
        self.ACC = self.Control

        exec("self.root.OutConsol.insert('1.0',"+"str("+str(self.root.InputConsol.get())+")+\"\\n\""+")")

        if str(self.root.InputConsol.get()) == "VInfo":
            self.root.OutConsol.insert('end', "VESSEL INFO--- \n"+str(self.Control.GetVesselInfo()))
        elif str(self.root.InputConsol.get()) == "GActiv":
            self.root.OutConsol.insert('end', "GRUP ACTIVE--- \n"+str(self.Control.ActiveGrup()))
        elif str(self.root.InputConsol.get()) == "Vresc":
            self.root.OutConsol.insert('end', "VESSEL RESOURCES--- \n"+str(self.Control.GetResources()))
        elif str(self.root.InputConsol.get()) == "VSpeed":
            self.root.OutConsol.insert('end', "VESSEL SPEED--- \n"+str(self.Control.SetVesselSpeed()))
    
    def HELP(self):
        self.root.OutConsol.insert('end',"ACV < ACTIVE VESSEL\nACC ACTIV VESSEL CONTROL \n")
        #self.root.OotConsol.insert('end',"Connect Active Rocket PICPC ---> "+str(self.ACV.name))
    
    def NextGrupRocket(self, event):
        self.ACV.control.activate_next_stage()


    def DisconnectAV(self, event):
        self.Control.con.close()
        self.CCS.ConnectName.close()
        self.UpRoot.destroy()
        self.RootInner.INFOCONCLOSE()


class ActivVesselControlSystem:
    def __init__(self, ConnectName = "DefRoot", Active_Vessel = None):
        self.con = krpc.connect(ConnectName)
        self.Active_Vessel = Active_Vessel

    def DeployAntena(self, IN):
        self.con.space_center.active_vessel.control.antennas = bool(IN)
        
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


class VesselInfoConnect:

    CB_SELECTED = 0

    def __init__(self, ConnectName, PICPC, CB_SELECTEDINDEX):
        self.con = krpc.connect(ConnectName)
        self.PICPC = PICPC
        self.CB_SELECTED = CB_SELECTEDINDEX
        
    def DisconnectAV(self):
        self.con.close()

    def ConnectSignal(self):
        while True:
            self.PICPC.root.VesselConnectSignal.config(text="Signal :    "+str(self.con.space_center.active_vessel.comms.signal_strength))
    
    def ConnectSignalRCS(self):
        while True:
            self.PICPC.root.CommSignalStatus.config(text="Signal :    "+str(self.con.space_center.active_vessel.comms.signal_strength))
    
    def OrbitInfoAP(self):
        while True:
            self.PICPC.root.OrbitalApsisValue.config(text="Apsis :   "+str(self.con.space_center.active_vessel.orbit.apoapsis))
            self.PICPC.root.OrbitalPeapsisValue.config(text="Peapsis :   "+str(self.con.space_center.active_vessel.orbit.periapsis))
            self.PICPC.root.OrbitalApsisAltValue.config(text="Apoapsis Altitude :    "+str(self.con.space_center.active_vessel.orbit.apoapsis_altitude))
            self.PICPC.root.OrbitalPeapsisAltValue.config(text="Periapsis Altitude : "+str(self.con.space_center.active_vessel.orbit.periapsis_altitude))
    
    def OrbitInfo(self):    
        while True:
           
            self.PICPC.root.OrbitalSpeedValue.config(text="Orbit Speed :   "+str(self.con.space_center.active_vessel.orbit.orbital_speed))
            self.PICPC.root.OrbitalPeriodValue.config(text="Orbit Period :  "+str(self.con.space_center.active_vessel.orbit.period))
            self.PICPC.root.OrbitalBodyName.config(text="Body SGp : "+str(self.con.space_center.active_vessel.orbit.body.gravitational_parameter))

            self.PICPC.root.OrbitalSelectedValue['values'] = ("Time To Apoapsis : "+str(self.con.space_center.active_vessel.orbit.time_to_apoapsis),
                                                                        "Time To Periapsis : "+str(self.con.space_center.active_vessel.orbit.time_to_periapsis),
                                                                            "Speed : "+str(self.con.space_center.active_vessel.orbit.speed))
            self.PICPC.root.OrbitalSelectedValue.current(self.CB_SELECTED)

    def RocketGetPart(self):
        #self.PICPC.root.Scrolledtreeview1.delete("1.0", "end-1c")
        self.PICPC.root.Scrolledtreeview1.config(selectmode = 'browse')
        #select = self.PICPC.root.Scrolledtreeview1.get_selection()
        #select.connect("changed", on_tree_selection_changed)
        self.PICPC.root.PartInfoLoaderWidget.config(text="Load...")
        self.PICPC.root.Scrolledtreeview1.bind('<ButtonRelease-1>', self.SelectPart)
        
        for i in self.PICPC.root.Scrolledtreeview1.get_children():
            self.PICPC.root.Scrolledtreeview1.delete(i)
        
        i = 0
        loadsize = 100 / len(self.con.space_center.active_vessel.parts.all)
        print(loadsize)
        self.Vessel_Parts_List = [] 

        for roc_parts in self.con.space_center.active_vessel.parts.all:
            
            self.Vessel_Parts_List.append(roc_parts)
            ii = 0

            part_info = self.PICPC.root.Scrolledtreeview1.insert('', i, text=str("ID"+str(i)+" : "+roc_parts.name), tags = ('tt',))
            #if roc_parts.temperature > 80.0:
            #self.PICPC.root.Scrolledtreeview1.tag_configure('tt', background="red")
            for info in dir(roc_parts):
                
                if info[0] != '_':
                    loc_ver = {}
                    
                    exec("ver = type(roc_parts."+info+")", locals(), loc_ver)
                    if str(loc_ver['ver']) == "<class 'float'>" or str(loc_ver['ver']) == "<class 'int'>" or str(loc_ver['ver']) == "<class 'str'>" or str(loc_ver['ver']) == "<class 'tuple'>":
                        exec("info = str(\""+info+" : \"+str(roc_parts."+info+"))", locals(), loc_ver)
                        self.PICPC.root.Scrolledtreeview1.insert(part_info,  'end', text="PID"+str(ii)+" : "+loc_ver['info'])
                        ii+=1
            i+=1

            
            self.PICPC.root.LoadingObject['value'] = i*loadsize
            #self.PICPC.root.update_idletasks()

        self.PICPC.root.PartInfoLoaderWidget.config(text="Part Info Loading Compleyt...")

        
        #time.sleep(4)

    #ONTI[P]
    PARTINFOON = False
    def SelectPart(self, event):
      

        #Select_Parts = self.PICPC.root.Scrolledtreeview1.focus()
        #print(dir(selector_events))
        curItem = self.PICPC.root.Scrolledtreeview1.focus()
        #curRow = self.PICPC.root.Scrolledtreeview1.set(event)
        #loc_value = curRow["loc"]
        selected_item = self.PICPC.root.Scrolledtreeview1.selection()[0]
        print(self.PICPC.root.Scrolledtreeview1.item(curItem))

        if self.PARTINFOON == False:
            ThreadConnect.Connect(self.SetRocketPartInfo, ("")).Run()
            self.PARTINFOON = True
        #else:
         #   self.SetRocketPartInfo()

        print(selected_item)
        print(self.PICPC.root.Scrolledtreeview1.focus()[0])
        
        #dir(self.PICPC.root.Scrolledtreeview1.focus()[0])
        #self.PICPC.root.RocketSelectedPartInfo.config(text="test : "+Select_Parts)
        
        #self.PICPC.root.Scrolledtreeview1.insert('', 'end', 'Col1', text='0')
        #self.PICPC.root.Scrolledtreeview1.set("Col1", 'Col1', '12KB')

    def SetRocketPartInfo(self):
        while True:
            curItem = self.PICPC.root.Scrolledtreeview1.focus()
            #curRow = self.PICPC.root.Scrolledtreeview1.set(event)
            #loc_value = curRow["loc"]

            ID = str(self.PICPC.root.Scrolledtreeview1.item(curItem, "text")).split(":")[0][:2]
            PID = str(self.PICPC.root.Scrolledtreeview1.item(curItem, "text")).split(":")[0][:3]

            if ID == "ID":
                SelectedItem = self.Vessel_Parts_List[int(str(self.PICPC.root.Scrolledtreeview1.item(curItem, "text")).split(":")[0][2:])]
                POST = ""
                for info in dir(SelectedItem):
                        
                    if info[0] != '_':
                        loc_ver = {}
                            
                        exec("ver = type(SelectedItem."+info+")", locals(), loc_ver)
                        if str(loc_ver['ver']) == "<class 'float'>" or str(loc_ver['ver']) == "<class 'int'>" or str(loc_ver['ver']) == "<class 'str'>" or str(loc_ver['ver']) == "<class 'tuple'>":
                            exec("info = str(\""+info+" : \"+str(SelectedItem."+info+"))", locals(), loc_ver)
                            POST += loc_ver['info'] + "\n"

                self.PICPC.root.RocketSelectedPartInfo.config(text=POST)

            elif PID == "PID":
                self.PICPC.root.RocketSelectedPartInfo.config(text="NON OR BIT")

    def Spped(self):
        while True:
            flight = self.con.space_center.active_vessel.flight()
            self.PICPC.root.RocketVelocity.config(text="Velocity : "+str(flight.velocity))
            self.PICPC.root.RocketSpeed.config(text="Speed : "+str(flight.speed))
            self.PICPC.root.RocketVerticalSpeed.config(text="Vertical Speed"+str(flight.vertical_speed))

    def Altitude(self):
        while True:
            flight = self.con.space_center.active_vessel.flight()

            self.PICPC.root.RocketMeanAltitude.config(text="Mean Altitude : "+str(flight.mean_altitude))
            self.PICPC.root.RocketSurfaceAltitude.config(text="Surface Altitude : "+str(flight.surface_altitude))
            self.PICPC.root.RocketBedrockAltitude.config(text="Bedrock Altitude : "+str(flight.bedrock_altitude))
            self.PICPC.root.RocketGForce.config(text="G Force : "+str(flight.g_force))
    
    def Resources(self):
        while True:
            POST = ""
            for res in self.con.space_center.active_vessel.resources.all:
                POST += str(res.name)+":>"+str(res.amount)+"\n"
            #self.PICPC.root.RocketResourcesValues.delete("1.0", "end-1c")
            self.PICPC.root.RocketResourcesValues.config(text=str(POST))

    #GUI  
    def callback(self, event):
        self.CB_SELECTED = self.PICPC.root.OrbitalSelectedValue.current()