from pydoc import visiblename
from sqlite3 import connect

import sys

from tkinter import *
import tkinter as tk
import tkinter
import tkinter.ttk as ttk

import krpc

import ThreadConnect
from Backend.VesselInfoConnect import *
import RocketControlGui
import PicPcControl

class SpaceCenterConnect:

    THREADOBJECTVISIBLE = 0
    def __init__(self, ConnectName = "DefRoot", root = tkinter, UpRoot = None) -> None:
        self.con = krpc.connect(ConnectName)
        self.root = root
        self.UpRoot = UpRoot

        self.UpRoot.bind("<Button-1>", self.motion)
        self.UpRoot.bind("<Button-1>", self.Disconnect)

        self.active_vessel = self.con.space_center.active_vessel

        self.AV_ORBIT_INFOCONNECTOR = VesselInfoConnect("Connect Orbit Info ", self, 0)
        self.AV_ORBIT_AP_INFOCONNECTOR = VesselInfoConnect("Connect Orbit AP Info", self, 0)
        self.AV_SIGNAL_INFOCONNECTOR = VesselInfoConnect("Connect Signal Info ", self, 0)

        self.getActiveVesel()
        self.activevesselgetinfo()

        self.PICPC = None
        
    def RUN(self):
        SignalConnectRCS = ThreadConnect.Connect(self.AV_SIGNAL_INFOCONNECTOR.ConnectSignalRCS, (""))
        SignalConnectRCS.Run()

    def setorbitinfo(self):
        
        while True:
            self.PICPC.OrbitalApsisValue.config(text="Apsis :   "+str(self.con.space_center.active_vessel.orbit.apoapsis))
            self.PICPC.OrbitalPeapsisValue.config(text="Peapsis :   "+str(self.con.space_center.active_vessel.orbit.periapsis))
            self.PICPC.OrbitalApsisAltValue.config(text="Apoapsis Altitude :    "+str(self.active_vessel.orbit.apoapsis_altitude))
            self.PICPC.OrbitalPeapsisAltValue.config(text="Periapsis Altitude : "+str(self.active_vessel.orbit.periapsis_altitude))
            self.PICPC.OrbitalSelectedValue['values'] = ("test")

    def gettestbuttoncilcik():
        print("Hello")

    def getActiveVesel(self):
        self.active_vesel = self.con.space_center.active_vessel

    def getVessels(self):
        for index in range(self.root.Listbox1.size()):
            self.root.Listbox1.delete(0)
        i = 0
        for vessel in self.con.space_center.vessels:
            if str(vessel.type) == 'VesselType.debris': 
                self.root.Listbox1.insert(i,([vessel.name, " <name - signal> ", str(vessel.type)+" <<< NO CONNECT 'NO PIC-PC', <<GARBER>>?"]))#print(str(vessel.type)+" <<< NO CONNECT 'NO PIC-PC', <<GARBER>>?")
                i += 1
            elif str(vessel.type) == 'VesselType.lander':
                self.root.Listbox1.insert(i,([vessel.name, " <name - signal> ", str(vessel.type)+" <<< NO CONNECT 'NO PIC-PC', <<GARBER>>?"]))#print(str(vessel.type)+" <<< NO CONNECT 'NO PIC-PC', <<LANDING>>?")
                i += 1
            else:
                self.root.Listbox1.insert(i,([vessel.name, " <name - signal> ", vessel.comms.signal_strength]))
                i += 1

    def Disconnect(self, event):
        if self.THREADOBJECTVISIBLE != 0:
            self.AV_ORBIT_INFOCONNECTOR.DisconnectAV()
            self.AV_ORBIT_AP_INFOCONNECTOR.DisconnectAV()
            self.AV_SIGNAL_INFOCONNECTOR.DisconnectAV()
            
    def motion(self, event):
        if self.root.Listbox1.curselection() != ():
            if str(self.active_vessel.comms.signal_strength) != "0.0":
            #    print("current vessel")
            #    print(self.con.space_center.vessels[self.root.Listbox1.curselection()[0]].name)
            #else:
          
                self.connectvessel(self.con.space_center.vessels[self.root.Listbox1.curselection()[0]])
                self.getVessels()

    def connectvessel(self, vessel):
        if str(vessel.type) == 'VesselType.debris': 
            pass
            print(str(vessel.type)+" <<< NO CONNECT 'NO PIC-PC', <<GARBER>>?")
        elif str(vessel.type) == 'VesselType.lander':
            pass
            print(str(vessel.type)+" <<< NO CONNECT 'NO PIC-PC', <<LANDING>>?")
        else:
            if vessel.comms.signal_strength > 0.0:
                self.con.space_center.active_vessel = vessel
                self.active_vesel = vessel
                self.activevesselgetinfo()
            else:
                print("NOT CONNECT VESSEL")

    def activevesselgetinfo(self):
        self.root.CommSignalStatus.config(text=self.active_vesel.comms.signal_strength)
        self.root.VesselType.config(text=self.active_vesel.type)
        self.root.vesselname.config(text=self.active_vesel.name)
        
        #self.root.VesselResources.config(text="CONNECT POINT\nSTART: "+self.active_vesel.comms+"\nEND: "+self.active_vesel.comms)


    def ConsolControl(self):
        self.THREADOBJECTVISIBLE = 1
        global root_pic_pc

        root_pic_pc = tk.Tk()
        root_pic_pc.protocol( 'WM_DELETE_WINDOW' , root_pic_pc.destroy)
        
        global _top1, _w1
        _top1 = root_pic_pc
        _w1 = RocketControlGui.SetControlPicPc(_top1)

        self.PICPC = _w1
        pic_pc_control = PicPcControl("PIC-PC-CONTROL", self.active_vessel, _w1, root_pic_pc)
        self.PICPC.OrbitalSelectedValue.bind("<<ComboboxSelected>>", self.callback)
        self.PICPC.Disconnect.bind("<Button-1>", self.Disconnect)
        
        self.OrbitInfo = ThreadConnect.Connect(self.AV_ORBIT_INFOCONNECTOR.OrbitInfo, (""))
        self.OrbitInfo.Run()

        self.OrbitInfoAP = ThreadConnect.Connect(self.AV_ORBIT_AP_INFOCONNECTOR.OrbitInfoAP, (""))
        self.OrbitInfoAP.Run()
        
        self.SignalConnect = ThreadConnect.Connect(self.AV_SIGNAL_INFOCONNECTOR.ConnectSignal, (""))
        self.SignalConnect.Run()



        root_pic_pc.mainloop()
    
    #GUI  
    def callback(self, eventObject):
        self.AV_ORBIT_INFOCONNECTOR.CB_SELECTED = self.PICPC.OrbitalSelectedValue.current()