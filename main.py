import os
import shutil
import json
from tkinter import *
from tkinter.filedialog import askopenfilename, askopenfilenames
from tkinter.messagebox import showinfo

root = Tk()

filetypes = (
    (".png", ".png"),
)

icon = ""
posters = []
tips = []

name = StringVar()
name.set("")
version = StringVar()
version.set("1.0.0")
URL = StringVar()
URL.set("https://x.com/CanigouStudio")
description = StringVar()
description.set("Un super mod")

def selIconFile() :
    global icon

    filenames = askopenfilename(title="Selectionner un fichier", initialdir='Images', filetypes=filetypes)
    icon = filenames

def selPostersSetFiles() :
    global posters

    filenames = askopenfilenames(title="Selectionner des fichiers", initialdir='Images', filetypes=filetypes)
    posters = filenames

def selUniquePostersSetFiles() :
    global tips

    filenames = askopenfilenames(title="Selectionner des fichiers", initialdir='Images', filetypes=filetypes)
    tips = filenames

def buildMod() :
    global name, version, URL, description, icon, posters, tips
    if name.get() != "":
        try:
            modFolderName = name.get() + "-" + version.get()
            os.mkdir(modFolderName)
            os.makedirs(modFolderName + "/BepInEx/plugins/LethalPosters/tips")
            os.makedirs(modFolderName + "/BepInEx/plugins/LethalPosters/posters")

            if icon != "" :
                shutil.copy(icon, modFolderName)
                os.replace(f"{modFolderName}/{icon.split("/")[-1]}", f"{modFolderName}/icon.png")
            else :
                showinfo(title="Error", message="No icon file selected")
                return

            if len(posters) <= 0 & len(tips) <= 0 :
                showinfo(title="Error", message="No custom posters set and no custom tips poster")

            if len(posters) > 0 :
                for p in posters :
                    shutil.copy(p, modFolderName + "/BepInEx/plugins/LethalPosters/posters")

            if len(tips) > 0 :
                for t in tips :
                    shutil.copy(t, modFolderName + "/BepInEx/plugins/LethalPosters/tips")

            readme = open(modFolderName + "/README.md", "w")
            readme.write(">Don't forget to edit this file")
            readme.close()

            changelog = open(modFolderName + "/CHANGELOG.md", "w")
            changelog.write(f"### {version.get()}  \n- Don't forget to edit this file")
            changelog.close()

            json_dictionnary = {
                "name": name.get(),
                "version_number": version.get(),
                "website_url": URL.get(),
                "description": description.get(),
                "dependencies": ["femboy-LethalPosters-1.2.0"]
            }

            json_object = json.dumps(json_dictionnary, indent=4)

            with open(modFolderName + "/manifest.json", "w") as outfile:
                outfile.write(json_object)

            showinfo(title="Succès", message=f"Mod {name.get()}{version.get()} créé avec succès !\nModifiez les fichiers README & CHANGELOG puis zippez le dossier")

            root.destroy()
        except Exception as e:
            showinfo(title="error", message=e)
            return


# Window Config
root.title('Création de mods posters')
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)
root.minsize(720, 480)

mainframe = Frame(root)
mainframe.grid(column = 0, row = 0, sticky = W+E)
mainframe.grid_columnconfigure(1, weight=1)

label1 = Label(mainframe, text='Nom du mod' + ' :')
label2 = Label(mainframe, text='Version du mod' + ' :')
label3 = Label(mainframe, text='URL du site web' + ' :')
label4 = Label(mainframe, text='Description du mod' + ' :')
label5 = Label(mainframe, text='Icône du mod' + ' :')
label6 = Label(mainframe, text='Groupes d\'affiches du mod' + ' :')
label7 = Label(mainframe, text='Affiches solo du mod' + ' :')

label1.grid(column= 0, row= 0, padx=(0,5), pady= 5, sticky=E)
label2.grid(column= 0, row= 1, padx=(0,5), pady= 5, sticky=E)
label3.grid(column= 0, row= 2, padx=(0,5), pady= 5, sticky=E)
label4.grid(column= 0, row= 3, padx=(0,5), pady= 5, sticky=E)
label5.grid(column= 0, row= 4, padx=(0,5), pady= 5, sticky=E)
label6.grid(column= 0, row= 5, padx=(0,5), pady= 5, sticky=E)
label7.grid(column= 0, row= 6, padx=(0,5), pady= 5, sticky=E)

entry1 = Entry(mainframe, textvariable=name)
entry2 = Entry(mainframe, textvariable=version)
entry3 = Entry(mainframe, textvariable=URL)
entry4 = Entry(mainframe, textvariable=description)
iconfile = Button(mainframe, text="Selectionner un fichier", command=selIconFile)
postersfiles = Button(mainframe, text="Selectionner un fichier", command=selPostersSetFiles)
solofiles = Button(mainframe, text="Selectionner un fichier", command=selUniquePostersSetFiles)

entry1.grid(column= 1, row= 0, padx=(0,5), pady= 5, sticky=W+E)
entry2.grid(column= 1, row= 1, padx=(0,5), pady= 5, sticky=W+E)
entry3.grid(column= 1, row= 2, padx=(0,5), pady= 5, sticky=W+E)
entry4.grid(column= 1, row= 3, padx=(0,5), pady= 5, sticky=W+E)
iconfile.grid(column= 1, row= 4, padx=(0,5), pady= 5, sticky=W+E)
postersfiles.grid(column= 1, row= 5, padx=(0,5), pady= 5, sticky=W+E)
solofiles.grid(column= 1, row= 6, padx=(0,5), pady= 5, sticky=W+E)

buttonframe = Frame(root)
buttonframe.grid(column = 0, row = 1, sticky = W+E+N)
buttonframe.grid_rowconfigure(0, weight=1)
buttonframe.grid_columnconfigure(0, weight=1)

buildButton = Button(buttonframe, text="Créer le mod", command=buildMod)
buildButton.grid(column = 0, row = 0, sticky = W+E+N+S)

root.mainloop()

