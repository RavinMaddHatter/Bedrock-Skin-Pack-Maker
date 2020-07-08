import json
import uuid
import os
from shutil import copyfile
from zipfile import ZipFile
import random
from tkinter import *
import string
from tkinter import ttk
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import askdirectory
import json
from tkinter import filedialog
import shutil

lang={}




    

class skinDialog:
    def __init__(self,master,nameVar,pictureFileVar):
        top=self.top=Toplevel(master)
        rt=0
        self.l=Label(top,text="Name",justify=LEFT).grid(row=rt,column=1)
        Entry(master=top,textvariable=nameVar,width=37,borderwidth=1).grid(row=rt,column=2,columnspan=2)
        rt+=1
        self.l=Label(top,text="file",justify=LEFT).grid(row=rt,column=1)
        Entry(top,textvariable=pictureFileVar,width=30,borderwidth=1).grid(row=rt,column=2)
        Button(top,text="Browse",command=lambda: self.browseSkin(pictureFileVar)).grid(row=rt,column=3)
        rt+=1
        Button(top,text='Done',command=self.cleanup).grid(row=rt,column=3)
    def browseSkin(self,pathVar):
        pathVar.set(askopenfilename(master=self.top, title="Browse for Skin",filetypes =(("Skin File", "*.png"),
                                                                             ("All Files","*.*"))))
        self.top.lift()
    def cleanup(self):
        ##self.value=self.e.get()
        self.top.destroy()
class mainWindow:
    def __init__(self,master):
        self.PackLanName=''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(5))
        self.skins=[]
        self.LangPack=[]
        self.master=master
        self.master.title("Skin Pack maker")
        self.workingDir = StringVar()
        self.workingDir.set("temp")
        workingDir=self.workingDir
        self.packName = StringVar()
        self.relVersion = StringVar()
        relVersion=self.relVersion
        self.subVersion = StringVar()
        subVersion=self.subVersion
        minorVersion = StringVar()
        self.minorVersion=minorVersion
        description=StringVar()
        self.description=description
        self.uuid1=None
        self.uuid2=None
        self.uuid3=None
        self.uuid4=None
        r=0

        Label(self.master, text="Working Directory",borderwidth=1, justify=LEFT).grid(row=r,column=1)
        Entry(self.master, textvariable=workingDir,borderwidth=1, width=40).grid(row=r,column=2,columnspan=3)
        Button(self.master, text="Browse",command=self.browseWorkingDir,borderwidth=1 ).grid(row=r,column=5)

        r+=1

        Label(self.master, text="Name",borderwidth=1,justify=LEFT ).grid(row=r,column=1)
        Entry(self.master, textvariable=self.packName,borderwidth=1,width=47).grid(row=r,column=2,columnspan=4)
        r+=1

        Label(self.master, text="Version",borderwidth=1,justify=LEFT ).grid(row=r,column=1)
        Entry(self.master, textvariable=relVersion,borderwidth=1,width=3).grid(row=r,column=2)
        Entry(self.master, textvariable=subVersion,borderwidth=1,width=3).grid(row=r,column=3)
        Entry(self.master, textvariable=minorVersion,borderwidth=1,width=3).grid(row=r,column=4)

        r+=1

        Label(self.master, text="Description",borderwidth=1,justify=LEFT ).grid(row=r,column=1)
        Entry (self.master, textvariable=description,borderwidth=1,width=47).grid(row=r,column=2,columnspan=4)

        r+=1
        Label(self.master, text="Skins",borderwidth=1,justify=LEFT ).grid(row=r,column=1)
        self.listbox = Listbox(self.master)
        self.listbox.grid(row=r,column=2,columnspan=3,rowspan=4)
        self.addButton=Button(self.master, text="Add Skin",command=lambda: self.addSkin(self.listbox))
        self.addButton.grid(row=r,column=5)
        r+=1
        self.delButton=Button(self.master, text="Delete",command=self.deleteSkin ).grid(row=r,column=5)
        r+=1
        self.loadButton=Button(self.master, text="Import",command=self.loadOldPack ).grid(row=r,column=5)
        r+=1
        self.delButton=Button(self.master, text="Export",command=self.export ).grid(row=r,column=5)
    def browseWorkingDir(self):
        name = askdirectory(title="Working Folder")
        self.workingDir.set(name)
    def export(self):
        if len(self.skins)>0:
            subVersion=self.subVersion
            relVersion=self.relVersion
            minorVersion=self.minorVersion
            description=self.description
            manifest={}
            if self.uuid1==None:
                self.uuid1=str(uuid.uuid1())
            if self.uuid2==None:
                self.uuid2=str(uuid.uuid1())
            
            if self.uuid3==None:
                self.uuid3=str(uuid.uuid1())
            if self.uuid4==None:
                self.uuid4=str(uuid.uuid1())
            manifest["format_version"]=1
            manifest["header"]={}
            manifest["header"]["name"]=self.packName.get()
            manifest["header"]["uuid"]=self.uuid1
            manifest["header"]["version"]=[int(relVersion.get()),int(subVersion.get()),int(minorVersion.get())]
            manifest["modules"]=[]
            manifest["modules"].append({})

            manifest["modules"][0]["type"]="skin_pack"
            manifest["modules"][0]["uuid"]=self.uuid2
            manifest["modules"][0]["version"]=[int(relVersion.get()),int(subVersion.get()),int(minorVersion.get())]

            pack_manifest={}
            pack_manifest["header"]={}
            pack_manifest["header"]["pack_id"]=self.uuid4
            pack_manifest["header"]["name"]=self.packName.get()
            pack_manifest["header"]["packs_version"]=str(relVersion.get())+"."+str(subVersion.get())+"."+str(minorVersion.get())
            pack_manifest["header"]["description"]=self.description.get()
            pack_manifest["header"]["modules"]=[]
            pack_manifest["header"]["modules"].append({})
            pack_manifest["header"]["modules"][0]["description"]="description"
            pack_manifest["header"]["modules"][0]["version"]=str(relVersion.get())+"."+str(subVersion.get())+"."+str(minorVersion.get())
            pack_manifest["header"]["modules"][0]["uuid"]=self.uuid4
            pack_manifest["header"]["modules"][0]["type"]="skin_pack"
            
            skins={}
            skins["geometry"]= "skinpacks/skins.json"
            skins["skins"]= self.skins
            skins["serialize_name"]= "name"
            skins["localization_name"]= self.PackLanName
            with open(os.path.join(self.workingDir.get(),'manifest.json'), 'w+') as outfile:
                json.dump(manifest,outfile,indent=4)
            with open(os.path.join(self.workingDir.get(),'pack_manifest.json'), 'w+') as outfile:
                json.dump(pack_manifest,outfile,indent=4)
            with open(os.path.join(self.workingDir.get(),'skins.json'), 'w+') as outfile:
                json.dump(skins,outfile,indent=4)
            try:
                os.mkdir(os.path.join(self.workingDir.get(),"texts"))
            except:
                pass
            self.LangPack.append("skinpack."+self.PackLanName+"= "+self.packName.get())
            if self.workingDir.get()=="temp":
                self.workingDir.set(os.path.join(os.getcwd(),"temp"))
            with open(os.path.join(self.workingDir.get(),"texts","en_us.lang"),"w+") as outfile:
                for L in self.LangPack:
                    outfile.writelines(L)
            os.chdir(self.workingDir.get())
            file_paths = self.get_all_file_paths(self.workingDir.get())
            with ZipFile(os.path.join(self.workingDir.get(),self.packName.get()+".mcpack"),'x') as zip: 
                # writing each file one by one 
                for file in file_paths:
                    file=file.replace(os.path.join(self.workingDir.get(),""),"")
                    print(file)
                    zip.write(file)
            self.PackLanName=''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(5))
            self.uuid1=None
            self.uuid2=None
            self.uuid3=None
            self.uuid4=None
    def loadOldPack(self):
        zipFile=filedialog.askopenfilename(filetypes = (("World files", "*.mcpack"),))
        path_to_save=self.workingDir.get()
        print(path_to_save)
        if not os.path.isdir(path_to_save):#make a temp folder to work out of
            os.mkdir(path_to_save)
        elif path_to_save=="temp":
            for filename in os.listdir(path_to_save):
                file_path = os.path.join(path_to_save, filename)
                try:
                    if os.path.isfile(file_path) or os.path.islink(file_path):
                        os.unlink(file_path)
                    elif os.path.isdir(file_path):
                        shutil.rmtree(file_path)
                except Exception as e:
                    print('Failed to delete %s. Reason: %s' % (file_path, e))
        with ZipFile(zipFile, 'r') as zipObj:
            zipObj.extractall(path_to_save)
        with open(os.path.join(self.workingDir.get(),'pack_manifest.json'),'r') as json_file:
            data = json.load(json_file)
            self.packName.set(data["header"]["name"])
            self.uuid1=data["header"]["modules"][0]["uuid"]
            version=data["header"]["modules"][0]["version"]
            
            version=version.replace("[","").replace("]","")
            version=version.split(".")
            print(version)
            self.subVersion.set(version[1])
            self.relVersion.set(version[0])
            self.minorVersion.set(version[2])
            self.description.set(data["header"]["description"])
            self.packName.set(data["header"]["name"])
        with open(os.path.join(self.workingDir.get(),'manifest.json'),'r') as json_file:
            data = json.load(json_file)
            self.uuid1=data["header"]["uuid"]
            self.uuid2=data["modules"][0]["uuid"]
        with open(os.path.join(self.workingDir.get(),'skins.json'),'r') as json_file:
            data = json.load(json_file)
            self.skins=data["skins"]
            self.PackLanName=data["localization_name"]
        for skinName in self.skins:
            self.listbox.insert(END,skinName["localization_name"])
    def get_all_file_paths(self,directory): 
  
        # initializing empty file paths list 
        file_paths = [] 
      
        # crawling through directory and subdirectories 
        for root, directories, files in os.walk(directory): 
            for filename in files: 
                # join the two strings in order to form the full filepath. 
                filepath = os.path.join(root, filename) 
                file_paths.append(filepath) 
      
        # returning all file paths 
        return file_paths
    def deleteSkin(self):
        items = self.listbox.curselection()
        if len(items)>0:
            self.skins.pop(items[0])
            self.listbox.delete(ANCHOR)
    def addSkin(self,lb):
        
        name=StringVar()
        path=StringVar()
        w=skinDialog(root,name,path)
        self.addButton["state"]="disabled"
        root.wait_window(w.top)
        self.addButton["state"] = "normal"
        if len(name.get())>0 and len(path.get())>0:
            self.LangPack.append("skin."+self.PackLanName+"."+name.get().replace(' ',"")+"= "+name.get()+"\n")
            self.skins.append({
                "localization_name":name.get().replace(' ',""),
                "geometry":"geometry.humanoid.custom",
                "texture":os.path.basename(path.get()),
                "type":"free"
                })
            lb.insert(END,name.get())
            print(path.get())
            print(self.workingDir.get())
            print(os.path.basename(path.get()))
            newName=os.path.join(self.workingDir.get(),os.path.basename(path.get()))
            print(newName)
            copyfile(path.get(), newName)
            print(path.get())
        
            

root = Tk()
m=mainWindow(root)
root.mainloop(  )




