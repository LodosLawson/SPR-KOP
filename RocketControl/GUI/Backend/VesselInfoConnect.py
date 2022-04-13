import krpc 

class VesselInfoConnect:

    CB_SELECTED = 0

    def __init__(self, ConnectName, SpaceCenter, CB_SELECTEDINDEX):
        self.con = krpc.connect(ConnectName)
        self.SpaceCenter = SpaceCenter

    def DisconnectAV(self):
        self.con.close()

    def ConnectSignal(self):
        while True:
            self.SpaceCenter.PICPC.VesselConnectSignal.config(text="Signal :    "+str(self.con.space_center.active_vessel.comms.signal_strength))
    
    def ConnectSignalRCS(self):
        while True:
            self.SpaceCenter.root.CommSignalStatus.config(text="Signal :    "+str(self.con.space_center.active_vessel.comms.signal_strength))
    
    def OrbitInfoAP(self):
        while True:
            self.SpaceCenter.PICPC.OrbitalApsisValue.config(text="Apsis :   "+str(self.con.space_center.active_vessel.orbit.apoapsis))
            self.SpaceCenter.PICPC.OrbitalPeapsisValue.config(text="Peapsis :   "+str(self.con.space_center.active_vessel.orbit.periapsis))
            self.SpaceCenter.PICPC.OrbitalApsisAltValue.config(text="Apoapsis Altitude :    "+str(self.con.space_center.active_vessel.orbit.apoapsis_altitude))
            self.SpaceCenter.PICPC.OrbitalPeapsisAltValue.config(text="Periapsis Altitude : "+str(self.con.space_center.active_vessel.orbit.periapsis_altitude))
    
    def OrbitInfo(self):    
        while True:
           
            self.SpaceCenter.PICPC.OrbitalSpeedValue.config(text="Orbit Speed :   "+str(self.con.space_center.active_vessel.orbit.orbital_speed))
            self.SpaceCenter.PICPC.OrbitalPeriodValue.config(text="Orbit Period :  "+str(self.con.space_center.active_vessel.orbit.period))
            self.SpaceCenter.PICPC.OrbitalBodyName.config(text="Body SGp : "+str(self.con.space_center.active_vessel.orbit.body.gravitational_parameter))

            self.SpaceCenter.PICPC.OrbitalSelectedValue['values'] = ("Time To Apoapsis : "+str(self.con.space_center.active_vessel.orbit.time_to_apoapsis),
                                                                        "Time To Periapsis : "+str(self.con.space_center.active_vessel.orbit.time_to_periapsis),
                                                                            "Speed : "+str(self.con.space_center.active_vessel.orbit.speed))
            self.SpaceCenter.PICPC.OrbitalSelectedValue.current(self.CB_SELECTED)
