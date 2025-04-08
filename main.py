import pandas as pd
import tkinter as tk
import updateDB as udb
from tkinter import messagebox
#from time import sleep as slp
from PIL import Image, ImageTk
import urllib.request as rqst
import io


class PokedexUI:
    def __init__(self):
        #typical frontend placeholders
        #self.pokeShow = [(1002, 'chien-pao'), (1003, 'ting-lu'), (1004, 'chi-yu'), (1, 'bulbasaur'), (2, 'ivysaur'), (3, 'venusaur'), (4, 'charmander')]
        #self.pokedata = {'name': 'bulbasaur', 'type1': 'grass', 'type2': 'poison', 'hp': 45, 'attack': 49, 'defense': 49, 'sp_attack': 65, 'sp_defense': 65, 'speed': 45, 'image': 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/1.png', 'cry': 'https://raw.githubusercontent.com/PokeAPI/cries/main/cries/pokemon/latest/1.ogg', 'id': 1}
        
        #database
        db = pd.read_csv('pokeDB.csv', index_col = False) #Note: index_col=False is used to avoid pandas doing his own index
        db = db.set_index('id') #Note 2: don't try multiindexing in the first database you use to learn databases
        self.db = db.replace({float('nan'): None})
        print(self.db) #debugging things i guess
        
        
        #window cooking xD
        self.maxW = 800
        self.maxH = 600
        self.win = tk.Tk()
        self.win.title("Noelveon's pokedex")
        self.win.geometry(f'{self.maxW}x{self.maxH}')
        self.win.configure(bg='#000088')
        self.win.minsize(str(self.maxW), str(self.maxH))
        self.win.maxsize(str(self.maxW), str(self.maxH))
        self.imgSize = (250, 250)
        self.txtAnchor = tk.StringVar()
        self.txtAnchor.set('w')
        self.namescolor = '#95daf8'
        self.datacolor = '#aaaaff'
        
        print('window cooked')
        
        #not dynamic elements
        self.searchtxt = tk.Entry(self.win, bg = 'white', fg = 'black')
        self.searchbtn = tk.Button(self.win, text='Search', fg = 'blue', bg = '#ffffaa', command = self.search)
        self.updatebtn = tk.Button(self.win, text = 'Update DB', fg = 'blue', bg = '#ffffaa', command = self.updateDB)
        self.bg0 = tk.Label(self.win, bg = '#aaaaff')
        self.bg1 = tk.Label(self.win, bg = 'black')
        self.bg2 = tk.Label(self.win, bg = '#ffffaa')
        self.img_border0 = tk.Label(self.win, bg = 'white')
        self.img_border1 = tk.Label(self.win, bg = 'black')
        self.author = tk.Label(self.win, text = 'Made by:\nNoelveon', font = ('bold',25), fg = '#000088', bg = self.datacolor)
        
        #placing of that elements
        self.searchbtn.place(x = self.maxW - 12, y = self.maxH - 20, width = 75, height = 35, anchor='se')
        self.searchtxt.place(x = self.maxW - 97, y = self.maxH - 20, width = 170, height = 35, anchor='se')
        self.updatebtn.place(x = self.maxW - 12, y = 20, width = 100, height = 35, anchor='ne')
        self.bg0.place(x = 20, y = 20, width = 500,height = 560, anchor='nw')
        self.bg1.place(x = 21, y = 21, width = 498,height = 558, anchor='nw')
        self.bg2.place(x = 25, y = 25, width = 490,height = 550, anchor='nw')
        self.img_border0.place(x = 35, y = 35, width = self.imgSize[0], height = self.imgSize[1], anchor = 'nw')
        self.img_border1.place(x = 36, y = 36, width = self.imgSize[0] - 2, height = self.imgSize[1] - 2, anchor = 'nw')
        self.author.place(x = 305, y = self.maxH - 35, width = 200, height = 100, anchor = 'sw')
        
        self.search(1) #collecting data on start
    
    def main(self): #the main function actually is a refresh window function, lol
        self.showImage() #download and use images in local is a posible update
        
        #i made this part of code because i dont want tho show 'nan' in the second type when a pokemon doesnt have second type
        if self.pokedata['type2'] == None:
            type2 = ' '
        else:
            type2 = self.pokedata['type2']
        
        #dynamic interface elements
        self.ppprename = tk.Button(self.win, text=f'{self.pokeShow[0][0]}: {self.pokeShow[0][1]}', bg=self.namescolor, command=lambda: self.btnsearch(-3))
        self.pprename = tk.Button(self.win, text = f'{self.pokeShow[1][0]}: {self.pokeShow[1][1]}', bg = self.namescolor, command=lambda: self.btnsearch(-2))
        self.prename = tk.Button(self.win, text = f'{self.pokeShow[2][0]}: {self.pokeShow[2][1]}', bg = self.namescolor, command=lambda: self.btnsearch(-1))
        self.namebtn = tk.Button(self.win, text = f'{self.pokeShow[3][0]}: {self.pokeShow[3][1]}', bg = self.namescolor)
        self.posname = tk.Button(self.win, text = f'{self.pokeShow[4][0]}: {self.pokeShow[4][1]}', bg = self.namescolor, command=lambda: self.btnsearch(1))
        self.pposname = tk.Button(self.win, text = f'{self.pokeShow[5][0]}: {self.pokeShow[5][1]}', bg = self.namescolor, command=lambda: self.btnsearch(2))
        self.ppposname = tk.Button(self.win, text = f'{self.pokeShow[6][0]}: {self.pokeShow[6][1]}', bg = self.namescolor, command=lambda: self.btnsearch(3))
        
        self.txtname = tk.Label(self.win, text = f'name: {self.pokedata['name']}', font = ('bold', 11), bg = self.datacolor)
        self.txtid = tk.Label(self.win, text = f'pokedex ID: {self.pokedata['id']}', font = ('bold', 15), bg = self.datacolor)
        self.txttype1 = tk.Label(self.win, text = f'first type: {self.pokedata['type1']}', font = ('bold', 15), bg = self.datacolor)
        self.txttype2 = tk.Label(self.win, text = f'second type: {type2}', font = ('bold', 15), bg = self.datacolor)
        
        self.txtstats = tk.Label(self.win, text = f'Base stats:', font = ('bold', 15), bg = self.datacolor)
        self.txthp = tk.Label(self.win, text = f'hp: {self.pokedata['hp']}', font = ('bold', 13), bg = self.datacolor)
        self.txtspeed = tk.Label(self.win, text = f'speed: {self.pokedata['speed']}', font = ('bold', 13), bg = self.datacolor)
        self.txtatk = tk.Label(self.win, text = f'attack: {self.pokedata['attack']}', font = ('bold', 13), bg = self.datacolor)
        self.txtspatk = tk.Label(self.win, text = f'sp_attack: {self.pokedata['sp_attack']}', font = ('bold', 13), bg = self.datacolor)
        self.txtdef = tk.Label(self.win, text = f'defense: {self.pokedata['defense']}', font = ('bold', 13), bg = self.datacolor)
        self.txtspdef = tk.Label(self.win, text = f'sp_defense: {self.pokedata['sp_defense']}', font = ('bold', 11), bg = self.datacolor)
        
        print('elements cooked')
        
        #elements placing
        self.ppprename.place(x = self.maxW - 10, y = self.maxH/2 - 180 - 5, width = 250, height = 50, anchor='e')
        self.pprename.place(x = self.maxW - 13, y = self.maxH/2 - 120 - 5, width = 250, height = 50, anchor='e')
        self.prename.place(x = self.maxW - 15, y = self.maxH/2 - 60 - 5, width = 250, height = 50, anchor='e')
        self.namebtn.place(x = self.maxW - 17, y = self.maxH/2, width = 250, height = 50, anchor='e')
        self.posname.place(x = self.maxW - 15, y = self.maxH/2 + 60 + 5, width = 250, height = 50, anchor='e')
        self.pposname.place(x = self.maxW - 13, y = self.maxH/2 + 120 + 5, width = 250, height = 50, anchor='e')
        self.ppposname.place(x = self.maxW - 10, y = self.maxH/2 + 180 + 5, width = 250, height = 50, anchor='e')
        
        self.pokeImg.place(x = 39, y = 39, width = self.imgSize[0] - 8, height = self.imgSize[1] - 8, anchor = 'nw')
        self.txtname.place(x = 40, y = 305, width = 240, height = 50, anchor = 'nw')
        self.txtid.place(x = 55, y = 373, width = 210, height = 50, anchor = 'nw')
        self.txttype1.place(x = 55, y = 441, width = 210, height = 50, anchor = 'nw')
        self.txttype2.place(x = 55, y = 509, width = 210, height = 50, anchor = 'nw')
        
        self.txtstats.place(x = 300, y = 55, width = 200, height = 50, anchor = 'nw')
        self.txthp.place(x = 320, y = 110, width = 135, height = 50, anchor = 'nw')
        self.txtspeed.place(x = 355, y = 165, width = 135, height = 50, anchor = 'nw')
        self.txtatk.place(x = 320, y = 220, width = 135, height = 50, anchor = 'nw')
        self.txtspatk.place(x = 355, y = 275, width = 135, height = 50, anchor = 'nw')
        self.txtdef.place(x = 320, y = 330, width = 135, height = 50, anchor = 'nw')
        self.txtspdef.place(x = 355, y = 385, width = 135, height = 50, anchor = 'nw')
        
        print('elements placed in the oven')
        
        #text align
        self.ppprename.config(padx = 15, anchor = self.txtAnchor.get())
        self.pprename.config(padx = 15, anchor = self.txtAnchor.get())
        self.prename.config(padx = 15, anchor = self.txtAnchor.get())
        self.namebtn.config(padx = 15, anchor = self.txtAnchor.get())
        self.posname.config(padx = 15, anchor = self.txtAnchor.get())
        self.pposname.config(padx = 15, anchor = self.txtAnchor.get())
        self.ppposname.config(padx = 15, anchor = self.txtAnchor.get())
        
        self.txtname.config(padx = 5, anchor = self.txtAnchor.get())
        self.txtid.config(padx = 5, anchor = self.txtAnchor.get())
        self.txttype1.config(padx = 5, anchor = self.txtAnchor.get())
        self.txttype2.config(padx = 5, anchor = self.txtAnchor.get())
        
        print('text aligned')
        
        #key binding
        self.win.bind('<Up>', lambda event: self.btnsearch(-1))
        self.win.bind('<Down>', lambda event: self.btnsearch(1))
        self.win.bind('<Return>', lambda event: self.search(0))
        
        print('keys binded')
        
        self.win.mainloop()
    
    #this thing is for use the search function with an id relative to the current id
    def btnsearch(self, num):
        temp = int(self.pokedata['id'] + num)
        if temp <= 0:
            temp += 1025
        elif temp > 1025:
            temp -= 1025
        self.search(temp)
    
    def search(self, number = 0): #GG for my hard work doing a working function for searching everything in this code
        row = []
        self.pokedata = {}
        txt = str(self.searchtxt.get()).lower()
        print(f'relative number: {number} with text search: {txt}')
        
        try:
            if number > 0:
                row = self.db.iloc[number - 1]
                self.pokedata = row.to_dict()
                self.pokedata['id'] = number
            else: #i can do an elif but im lazy to do it
                if txt.isnumeric(): #isnumeric() is to separate the search between ID and name in the same input bar
                    row = self.db.iloc[int(txt) - 1]
                    self.pokedata = row.to_dict()
                    self.pokedata['id'] = int(txt)
                else:
                    row = self.db.loc[self.db['name'] == txt]
                    self.pokedata = row.to_dict(orient='records', index=True)[0]
                    self.pokedata['id'] = int(row.index.unique()[0])
            print(row)
        except Exception as e:
            print(f'Error searching data: {e}') #i think 404 is not the only error but xD
        
        if self.pokedata != []:
            self.showPoke()
    
    def showPoke(self): #i think this is the real main function, good luck reading the code ;3
        print(self.pokedata)
        mainID = self.pokedata['id']
        self.pokeShow = []
        names = []
        IDs = []
        
        for i in range(-3, 4):
            temp = mainID + i
            if temp <= 0:
                temp += 1025
            elif temp > 1025:
                temp -= 1025
            
            row = self.db.iloc[temp - 1]
            names.append(row['name'])
            IDs.append(temp)
        
        print(f'names: {names}')
        print(f'IDs: {IDs}')
        for i in range(len(names)):
            self.pokeShow.append((IDs[i], names[i]))
            print(f'{IDs[i]}: {names[i]}')
        
        self.main()
    
    def showImage(self): #obviusly copied from StackOverflow and edited to use it on my code
        try:
            with rqst.urlopen(self.pokedata['image']) as data:
                img = data.read()
            image = Image.open(io.BytesIO(img))
            image = image.resize(self.imgSize)
            photo = ImageTk.PhotoImage(image) #ImageTk is better than native tk photoImage because it can show jpg images and other extensions
            print('image loaded')
        except Exception as e:
            print('Error loading image: ' + str(e))
        self.pokeImg = tk.Label(self.win, image=photo)
        self.pokeImg.image = photo
    
    def updateDB(self): #this function needs debugging when i finish doing the pokedex
        if messagebox.askyesno('Update Database', 'Are you sure you want to update the database?'):
            print('pre-updating DB message')
            messagebox.showwarning('Update Database', 'Press OK and dont close any window')
            
            try:
                udb.update()
                messagebox.showinfo('Update Database', 'Database update succesfull')
            except Exception as e:
                messagebox.showerror('Update Database', 'Database update failed')
                print(f'Fatal error while updating database: {e}')
            
            print('post-updating DB message')

if __name__ == '__main__':
    Pokedex = PokedexUI()
    Pokedex.main()