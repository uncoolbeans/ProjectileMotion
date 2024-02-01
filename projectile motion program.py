from tkinter import *
from tkinter import messagebox
import customtkinter as ctk
import math
import matplotlib.pyplot as plt
import numpy as np

def switchToNewScreen(oldFrame,newFrame): #general purpose switch screen function
    oldFrame.forget()
    newFrame.pack()
    return
screen3 = None #a9huawho

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("900x700")
        self.title("Projectile Motion Calculator")

        global screen3

        screen2 = dataScreen(self)

        screen1 = introScreen(self,screen2)


        screen1.pack()

def exitProgram(): #ends program
    app.quit()

def startSimulation(oldFrame, data):
    global screen3
    screen3 = simulator(app, data)
    oldFrame.forget()
    screen3.pack()



class introScreen(ctk.CTkFrame):
    def __init__(self, master, nextScreen):
        super().__init__(master)

        def exitProgram():
            master.quit()

        self.titleLabel = ctk.CTkLabel(self, 
                                    text = 'Projectile Motion Calculator', 
                                    fg_color= 'transparent', 
                                    anchor= 'center', 
                                    font = ("Bahnschrift SemiBold",30),
                                    padx = 10, pady=50)
    

        self.beginButton = ctk.CTkButton(self,
                                        text = 'Begin',
                                        font = ("Bahnschrift SemiBold",30),
                                        command = lambda: switchToNewScreen(self, nextScreen),
                                        width = 300, height = 100,
                                     )
        
        self.exitButton = ctk.CTkButton(self,
                                        text = 'Exit',
                                        font = ("Bahnschrift SemiBold",20),
                                        command = exitProgram,
                                        width = 250, height = 100,
                                     )
        self.titleLabel.pack()
        self.beginButton.pack(pady = 10)
        self.exitButton.pack(pady = 10)

class dataScreen(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.screenLabel = ctk.CTkLabel(self,text = 'Enter your parameters', 
                                        fg_color= 'transparent', 
                                        anchor= 'center', 
                                        font = ("Bahnschrift SemiBold",30),
                                        padx = 10, pady=50)
        self.screenLabel.grid(row = 0, column = 0, columnspan = 2, padx = 20)

        self.angleFrame = ctk.CTkFrame(self, width=100)
        angleLabel = ctk.CTkLabel(self.angleFrame,
                                        text = 'Launch angle to horizontal',
                                        font = ("Bahnschrift SemiBold",15),
                                        )
        angleEntry = ctk.CTkEntry(self.angleFrame,
                                       placeholder_text = 'Launch angle',
                                       width=200,
                                       )
        unitSelect = ctk.CTkSegmentedButton(self.angleFrame, values= ['Degrees','Radians'])
        unitSelect.set("Degrees")

        angleLabel.pack()
        angleEntry.pack()
        unitSelect.pack()
        self.angleFrame.grid(row = 1, column = 0, pady = 10)

        self.velocityFrame = ctk.CTkFrame(self, width=100)
        velocityLabel = ctk.CTkLabel(self.velocityFrame,
                                        text = 'Launch velocity',
                                        font = ("Bahnschrift SemiBold",15),
                                        )
        velocityEntry = ctk.CTkEntry(self.velocityFrame,
                                       placeholder_text = 'Launch velocity in m/s',
                                       width=200
                                       )
        velocityLabel.pack()
        velocityEntry.pack()
        self.velocityFrame.grid(row = 2, column = 0, pady = 10)

        self.heightFrame = ctk.CTkFrame(self, width=100)
        heightLabel = ctk.CTkLabel(self.heightFrame,
                                        text = 'Launch Height',
                                        font = ("Bahnschrift SemiBold",15),
                                        )
        heightEntry = ctk.CTkEntry(self.heightFrame,
                                       placeholder_text = 'Launch height',
                                       width=200
                                       )
        heightUnitSelect = ctk.CTkSegmentedButton(self.heightFrame, values= ['Meters','Centimeters'])
        heightUnitSelect.set("Meters")

        heightLabel.pack()
        heightEntry.pack()
        heightUnitSelect.pack()
        self.heightFrame.grid(row = 3, column = 0, pady = 10)

        self.gravityFrame = ctk.CTkFrame(self, width=100)
        gravityLabel = ctk.CTkLabel(self.gravityFrame,
                                        text = 'Gravity',
                                        font = ("Bahnschrift SemiBold",15),
                                        )
        gravityEntry = ctk.CTkEntry(self.gravityFrame,
                                       placeholder_text = 'Set gravity in m/s^2',
                                       width=200
                                       )
        gravityLabel.pack()
        gravityEntry.pack()
        self.gravityFrame.grid(row = 4, column = 0, pady = 10)

        def validate(): #checks and packages data for passing into next frame
            try:
                if unitSelect.get() ==  'Degrees':
                    self.launchAngle = float(angleEntry.get()) * (math.pi/180) #converts all angles to radians
                else:
                    self.launchAngle = float(angleEntry.get())
                self.initalVelocity = float(velocityEntry.get())
                if heightUnitSelect.get() == 'Centimeters':
                    self.launchHeight = float(heightEntry.get())/100 #converts all to meters
                else:
                    self.launchHeight = float(heightEntry.get())
                self.gravity = float(gravityEntry.get())
                self.beginButton.configure(state = 'normal')
            except:
                messagebox.showerror('Input error',"Check that all data is entered correctly!")
                return
        
            self.dataDict = {'angle': self.launchAngle, 'velocity': self.initalVelocity, 'height': self.launchHeight, 'gravity': self.gravity} #dictionary to pass data onto next screen
            print(self.dataDict)


        self.validateButton = ctk.CTkButton(self,
                                text = 'Check data',
                                font = ("Bahnschrift SemiBold",30),
                                command = validate,
                                fg_color = 'green',
                                width = 200, height = 50,
                             )
        self.validateButton.grid(row = 5, column = 0, pady = 10)

        self.beginButton = ctk.CTkButton(self,
                                text = 'Confirm',
                                font = ("Bahnschrift SemiBold",30),
                                fg_color = 'green',
                                width = 300, height = 100,
                                state = 'disabled',
                                command = lambda: startSimulation(self, self.dataDict)
                             )
        
        self.beginButton.grid(row = 6, column = 0, pady = 10)


class simulator(ctk.CTkFrame):
    def __init__(self, master, data):
        super().__init__(master)

        self.angle = data['angle']
        self.initVelocity = data['velocity']
        self.gravity = -data['gravity']
        self.height = data['height']

        ux = self.initVelocity * math.cos(self.angle) #uses radians
        uy = self.initVelocity * math.sin(self.angle)

        self.time = (-uy-math.sqrt((uy**2)-2*self.gravity*self.height))/self.gravity #time to impact
        self.distance = self.time*ux #horizontal distance travelled
        self.maxHeight = self.height + uy*(self.time/2) + 0.5*self.gravity*((self.time/2)**2)

        fig= plt.figure()

        x = np.linspace(0,self.distance,1000)

        y = x*math.tan(self.angle) + (self.gravity*(x**2)) / (2*(ux**2)) + self.height

        fig, ax = plt.subplots()
        ax.plot(x,y)
        plt.show()


app = App()
app.mainloop()


