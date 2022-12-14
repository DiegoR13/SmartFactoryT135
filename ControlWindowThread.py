from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image
from NewServer import Server
import time
import threading

class ControlWindow(threading.Thread):
    def __init__(self):
        self.srvr = Server()
        threading.Thread.__init__(self)
        self.start()
        self.estadoBot1 = 0
        self.estadoBot2 = 0
        
    def callback(self):
        self.window.quit()  

    def update(self):
        self.srvr.Vars()
        self.Status.configure(fg=self.srvr.statusCol)
        self.TxtStatus.set(self.srvr.statusTxt)
        self.StatusTxt.configure(fg=self.srvr.statusCol)
        self.canvasStatInd.itemconfig(self.oval, fill=self.srvr.statusCol,outline=self.srvr.statusCol)
        self.LabelxMART1.configure(fg=self.srvr.colorx1)
        self.LabelxMART2.configure(fg=self.srvr.colorx2)
        self.x1BattCanvas.itemconfig(self.BattCanvx1,fill=self.srvr.Batx1Col)
        self.x1BattCanvas.itemconfig(self.txtBatt1,text=(str(self.srvr.Batx1) + " %"))
        self.x1BattCanvas.coords(self.BattCanvx1,0,0,self.srvr.xBatx1,55)
        self.x2BattCanvas.itemconfig(self.BattCanvx2,fill=self.srvr.Batx2Col)
        self.x2BattCanvas.itemconfig(self.txtBatt2,text=(str(self.srvr.Batx2) + " %"))
        self.x2BattCanvas.coords(self.BattCanvx2,0,0,self.srvr.xBatx2,55)
        self.txtRSx1.set(self.srvr.RSx1)
        self.txtMSx1.set(self.srvr.MSx1)
        self.txtGXx1.set(self.srvr.GXx1)
        self.txtGYx1.set(self.srvr.GYx1)
        self.txtCXx1.set(self.srvr.CXx1)
        self.txtCYx1.set(self.srvr.CYx1)
        self.txtD2Gx1.set(self.srvr.distSMART1)
        self.txtRSx2.set(self.srvr.RSx2)
        self.txtMSx2.set(self.srvr.MSx2)
        self.txtGXx2.set(self.srvr.GXx2)
        self.txtGYx2.set(self.srvr.GYx2)
        self.txtCXx2.set(self.srvr.CXx2)
        self.txtCYx2.set(self.srvr.CYx2)
        self.txtRSOM.set(self.srvr.RSOM)
        self.txtD2Gx2.set(self.srvr.distSMART2)
        self.txtPzasMod.set(self.srvr.PzasMod)
        self.txtStatConv.set(self.srvr.StatConv)
        self.txtStatABB.set(self.srvr.StatABB)
        self.txtPzasAlm.set(self.srvr.PzasAlm)
        
    def changeBot1(self):
        if self.estadoBot1 == 0:
            self.txtBot1.set("Activar")
            self.srvr.changeStates(5,16)
            self.estadoBot1 = 1
        elif self.estadoBot1 == 1:
            self.txtBot1.set("Desactivar")
            self.srvr.changeStates(5,0)
            self.estadoBot1 = 0

    def changeBot2(self):
        if self.estadoBot2 == 0:
            self.txtBot2.set("Activar")
            self.srvr.changeStates(12,16)
            self.estadoBot2 = 1
        elif self.estadoBot2 == 1:
            self.txtBot2.set("Desactivar")
            self.srvr.changeStates(12,0)
            self.estadoBot2 = 0

    def run(self):
        self.srvr.Vars()
        self.window = Tk()
        self.window.protocol("WM_DELETE_WINDOW", self.callback)
        self.window.geometry('1280x750+105+25')
        self.window.title("Smart Factory by E3T")
        self.window.iconbitmap('LogoSF.ico')
        self.window.columnconfigure(0, weight=1)
        self.window.columnconfigure(1, weight=1)
        self.window.columnconfigure(2, weight=1)
        self.window.columnconfigure(3, weight=1)
        self.window.columnconfigure(4, weight=1)
        self.window.columnconfigure(5, weight=1)
        self.window.columnconfigure(6, weight=1)
        self.window.columnconfigure(7, weight=1)
        self.window.columnconfigure(8, weight=1)
        self.window.columnconfigure(9, weight=1)
        self.window.columnconfigure(10, weight=1)

        self.window.rowconfigure(0, weight=1)
        self.window.rowconfigure(1, weight=1)
        self.window.rowconfigure(2, weight=1)
        self.window.rowconfigure(3, weight=1)
        self.window.rowconfigure(4, weight=1)
        self.window.rowconfigure(5, weight=1)
        self.window.rowconfigure(6, weight=1)
        self.window.rowconfigure(7, weight=1)
        self.window.rowconfigure(8, weight=1)
        self.window.rowconfigure(9, weight=1)
        self.window.rowconfigure(10, weight=1)
        self.window.rowconfigure(11, weight=1)
        self.window.rowconfigure(12, weight=1)
        self.window.rowconfigure(13, weight=1)
        self.window.rowconfigure(14, weight=1)
        imgLogo = ImageTk.PhotoImage(Image.open("LogoSF.jpg").resize((115,115)))
        Logo = Label(self.window, image=imgLogo)
        Logo.image = imgLogo
        Titulo1 = Label(self.window, text='S M A R T   FACTORY', font=("Bahnschrift SemiCondensed", 60))
        Titulo2 = Label(self.window, text='... by T1,3,5', font=("Bradley Hand ITC", 22, "bold", "italic"))
        Logo.grid(row=0, column=0)
        Titulo1.grid(row=0, column=1, columnspan=6, sticky=W)
        Titulo2.grid(row=0, column=2, sticky=S+E)
        self.Status = Label(self.window, text="Status", font=("Bahnschrift", 30),
        fg=self.srvr.statusCol)
        self.Status.grid(row=0, column=8, sticky=N+W)
        self.TxtStatus = StringVar()
        self.TxtStatus.set(self.srvr.statusTxt)
        self.StatusTxt = Label(self.window, textvariable=self.TxtStatus, font=("Bahnschrift", 25),
        fg=self.srvr.statusCol)
        self.canvasStatInd = Canvas(self.window, width=70, height=70)
        self.oval = self.canvasStatInd.create_oval(5,5,65,65, fill=self.srvr.statusCol,outline=self.srvr.statusCol)
        self.canvasStatInd.grid(row=0, column=7)
        self.StatusTxt.grid(row=0, column=8, pady=50)
        ### Tabla Info Robots ###
        LabelRobot = Label(self.window, text="Robots", font=("Bahnschrift", 30))
        LabelRobot.grid(row=1, column=3, columnspan=2)
        self.LabelxMART1 = Label(self.window, text="xMART 1", font=("Bahnschrift", 20), fg=self.srvr.colorx1)
        self.LabelxMART2 = Label(self.window, text="xMART 2", font=("Bahnschrift", 20), fg=self.srvr.colorx2)
        LabelOMRON = Label(self.window, text="OMRON", font=("Bahnschrift", 20))
        self.LabelxMART1.grid(row=3, column=0)
        self.LabelxMART2.grid(row=4, column=0)
        LabelOMRON.grid(row=5, column=0)
        LabelTitRobot = Label(self.window, text="Robot", font=("Bahnschrift", 15))
        LabelTitRS = Label(self.window, text="Robot Status", font=("Bahnschrift", 15))
        LabelTitMS = Label(self.window, text="Mission Status", font=("Bahnschrift", 15))
        LabelTitBattery = Label(self.window, text="Battery", font=("Bahnschrift", 15))
        LabelTitGoalX = Label(self.window, text="Goal X", font=("Bahnschrift", 15))
        LabelTitGoalY = Label(self.window, text="Goal Y", font=("Bahnschrift", 15))
        LabelTitCurrX = Label(self.window, text="Current X", font=("Bahnschrift", 15))
        LabelTitCurrY = Label(self.window, text="Current Y", font=("Bahnschrift", 15))
        LabelTitDis2G = Label(self.window, text="Distance to Goal", font=("Bahnschrift", 15))
        self.txtBot1 = StringVar()
        self.txtBot2 = StringVar()
        self.txtBot1.set("Desactivar")
        self.txtBot2.set("Desactivar")
        self.DeactSMART1 = Button(self.window, textvariable=self.txtBot1, command=self.changeBot1, font=("Bahnschrift", 10))
        self.DeactSMART2 = Button(self.window, textvariable=self.txtBot2, command=self.changeBot2, font=("Bahnschrift", 10))
        LabelTitRobot.grid(row=2 ,column=0)
        LabelTitRS.grid(row=2 ,column=1)
        LabelTitMS.grid(row=2 ,column=2)
        LabelTitBattery.grid(row=2 ,column=3)
        LabelTitGoalX.grid(row=2 ,column=4)
        LabelTitGoalY.grid(row=2 ,column=5)
        LabelTitCurrX.grid(row=2 ,column=6)
        LabelTitCurrY.grid(row=2 ,column=7)
        LabelTitDis2G.grid(row=2 ,column=8)
        self.DeactSMART1.grid(row=3, column=9)
        self.DeactSMART2.grid(row=4, column=9)
        sep1 = ttk.Separator(self.window, orient='horizontal')
        sep2 = ttk.Separator(self.window, orient='horizontal')
        sep3 = ttk.Separator(self.window, orient='horizontal')
        sep4 = ttk.Separator(self.window, orient='horizontal')
        sep5 = ttk.Separator(self.window, orient='horizontal')
        sep6 = ttk.Separator(self.window, orient='vertical')
        sep7 = ttk.Separator(self.window, orient='vertical')
        sep8 = ttk.Separator(self.window, orient='vertical')
        sep9 = ttk.Separator(self.window, orient='vertical')
        sep10 = ttk.Separator(self.window, orient='vertical')
        sep11 = ttk.Separator(self.window, orient='vertical')
        sep12 = ttk.Separator(self.window, orient='vertical')
        sep13 = ttk.Separator(self.window, orient='vertical')
        sep30 = ttk.Separator(self.window, orient='vertical')
        sep1.grid(row=2, column=0, columnspan=10, sticky=N+E+W)
        sep2.grid(row=2, column=0, columnspan=10, sticky=S+E+W)
        sep3.grid(row=3, column=0, columnspan=10, sticky=S+E+W)
        sep4.grid(row=4, column=0, columnspan=10, sticky=S+E+W)
        sep5.grid(row=5, column=0, columnspan=2, sticky=S+E+W)
        sep6.grid(row=2, column=0, rowspan=4, sticky=N+S+E)
        sep7.grid(row=2, column=1, rowspan=4, sticky=N+S+E)
        sep8.grid(row=2, column=2, rowspan=3, sticky=N+S+E)
        sep9.grid(row=2, column=3, rowspan=3, sticky=N+S+E)
        sep10.grid(row=2, column=4, rowspan=3, sticky=N+S+E)
        sep11.grid(row=2, column=5, rowspan=3, sticky=N+S+E)
        sep12.grid(row=2, column=6, rowspan=3, sticky=N+S+E)
        sep13.grid(row=2, column=7, rowspan=3, sticky=N+S+E)
        sep30.grid(row=2, column=8, rowspan=3, sticky=N+S+E)
        self.x1BattCanvas=Canvas(self.window, width=150, height=55)
        self.x2BattCanvas=Canvas(self.window, width=150, height=55)
        # self.OmBattCanvas=Canvas(self.window, width=150, height=55)
        self.x1BattCanvas.grid(row=3 , column=3)
        self.x2BattCanvas.grid(row=4 , column=3)
        # self.OmBattCanvas.grid(row=5 , column=3)
        self.BattCanvx1=self.x1BattCanvas.create_rectangle(0,0,self.srvr.xBatx1,55,fill=self.srvr.Batx1Col)
        self.BattCanvx2=self.x2BattCanvas.create_rectangle(0,0,self.srvr.xBatx2,55,fill=self.srvr.Batx2Col)
        # self.OmBattCanvas.create_rectangle(0,0,self.srvr.xBatOM,55,fill=self.srvr.BatOmCol)
       
        ### Tabla Info Procesos ###
        LabelProc = Label(self.window, text="Procesos", font=("Bahnschrift", 30))
        LabelProc.grid(row=6, column=3, columnspan=2)
        LabelMod = Label(self.window, text="Modula", font=("Bahnschrift", 20))
        LabelConv = Label(self.window, text="Conveyor", font=("Bahnschrift", 20))
        LabelABB = Label(self.window, text="ABB", font=("Bahnschrift", 20))
        LabelAlmacen = Label(self.window, text="Almacen", font=("Bahnschrift", 20))
        LabelMod.grid(row= 7, column=0, columnspan=2)
        LabelConv.grid(row= 7, column=2, columnspan=2)
        LabelABB.grid(row= 7, column=4, columnspan=2)
        LabelAlmacen.grid(row= 7, column=6, columnspan=2)
        LabelPzasM1 = Label(self.window, text="Piezas en", font=("Bahnschrift", 15))
        LabelPzasM2 = Label(self.window, text="Modula", font=("Bahnschrift", 15))
        LabelEstadoC1 = Label(self.window, text="Estado", font=("Bahnschrift", 15))
        LabelEstadoC2 = Label(self.window, text="Conveyor", font=("Bahnschrift", 15))
        LabelEstadoABB1 = Label(self.window, text="Estado", font=("Bahnschrift", 15))
        LabelEstadoABB2 = Label(self.window, text="ABB", font=("Bahnschrift", 15))
        LabelPzasAlm1 = Label(self.window, text="Piezas en", font=("Bahnschrift", 15))
        LabelPzasAlm2 = Label(self.window, text="Almacen", font=("Bahnschrift", 15))
        LabelPzasM1.grid(row= 8, column=0, sticky=N, ipady=15)
        LabelPzasM2.grid(row= 8, column=0, sticky=S)
        LabelEstadoC1.grid(row= 8, column=2, sticky=N, ipady=15)
        LabelEstadoC2.grid(row= 8, column=2, sticky=S)
        LabelEstadoABB1.grid(row= 8, column=4, sticky=N, ipady=15)
        LabelEstadoABB2.grid(row= 8, column=4, sticky=S)
        LabelPzasAlm1.grid(row= 8, column=6, sticky=N, ipady=15)
        LabelPzasAlm2.grid(row= 8, column=6, sticky=S)
        sep14 = ttk.Separator(self.window, orient='horizontal')
        sep15 = ttk.Separator(self.window, orient='horizontal')
        sep16 = ttk.Separator(self.window, orient='horizontal')
        sep18 = ttk.Separator(self.window, orient='vertical')
        sep19 = ttk.Separator(self.window, orient='vertical')
        sep20 = ttk.Separator(self.window, orient='vertical')
        sep21 = ttk.Separator(self.window, orient='vertical')
        sep22 = ttk.Separator(self.window, orient='vertical')
        sep23 = ttk.Separator(self.window, orient='vertical')
        sep24 = ttk.Separator(self.window, orient='vertical')
        sep25 = ttk.Separator(self.window, orient='vertical')
        sep14.grid(row=7, column=0, columnspan=10, sticky=N+E+W)
        sep15.grid(row=7, column=0, columnspan=10, sticky=S+E+W)
        sep16.grid(row=8, column=0, columnspan=8, sticky=S+E+W)
        sep18.grid(row=8, column=0, rowspan=1, sticky=E+N+S)
        sep19.grid(row=7, column=1, rowspan=2, sticky=E+N+S)
        sep20.grid(row=8, column=2, rowspan=1, sticky=E+N+S)
        sep21.grid(row=7, column=3, rowspan=2, sticky=E+N+S)
        sep22.grid(row=8, column=4, rowspan=1, sticky=E+N+S)
        sep23.grid(row=7, column=5, rowspan=2, sticky=E+N+S)
        sep24.grid(row=8, column=6, rowspan=1, sticky=E+N+S)
        sep25.grid(row=7, column=7, rowspan=2, sticky=E+N+S)
        ### Labels de los datos de Servidor ###
            #Declaracion de variables
        self.txtRSx1 = StringVar()
        self.txtMSx1 = StringVar()
        self.txtGXx1 = StringVar()
        self.txtGYx1 = StringVar()
        self.txtCXx1 = StringVar()
        self.txtCYx1 = StringVar()
        self.txtD2Gx1 = StringVar()
        self.txtRSx2 = StringVar()
        self.txtMSx2 = StringVar()
        self.txtGXx2 = StringVar()
        self.txtGYx2 = StringVar()
        self.txtCXx2 = StringVar()
        self.txtCYx2 = StringVar()
        self.txtD2Gx2 = StringVar()
        self.txtRSOM = StringVar()
        # txtMSOM = StringVar()        
        # txtGXOM = StringVar()
        # txtGYOM = StringVar()
        # txtCXOM = StringVar()
        # txtCYOM = StringVar()
        # txtD2GOM = StringVar()
        self.txtPzasMod = StringVar()
        self.txtStatConv = StringVar()
        self.txtStatABB = StringVar()
        self.txtPzasAlm = StringVar()
            #Escritura de variables
        self.txtRSx1.set(self.srvr.RSx1)
        self.txtMSx1.set(self.srvr.MSx1)
        self.txtGXx1.set(self.srvr.GXx1)
        self.txtGYx1.set(self.srvr.GYx1)
        self.txtCXx1.set(self.srvr.CXx1)
        self.txtCYx1.set(self.srvr.CYx1)
        self.txtD2Gx1.set(self.srvr.distSMART1) 
        self.txtRSx2.set(self.srvr.RSx2)
        self.txtMSx2.set(self.srvr.MSx2)
        self.txtGXx2.set(self.srvr.GXx2)
        self.txtGYx2.set(self.srvr.GYx2)
        self.txtCXx2.set(self.srvr.CXx2)
        self.txtCYx2.set(self.srvr.CYx2)
        self.txtD2Gx2.set(self.srvr.distSMART2) 
        self.txtRSOM.set(self.srvr.RSOM)
        # txtMSOM.set(self.srvr.MSOM)
        # txtGXOM.set(self.srvr.GXOM)
        # txtGYOM.set(self.srvr.GYOM)
        # txtCXOM.set(self.srvr.CXOM)
        # txtCYOM.set(self.srvr.CYOM)
        # txtD2GOM.set(self.srvr.RSOM) ###
        self.txtPzasMod.set(self.srvr.PzasMod)
        self.txtStatConv.set(self.srvr.StatConv)
        self.txtStatABB.set(self.srvr.StatABB)
        self.txtPzasAlm.set(self.srvr.PzasAlm)
            #Configuracion de Labels
        LabRSx1 = Label(self.window, textvariable=self.txtRSx1, font=("Bahnschrift", 15))
        LabMSx1 = Label(self.window, textvariable=self.txtMSx1, font=("Bahnschrift", 15))
        self.txtBatt1=self.x1BattCanvas.create_text(75,27.5,text=(str(self.srvr.Batx1) + " %"), font=("Bahnschrift", 15))
        LabGXx1 = Label(self.window, textvariable=self.txtGXx1, font=("Bahnschrift", 15))
        LabGYx1 = Label(self.window, textvariable=self.txtGYx1, font=("Bahnschrift", 15))
        LabCXx1 = Label(self.window, textvariable=self.txtCXx1, font=("Bahnschrift", 15))
        LabCYx1 = Label(self.window, textvariable=self.txtCYx1, font=("Bahnschrift", 15))
        LabD2Gx1 = Label(self.window, textvariable=self.txtD2Gx1, font=("Bahnschrift", 15))
        LabRSx2 = Label(self.window, textvariable=self.txtRSx2, font=("Bahnschrift", 15))
        LabMSx2 = Label(self.window, textvariable=self.txtMSx2, font=("Bahnschrift", 15))
        self.txtBatt2=self.x2BattCanvas.create_text(75,27.5,text=(str(self.srvr.Batx2) + " %"), font=("Bahnschrift", 15))
        LabGXx2 = Label(self.window, textvariable=self.txtGXx2, font=("Bahnschrift", 15))
        LabGYx2 = Label(self.window, textvariable=self.txtGYx2, font=("Bahnschrift", 15))
        LabCXx2 = Label(self.window, textvariable=self.txtCXx2, font=("Bahnschrift", 15))
        LabCYx2 = Label(self.window, textvariable=self.txtCYx2, font=("Bahnschrift", 15))
        LabD2Gx2 = Label(self.window, textvariable=self.txtD2Gx2, font=("Bahnschrift", 15))
        LabRSOM = Label(self.window, textvariable=self.txtRSOM, font=("Bahnschrift", 15))
        # LabMSOM = Label(self.window, textvariable=self.txtMSOM, font=("Bahnschrift", 15))
        # self.OmBattCanvas.create_text(75,27.5,text=(str(self.srvr.BatOM) + " %"), font=("Bahnschrift", 15))
        # LabGXOM = Label(self.window, textvariable=self.txtGXOM, font=("Bahnschrift", 15))
        # LabGYOM = Label(self.window, textvariable=self.txtGYOM, font=("Bahnschrift", 15))
        # LabCXOM = Label(self.window, textvariable=self.txtCXOM, font=("Bahnschrift", 15))
        # LabCYOM = Label(self.window, textvariable=self.txtCYOM, font=("Bahnschrift", 15))
        # LabD2GOM = Label(self.window, textvariable=self.txtD2GOM, font=("Bahnschrift", 15))
        LabPzasMod = Label(self.window, textvariable=self.txtPzasMod, font=("Bahnschrift", 15))
        LabStatConv = Label(self.window, textvariable=self.txtStatConv, font=("Bahnschrift", 15))
        LabStatABB = Label(self.window, textvariable=self.txtStatABB, font=("Bahnschrift", 15))
        LabPzasAlm = Label(self.window, textvariable=self.txtPzasAlm, font=("Bahnschrift", 15))
            #Placement de Labels
        LabRSx1.grid(row=3 ,column=1 )
        LabMSx1.grid(row=3 ,column=2 )
        LabGXx1.grid(row=3 ,column=4 )
        LabGYx1.grid(row=3 ,column=5 )
        LabCXx1.grid(row=3 ,column=6 )
        LabCYx1.grid(row=3 ,column=7 )
        LabD2Gx1.grid(row=3 ,column=8 )
        LabRSx2.grid(row=4 ,column=1 )
        LabMSx2.grid(row=4 ,column=2 )
        LabGXx2.grid(row=4 ,column=4 )
        LabGYx2.grid(row=4 ,column=5 )
        LabCXx2.grid(row=4 ,column=6 )
        LabCYx2.grid(row=4 ,column=7 )
        LabD2Gx2.grid(row=4 ,column=8 )
        LabRSOM.grid(row=5 ,column=1 )
        # LabMSOM.grid(row=5 ,column=2 )
        # LabGXOM.grid(row=5 ,column=4 )
        # LabGYOM.grid(row=5 ,column=5 )
        # LabCXOM.grid(row=5 ,column=6 )
        # LabCYOM.grid(row=5 ,column=7 )
        # LabD2GOM.grid(row=5 ,column=8 )
        LabPzasMod.grid(row=8 , column=1)
        LabStatConv.grid(row=8 , column=3)
        LabStatABB.grid(row=8 , column=5)
        LabPzasAlm.grid(row=8 , column=7)
        self.window.mainloop()
        


CW = ControlWindow()
time.sleep(1)
while True:
    try:
        if CW.window.winfo_exists():
            CW.update()
    except:
        exit()

