from tkinter import *
import tkinter
import krpc

con = krpc.connect()

top = Tk()
Status = Tk()

frame = Frame(top, bg="red")

L = Listbox(top)

i = 1
for x in con.space_center.vessels:
  i+1
  L.insert(i,[x.name,"-",str(x.comms.signal_strength)])
  
def motion(event):

  #print("Mouse position: (%s %s)" % (event.x, event.y))
  #print(L.get(L.curselection()[0]))
  #print(L.curselection()[0])
  #print(con.space_center.vessels[L.curselection()[0]])#[L.curselection()[0]].control.state()

  if con.space_center.vessels[L.curselection()[0]].comms.signal_strength > 0 :
  
    con.space_center.active_vessel = con.space_center.vessels[L.curselection()[0]]
    #print(con.space_center.vessels[L.curselection()[0]].state)

    for x in range(L.size()):
      L.delete(0)

    i = 1
    for x in con.space_center.vessels:
      i+1
      L.insert(i,[x.name,"-",str(x.comms.signal_strength)])

    #Status.mainloop()
  else:
    print("Not Connection Vessel")
                   
  return


top.bind("<Button-1>", motion)

L.config(width=65, height=55)
L.pack()

frame.pack()

top.minsize()
top.mainloop()
    

