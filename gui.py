from tkinter import *
from tkinter import filedialog
from tkinter import ttk
import configparser

class GUIframe():
    #self.values = self.tree.item(self.tree.selection())["values"]

    #get values from config and preset widgets accordingly
    def ingest(self):
        if(self.settings["base_path"] == ""):
            self.checker.deselect()
            self.basepath.config(state="disabled")
            self.basebutton.config(state="disabled")
        else:
            self.checker.select()
            self.basepath.config(state="normal")
            self.basepath.delete(0, END)
            self.basepath.insert(0, self.settings["base_path"])
            self.basebutton.config(state="normal")

        self.destpath.delete(0, END)
        self.destpath.insert(0, self.settings["search_path"])

        if(self.settings["loop"] == "true"):
            self.loopcheck.select()
            self.loopInterval.config(state="normal")
            self.loopInterval.delete(0, END)
            self.loopInterval.insert(0, self.settings["delay"])
        else:
            self.loopcheck.deselect()
            self.loopInterval.config(state="disabled")
            
        #insert existing rules into treebox
        for rule in self.rules:
            self.tree.insert('','end','', values=(rule, self.rules[rule]))

    #get settings from widgets and write to config.ini
    def action(self):
        if(self.checkVar.get() == 1):
            self.settings["base_path"] = self.basepath.get()
        else:
            self.settings["base_path"] = ""

        self.settings["search_path"] = self.destpath.get()

        if(self.checkVar2.get() == 1):
            self.settings["loop"] = "true"
        else:
            self.settings["loop"] = "false"

        self.settings["delay"] = self.loopInterval.get()

        self.rules.clear()

        for child in self.tree.get_children():
            pair = self.tree.item(child)["values"]
            self.rules[pair[0]] = pair[1]

        with open("config.ini", "w") as configfile:
            self.config.write(configfile)
            configfile.close()

    #get directory and give to specified widget    
    def setDirectory(self, widget):
        filename = filedialog.askdirectory()

        if(filename):
            widget.delete(0, END)
            widget.insert(0, filename)

    #same as setDirectory, but for the path selector in the
    #toplevel window
    def toplevelhelper(self):
        self.setDirectory(self.topPathEntry)
        self.top.focus()

    #update state of loop interval field upon changing loop checkbox
    def checkChange(self):
        status = self.checkVar.get()
        if(status == 0):
            self.basepath.config(state="disabled")
            self.basebutton.config(state="disabled")
        if(status == 1):
            self.basepath.config(state="normal")
            self.basebutton.config(state="normal")

    #update state of base path field upon changing its checkbox
    def loop_checkChange(self):
        status2 = self.checkVar2.get()
        if(status2 == 0):
            self.loopInterval.config(state="disabled")
        if(status2 == 1):
            self.loopInterval.config(state="normal")

    #add values from toplevel to treebox
    def addAssoc(self):
        self.tree.insert('','end','', values=(self.topExtEntry.get(), self.topPathEntry.get()))
        self.topExtEntry.delete(0, END)
        self.topPathEntry.delete(0, END)

    #remove selected treebox item
    def remover(self):
        self.selected_item = self.tree.selection()[0]
        self.tree.delete(self.selected_item)

    #intialize and show toplevel window
    def toplevel(self):
        
        #create toplevel and initalize widgets
        self.top = Toplevel()
        self.topExtEntry = Entry(self.top)
        self.topPathEntry = Entry(self.top)
        self.topSubmit = Button(self.top, text="Submit", command=lambda: self.addAssoc())
        self.choosePath = Button(self.top, text="Select", command=self.toplevelhelper)

        #create labels and grid widgets
        Label(self.top, text="Extension: ").grid(row=0, column=0, padx=5, pady=5)
        self.topExtEntry.grid(row=0, column=1, padx=5, pady=5)
        Label(self.top, text="Destination: ").grid(row=1, column=0, padx=5, pady=5)
        self.topPathEntry.grid(row=1, column=1, padx=5, pady=5)
        self.choosePath.grid(row=1, column=2, padx=5, pady=5)
        self.topSubmit.grid(row=2, column=1, padx=5, pady=5)
        
        self.top.mainloop()     #start toplevel
        
    
    def __init__(self):
        #initialize configparser and read config.ini
        self.config = configparser.ConfigParser()
        self.config.read("config.ini")
        self.settings = self.config['CONFIGURATION']
        self.rules = self.config['RULES']

        #initialize window
        self.frame = Tk()
        self.frame.title("Andrew's mover")

        #intialize and add widgets
        self.basepath = Entry(state="disabled")
        self.basebutton = Button(state="disabled", text="Select", command=lambda: self.setDirectory(self.basepath))
        self.destpath = Entry()
        self.destbutton = Button(text="Select", command=lambda: self.setDirectory(self.destpath))

        self.checkVar = IntVar()
        self.checker = Checkbutton(variable = self.checkVar, command=lambda: self.checkChange())

        self.tree = ttk.Treeview(columns=("ext", "dest"))
        self.tree['show'] = "headings"
        self.tree.column("ext", width=200)
        self.tree.column("dest", width=200)
        self.tree.heading("ext", text="Extension")
        self.tree.heading("dest", text="Destination")

        self.checkVar2 = IntVar()
        self.loopcheck = Checkbutton(variable = self.checkVar2, command=lambda: self.loop_checkChange())

        self.loopInterval = Entry(state="disabled")

        self.saveButton = Button(text="Save", command=lambda: self.action())

        self.addbutton = Button(text="Add", command=lambda: self.toplevel())
        self.removebutton=Button(text="Remove", command=lambda: self.remover())

        #create labels and grid widgets
        Label(text="Looping ").grid(row=0, column=1, padx=5, pady=5)
        self.loopcheck.grid(row=0, column=0, padx=5, pady=5)
        Label(text="Interval (secs): ").grid(row=0, column=2, padx=5, pady=5)
        self.loopInterval.grid(row=0, column=3, padx=5, pady=5)
        
        self.checker.grid(row=1, column=0, padx=5, pady=5)
        Label(text="Base folder: ").grid(row=1, column=1, padx=5, pady=5)
        self.basepath.grid(row=1, column=2, padx=5, pady=5)
        self.basebutton.grid(row=1, column=3, padx=5, pady=5)

        Label(text="Search folder: ").grid(row=2, column=1, padx=5, pady=5)
        self.destpath.grid(row=2, column=2, padx=5, pady=5)
        self.destbutton.grid(row=2, column=3, padx=5, pady=5)

        self.tree.grid(row=3, rowspan=2, column=0, columnspan=4, padx=5, pady=5)

        self.addbutton.grid(row=3, column=4, padx=5, pady=5)
        self.removebutton.grid(row=4, column=4, padx=5, pady=5)

        self.saveButton.grid(sticky="we", row=5, column=1, columnspan=3, padx=5, pady=5)

        self.ingest()   #run ingest method to get initial values from config.ini
        self.frame.mainloop()   #start window

#if class is run directly, create a GUIframe() object
if __name__ == "__main__":
    g = GUIframe()
        
