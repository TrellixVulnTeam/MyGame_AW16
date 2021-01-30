"""
Programme pour le jeu FOE

Une zone de liste (listbox) a été mise en place pour lister les Gms possédés à la place d'un menu déroulant
(Combobox), car pour ce dernier, lorsqu'on ajoute/supprime un Gm, la liste ne se modifie pas instantanément : il
faut fermer et réouvrir l'application pour que la mise à jour soit faite.

Les modules de python ci-dessous ont été mis dans le fichier setup.py, dans la partie :
packages': ['tkinter', 'sqlite3', 'math', 'webbrowser', 'pickle']

le module tkinter.tix n'est pas reconnu lors de la conversion du fichier python en exécutable. Le répertoire tix8.4.3
qui se trouve dans le chemin suivant désigné ci-après a été copié dans le répertoire exe.win32-3.9 qui se trouve dans
le répertoire build pour l'exécutable du fichier

Éditeur : Laurent REYNAUD
Date : 30/01/2021
"""

# Chemin concerné -> C:\Users\LRCOM\AppData\Local\Programs\Python\Python39-32\tcl

from tkinter import ttk
from tkinter.tix import *
from tkinter import messagebox
import sqlite3  # accès à la base de données
from math import *
import webbrowser  # accès au site
import pickle  # sérialisation nom du joueur + blacklist

root = Tk()
root.title('FOE - GMs')
root.geometry('720x530+0+0')
root.resizable(width=False, height=False)

"""Liaison avec la BD"""
conn = sqlite3.connect('foe.db')
c = conn.cursor()
data = c.execute("""SELECT * FROM foe""")
my_list = []
for record in data:
    my_list.append(record[0])
    my_list.sort(reverse=True)  # trie par ordre croissant

"""Configuration des onglets"""
my_notebook = ttk.Notebook(root)
my_notebook.pack()

"""Configuration des cadres pour chaque onglet"""
my_frame1 = Frame(my_notebook, width=500, height=500)  # onglet 'Mes Gms'
my_frame1.pack(fill='both', expand=1)
my_frame2 = Frame(my_notebook, width=500, height=500)  # onglet 'Investissements'
my_frame2.pack(fill='both', expand=1)
my_frame3 = Frame(my_notebook, width=500, height=500)  # onglet 'Snippe'
my_frame3.pack(fill='both', expand=1)
my_frame4 = Frame(my_notebook, width=500, height=500)  # onglet 'Blacklist'
my_frame4.pack(fill='both', expand=1)

"""Ajout des onglets"""
my_notebook.add(my_frame1, text='Mes Gms')
my_notebook.add(my_frame2, text='Investissements')
my_notebook.add(my_frame3, text='Snippe')
my_notebook.add(my_frame4, text='Blacklist')


class Menus(Menu):
    """Version de l'application et année de création dont le menu apparaît avec le bouton de droite de la souris"""

    def message(self, *args):
        """Message d'information sur la conception de l'application"""
        version = messagebox.showinfo('À propos', "FOE - GMs version 4.0\n\n2021 - Laurent REYNAUD")
        Label(root, text=version).pack()

    def my_popup(self, e):
        """Fonction permettant d'afficher le menu dans la fenêtre selon l'endroit où on a cliqué avec le bouton de
        droite de la souris"""
        self.about.tk_popup(e.x_root, e.y_root)

    def __init__(self, master, **kw):
        super().__init__(master, **kw)

        """Menu 'À propos...'"""
        self.about = Menu(root, tearoff=0)
        self.about.add_command(label='À propos...', command=self.message)

        """Lien avec le bouton de droite de la souris"""
        root.bind('<Button-3>', self.my_popup)


class Gms(Frame):
    """Investissements à opérer sur mes propres Gms pour sécuriser les places (onglet Mes Gms)"""

    def __init__(self, master):
        super().__init__(master)
        self.grid(row=0, column=0, rowspan=2)
        self.widgets()

    def invest_pfs(self, *args):
        """Calcul du nombre de pfs requis pour chaque place de p1 à p5"""

        try:
            """Assignation des données saisies"""
            p1 = int(self.var_p1.get())
            p2 = int(self.var_p2.get())
            p3 = int(self.var_p3.get())
            p4 = int(self.var_p4.get())
            p5 = int(self.var_p5.get())
            summ = int(self.var_sum.get())
            my_invest = int(self.var_invest.get())
            one_more = int(self.var_one_more.get())
            snipe = int(self.var_snippe.get())
            profit = float(self.var_profit.get())

            """Calcul du nombre de pfs à investir pour chaque place : pfs mini place ... x taux de rentabilité"""
            self.res_p1 = ceil(p1 * profit)
            self.res_p2 = ceil(p2 * profit)
            self.res_p3 = ceil(p3 * profit)
            self.res_p4 = ceil(p4 * profit)
            self.res_p5 = ceil(p5 * profit)

            """Insertion dans les variables de contrôle du nombre de pfs requis pour chaque place en fonction du taux de
             rentabilité donné"""
            self.test.delete(1.0, END)
            if self.var_newName.get() == '':
                self.test.insert(END, f'{self.var_name.get()} {self.var_player.get()} p1 à {self.res_p1} pfs\n'
                                      f'{self.var_name.get()} {self.var_player.get()} p2 à {self.res_p2} pfs\n'
                                      f'{self.var_name.get()} {self.var_player.get()} p3 à {self.res_p3} pfs\n'
                                      f'{self.var_name.get()} {self.var_player.get()} p4 à {self.res_p4} pfs\n'
                                      f'{self.var_name.get()} {self.var_player.get()} p5 à {self.res_p5} pfs\n')
            else:
                self.test.insert(END, f'{self.var_name.get()} {self.var_newName.get()} p1 à {self.res_p1} pfs\n'
                                      f'{self.var_name.get()} {self.var_newName.get()} p2 à {self.res_p2} pfs\n'
                                      f'{self.var_name.get()} {self.var_newName.get()} p3 à {self.res_p3} pfs\n'
                                      f'{self.var_name.get()} {self.var_newName.get()} p4 à {self.res_p4} pfs\n'
                                      f'{self.var_name.get()} {self.var_newName.get()} p5 à {self.res_p5} pfs\n')

            """Calcul du nombre de pfs restant à investir pour sécuriser les p1 et p2"""
            minus_p1 = summ - ceil(p1 * 2 * profit) - my_invest - one_more + snipe
            if minus_p1 < 0:
                minus_p1 = 0
            self.var_label_investp1.set(minus_p1)
            self.var_label_investp2.set(minus_p1)

            """Calcul du nombre de pfs restant à investir pour sécuriser la p3"""
            minus_p3 = summ - ceil(p1 * profit) - ceil(p2 * profit) - my_invest - one_more + snipe \
                       - ceil(p3 * profit * 2)
            if minus_p3 < 0:
                minus_p3 = 0
            self.var_label_investp3.set(minus_p3)

            """Calcul du nombre de pfs restant à investir pour sécuriser la p4"""
            minus_p4 = summ - ceil(p1 * profit) - ceil(p2 * profit) - ceil(p3 * profit) - my_invest - one_more \
                       + snipe - ceil(p4 * profit * 2)
            if minus_p4 < 0:
                minus_p4 = 0
            self.var_label_investp4.set(minus_p4)

            """Calcul du nombre de pfs restant à investir pour sécuriser la p5"""
            minus_p5 = summ - ceil(p1 * profit) - ceil(p2 * profit) - ceil(p3 * profit) - ceil(p4 * profit) \
                       - my_invest - one_more + snipe - ceil(p5 * profit * 2)
            if minus_p5 < 0:
                minus_p5 = 0
            self.var_label_investp5.set(minus_p5)
        except ValueError:
            pass

    def change(self):
        """Fonction permettant de modifier les enregistrements de la BD"""

        title = (self.my_listbox.get(ANCHOR),)
        conn = sqlite3.connect('foe.db')
        c = conn.cursor()
        myData = (self.entry_level.get(),
                  self.entry_sum.get(),
                  self.entry_p1.get(),
                  self.entry_p2.get(),
                  self.entry_p3.get(),
                  self.entry_p4.get(),
                  self.entry_p5.get(),
                  self.entry_invest.get(),
                  self.entry_one_more.get(),
                  self.entry_snippe.get(),
                  self.entry_ark.get(),
                  self.entry_name.get())
        c.execute("""UPDATE foe SET Niveau=?, Total=?, P1=?, P2=?, P3=?, P4=?, P5=?, Investis=?, Surplus=?, Snipe=?,
        Arche=? WHERE GM =?""", myData)
        conn.commit()
        conn.close()

    def retrieve(self):
        """Fonction permettant de récupérer les enregistrements de la BD"""

        title = (self.my_listbox.get(ANCHOR),)
        conn = sqlite3.connect('foe.db')
        c = conn.cursor()
        request = c.execute("""SELECT * FROM foe WHERE GM =?""", title)
        res = request.fetchone()
        conn.close()

        """Affichage des données enregistrées avec un try except afin d'éviter d'avoir un message d'erreur si on appuye
        automatiquement sur le bouton 'Récupérer' sans avoir sélectionner le GM concerné dans le menu déroulant"""
        try:
            self.entry_name.delete(0, END)
            self.entry_name.insert(0, res[0])
            self.entry_level.delete(0, END)
            self.entry_level.insert(0, res[1])
            self.entry_sum.delete(0, END)
            self.entry_sum.insert(0, res[2])
            self.entry_p1.delete(0, END)
            self.entry_p1.insert(0, res[3])
            self.entry_p2.delete(0, END)
            self.entry_p2.insert(0, res[4])
            self.entry_p3.delete(0, END)
            self.entry_p3.insert(0, res[5])
            self.entry_p4.delete(0, END)
            self.entry_p4.insert(0, res[6])
            self.entry_p5.delete(0, END)
            self.entry_p5.insert(0, res[7])
            self.entry_invest.delete(0, END)
            self.entry_invest.insert(0, res[8])
            self.entry_one_more.delete(0, END)
            self.entry_one_more.insert(0, res[9])
            self.entry_snippe.delete(0, END)
            self.entry_snippe.insert(0, res[10])
            self.entry_ark.delete(0, END)
            self.entry_ark.insert(0, res[11])
        except TypeError:
            pass

    def append(self):
        """Fonction permettant d'ajouter les enregistrements dans la BD"""

        title = (self.entry_name.get(),)
        conn = sqlite3.connect('foe.db')
        c = conn.cursor()
        request = c.execute("""SELECT * FROM foe WHERE GM =?""", title)
        res = request.fetchone()
        try:
            conn = sqlite3.connect('foe.db')
            c = conn.cursor()
            myData = (self.entry_name.get(),
                      self.entry_level.get(),
                      self.entry_sum.get(),
                      self.entry_p1.get(),
                      self.entry_p2.get(),
                      self.entry_p3.get(),
                      self.entry_p4.get(),
                      self.entry_p5.get(),
                      self.entry_invest.get(),
                      self.entry_one_more.get(),
                      self.entry_snippe.get(),
                      self.entry_ark.get())
            c.execute("""INSERT INTO foe VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", myData)
            conn.commit()
            conn.close()
        except sqlite3.IntegrityError:
            pass

        """Mise à jour de la zone de liste"""
        self.my_listbox.insert(0, self.entry_name.get())

    def delete(self):
        """Fonction permettant de supprimer les enregistrements dans la BD'"""

        try:
            title = (self.my_listbox.get(ANCHOR),)
            conn = sqlite3.connect('foe.db')
            c = conn.cursor()
            c.execute("""DELETE FROM foe WHERE GM =?""", title)
            conn.commit()
            conn.close()
            self.my_listbox.delete(ANCHOR)
            self.entry_name.delete(0, END)
            self.entry_invest.delete(0, END)
            self.entry_one_more.delete(0, END)
            self.entry_snippe.delete(0, END)
            self.entry_level.delete(0, END)
            self.entry_sum.delete(0, END)
            self.entry_p1.delete(0, END)
            self.entry_p2.delete(0, END)
            self.entry_p3.delete(0, END)
            self.entry_p4.delete(0, END)
            self.entry_p5.delete(0, END)
            self.entry_ark.delete(0, END)
        except TclError:
            pass

    def remove(self):
        """Fonction permettant d'effacer les saisies faites dans l'onglet 'Mes Gms'"""
        self.entry_name.delete(0, END)
        self.entry_invest.delete(0, END)
        self.entry_one_more.delete(0, END)
        self.entry_snippe.delete(0, END)
        self.entry_level.delete(0, END)
        self.entry_sum.delete(0, END)
        self.entry_p1.delete(0, END)
        self.entry_p2.delete(0, END)
        self.entry_p3.delete(0, END)
        self.entry_p4.delete(0, END)
        self.entry_p5.delete(0, END)
        self.entry_ark.delete(0, END)

    def game(self, url):
        """Fonction permettant d'accéder au site du jeu"""
        webbrowser.open_new(url)

    def save_file(self):
        """Fonction permettant de sauvegarder le nom du joueur"""

        """Assignation de l'obtention des données saisies dans le champ de saisi"""
        player = self.entry_newName.get()

        """Assignation d'un nom de fichier"""
        file_name = 'player'

        """Assignation de l'ouverture du fichier en mode écriture"""
        output_file = open(file_name, 'wb')

        """Ajout des données de la zone de texte (variable enemies) dans le fichier en mode écriture (variable 
        output_file) """
        pickle.dump(player, output_file)

    def widgets(self):

        """Zone de liste"""
        self.my_listbox = Listbox(self, justify='center', activestyle='none', bd=0, highlightthickness=0,
                                  selectbackground='red', height=20)
        for item in my_list:
            self.my_listbox.insert(0, item)  # affichage de la liste des Gms dans la BD
        self.my_listbox.grid(row=0, column=0, rowspan=13, padx=5, pady=5)

        """Nom du Gm"""
        label_name = Label(self, text='GM')
        label_name.grid(row=0, column=1, padx=5, pady=5)
        self.var_name = StringVar()
        self.entry_name = Entry(self, justify='center', textvariable=self.var_name)
        self.var_name.trace('w', self.invest_pfs)
        self.entry_name.grid(row=0, column=2, pady=5)

        """Pfs investis sur mon GM"""
        label_invest = Label(self, text='Pfs investis')
        label_invest.grid(row=1, column=1, padx=5, pady=5)
        self.var_invest = StringVar()
        self.entry_invest = Entry(self, justify='center', width=20, textvariable=self.var_invest)
        self.var_invest.trace('w', self.invest_pfs)
        self.entry_invest.grid(row=1, column=2, pady=5)

        """Surplus de pfs prise par les autres joueurs sur une place"""
        label_on_more = Label(self, text='Surplus')
        label_on_more.grid(row=2, column=1, padx=5, pady=5)
        self.var_one_more = StringVar()
        self.entry_one_more = Entry(self, justify='center', width=20, textvariable=self.var_one_more)
        self.var_one_more.trace('w', self.invest_pfs)
        self.entry_one_more.grid(row=2, column=2, pady=5)
        tip = Balloon(self)  # info-bulle
        tip.bind_widget(self.entry_one_more, balloonmsg='Surplus versé par les autres joueurs sur une place\nqui ne'
                                                        'peut-être prise par un autre joueur')

        """Pfs snippés"""
        label_snippe = Label(self, text='Pfs snippés')
        label_snippe.grid(row=3, column=1, padx=5, pady=5)
        self.var_snippe = StringVar()
        self.entry_snippe = Entry(self, justify='center', width=20, textvariable=self.var_snippe)
        self.var_snippe.trace('w', self.invest_pfs)
        self.entry_snippe.grid(row=3, column=2, pady=5)

        """Niveau du GM"""
        label_level = Label(self, text='Niveau')
        label_level.grid(row=4, column=1, padx=5, pady=5)
        self.entry_level = Entry(self, justify='center', width=20)
        self.entry_level.grid(row=4, column=2, pady=5)

        """Nombre total de pfs"""
        label_sum = Label(self, text='Total pfs')
        label_sum.grid(row=5, column=1, padx=5, pady=5)
        self.var_sum = StringVar()
        self.entry_sum = Entry(self, justify='center', width=20, textvariable=self.var_sum)
        self.var_sum.trace('w', self.invest_pfs)
        self.entry_sum.grid(row=5, column=2, padx=5, pady=5)

        """Pfs minimum pour la p1"""
        label_p1 = Label(self, text='Pfs mini p1')
        label_p1.grid(row=6, column=1, padx=5, pady=5)
        self.var_p1 = StringVar()
        self.entry_p1 = Entry(self, justify='center', width=20, textvariable=self.var_p1)
        self.var_p1.trace('w', self.invest_pfs)
        self.entry_p1.grid(row=6, column=2, padx=5, pady=5)

        """Pfs minimum pour la p2"""
        label_p2 = Label(self, text='Pfs mini p2')
        label_p2.grid(row=7, column=1, padx=5, pady=5)
        self.var_p2 = StringVar()
        self.entry_p2 = Entry(self, justify='center', width=20, textvariable=self.var_p2)
        self.var_p2.trace('w', self.invest_pfs)
        self.entry_p2.grid(row=7, column=2, padx=5, pady=5)

        """Pfs minimum pour la p3"""
        label_p3 = Label(self, text='Pfs mini p3')
        label_p3.grid(row=8, column=1, padx=5, pady=5)
        self.var_p3 = StringVar()
        self.entry_p3 = Entry(self, justify='center', width=20, textvariable=self.var_p3)
        self.var_p3.trace('w', self.invest_pfs)
        self.entry_p3.grid(row=8, column=2, padx=5, pady=5)

        """Pfs minimum pour la p4"""
        label_p4 = Label(self, text='Pfs mini p4')
        label_p4.grid(row=9, column=1, padx=5, pady=5)
        self.var_p4 = StringVar()
        self.entry_p4 = Entry(self, justify='center', width=20, textvariable=self.var_p4)
        self.var_p4.trace('w', self.invest_pfs)
        self.entry_p4.grid(row=9, column=2, padx=5, pady=5)

        """Pfs minimum pour la p5"""
        label_p5 = Label(self, text='Pfs mini p5')
        label_p5.grid(row=10, column=1, padx=5, pady=5)
        self.var_p5 = StringVar()
        self.entry_p5 = Entry(self, justify='center', width=20, textvariable=self.var_p5)
        self.var_p5.trace('w', self.invest_pfs)
        self.entry_p5.grid(row=10, column=2, padx=5, pady=5)

        """Taux de rentabilité de l'arche"""
        label_ark = Label(self, text='Taux renta arche')
        label_ark.grid(row=11, column=1, padx=5, pady=5)
        self.entry_ark = Entry(self, justify='center', width=20)
        self.entry_ark.grid(row=11, column=2, padx=5, pady=5)

        """Taux de rentabilité"""
        label_profit = Label(self, text='Taux de rentabilité', fg='red')
        label_profit.grid(row=12, column=1, padx=5, pady=5)
        self.var_profit = StringVar()
        entry_profit = Entry(self, justify='center', width=20, fg='red', textvariable=self.var_profit)
        self.var_profit.trace('w', self.invest_pfs)
        entry_profit.insert(0, '1.900')  # valeur paramétrée
        entry_profit.grid(row=12, column=2, padx=5, pady=5)

        """Accès au site du jeu"""
        self.access_game = Label(self, text='Accès au jeu', fg='red', font='helvetica 10 italic bold', bd=1,
                                 relief='groove', width=30)
        self.access_game.bind('<Button-1>', lambda e: self.game('https://fr0.forgeofempires.com/page/'))
        self.access_game.grid(row=0, padx=5, ipadx=20, column=3, columnspan=2, pady=5)

        """Chargement des données du nom actuel du joueur"""
        try:
            file_name = 'player'  # assignation d'un nom de fichier
            input_file = open(file_name, 'rb')  # assignation de l'ouverture du fichier en mode lecture
            player = pickle.load(input_file)  # assignation de la récupération des données sauvegardées
        except FileNotFoundError:
            pass

        """Nom actuel du joueur"""
        label_currentPlayer = Label(self, text='Nom actuel')
        label_currentPlayer.grid(row=1, padx=5, ipadx=20, column=3, columnspan=2, pady=5)
        self.var_player = StringVar()
        self.entry_currentPlayer = Entry(self, justify='center', width=40, textvariable=self.var_player)
        self.var_player.trace('w', self.invest_pfs)  # faire ceci car la variable est appelée dans une autre fonction
        try:
            self.entry_currentPlayer.insert(0, player)  # insertion des données récupérées du fichier sauvegardé
        except UnboundLocalError:
            pass
        self.entry_currentPlayer.grid(row=2, padx=5, ipadx=20, column=3, columnspan=2, pady=5)

        """Nouveau nom du joueur"""
        label_newName = Label(self, text='Nouveau nom')
        label_newName.grid(row=3, padx=5, ipadx=20, column=3, columnspan=2, pady=5)
        self.var_newName = StringVar()
        self.entry_newName = Entry(self, justify='center', width=40, textvariable=self.var_newName)
        self.var_newName.trace('w', self.invest_pfs)   # faire ceci car la variable est appelée dans une autre fonction
        self.entry_newName.grid(row=4, padx=5, ipadx=20, column=3, columnspan=2, pady=5)

        """Bouton de sauvegarde du nouveau nom du joueur"""
        button_player = Button(self, text='Sauvegarder', command=self.save_file)
        button_player.grid(row=5, padx=5, ipadx=30, column=3, columnspan=2, pady=5)

        """Titre des pfs restants à mettre pour sécuriser les places"""
        label_title = Label(self, text='Places à sécuriser', font='Helvetica 10 italic', bd=1, relief='ridge')
        label_title.grid(row=7, column=3, padx=10, ipadx=40, columnspan=2, pady=5)

        """PFs restant pour la p1"""
        label_p1 = Label(self, text='Pfs restant pour la p1', bd=1, relief='ridge')
        label_p1.grid(row=8, column=3, padx=10, ipadx=7, pady=5)
        self.var_label_investp1 = StringVar()
        label_investp1 = Label(self, textvariable=self.var_label_investp1, width=5, bd=1, relief='ridge')
        label_investp1.grid(row=8, column=4, padx=10, ipadx=7, pady=5)

        """PFs restant pour la p2"""
        label_p2 = Label(self, text='Pfs restant pour la p2', bd=1, relief='ridge')
        label_p2.grid(row=9, column=3, ipadx=7, pady=5)
        self.var_label_investp2 = StringVar()
        label_investp2 = Label(self, textvariable=self.var_label_investp2, width=5, bd=1, relief='ridge')
        label_investp2.grid(row=9, column=4, ipadx=7, pady=5)

        """PFs restant pour la p3"""
        label_p3 = Label(self, text='Pfs restant pour la p3', bd=1, relief='ridge')
        label_p3.grid(row=10, column=3, ipadx=7, pady=5)
        self.var_label_investp3 = StringVar()
        label_investp3 = Label(self, textvariable=self.var_label_investp3, width=5, bd=1, relief='ridge')
        label_investp3.grid(row=10, column=4, ipadx=7, pady=5)

        """PFs restant pour la p4"""
        label_p4 = Label(self, text='Pfs restant pour la p4', bd=1, relief='ridge')
        label_p4.grid(row=11, column=3, ipadx=7, pady=5)
        self.var_label_investp4 = StringVar()
        label_investp4 = Label(self, textvariable=self.var_label_investp4, width=5, bd=1, relief='ridge')
        label_investp4.grid(row=11, column=4, ipadx=7, pady=5)

        """PFs restant pour la p5"""
        label_p5 = Label(self, text='Pfs restant pour la p5', bd=1, relief='ridge')
        label_p5.grid(row=12, column=3, ipadx=7, pady=5)
        self.var_label_investp5 = StringVar()
        label_investp5 = Label(self, textvariable=self.var_label_investp5, width=5, bd=1, relief='ridge')
        label_investp5.grid(row=12, column=4, ipadx=7, pady=5)

        """Zone de texte"""
        self.test = Text(self, height=5, width=40)
        self.test.grid(row=13, padx=5, column=3, rowspan=2, columnspan=2, pady=5)

        """Bouton pour la récupération des données du GM"""
        btn_retrieve = Button(self, text='Récupérer', command=self.retrieve)
        btn_retrieve.grid(row=13, column=0, padx=5, pady=5)

        """Bouton pour la modification des données du GM"""
        btn_update = Button(self, text='Modifier', command=self.change)
        btn_update.grid(row=13, column=1, padx=5, pady=5)

        """Bouton pour effacer la saisie"""
        btn_remove = Button(self, text='Effacer', command=self.remove)
        btn_remove.grid(row=13, column=2, padx=5, pady=5)

        """Bouton pour l'ajout des données du GM"""
        btn_append = Button(self, text='Ajouter', command=self.append)
        btn_append.grid(row=14, column=0, padx=5, pady=5)

        """Bouton pour la suppression des données du GM"""
        btn_delete = Button(self, text='Supprimer', command=self.delete)
        btn_delete.grid(row=14, column=1, padx=5, pady=5)


class Invest(Frame):
    """Investissements pfs auprès des autres joueurs (onglet Investissement)"""

    def __init__(self, master):
        super().__init__(master)
        self.pack()
        self.widgets()

    def invest_friends(self, *args):
        """Fonction permettant de calculer le nombre de pfs à mettre au joueur concerné selon le taux de renta saisi"""
        try:
            tx_invest = float(self.var_otherprofit.get())
            pfs_mini = float(self.var_pfsmini.get())
            tx_renta = float(self.var_txrenta.get())
            res_invest = ceil(pfs_mini * tx_invest)
            res_renta = ceil(pfs_mini * (tx_renta - tx_invest)) - 1
            self.var_pfsresult.set(res_invest)
            self.var_pfsrenta.set(res_renta)
        except ValueError:
            pass

    def widgets(self):

        """Connection à la base de données -> récupération des données de l'Arche"""
        conn = sqlite3.connect('foe.db')
        c = conn.cursor()
        request = c.execute("SELECT * FROM foe WHERE GM = 'Arche'")
        res = request.fetchone()

        """Titre de la fenêtre'"""
        label_title = Label(self, text='Investissements sur GM', font='helvetica 10 italic')
        label_title.grid(row=0, column=0, pady=10, columnspan=2)

        """Taux d'investissement"""
        label_otherprofit = Label(self, text="Taux d'investissement", fg='red')
        label_otherprofit.grid(row=1, column=0, pady=5, padx=10)
        self.var_otherprofit = StringVar()
        entry_otherprofit = Entry(self, justify='center', width=20, fg='red', textvariable=self.var_otherprofit)
        entry_otherprofit.insert(0, '1.900')  # affichage automatique de la renta 1,9 dans le champ de saisi concerné
        self.var_otherprofit.trace('w', self.invest_friends)
        entry_otherprofit.grid(row=1, column=1, padx=5)

        """Pfs minimum à investir"""
        label_pfsmini = Label(self, text='Pfs minimum à investir')
        label_pfsmini.grid(row=2, column=0, pady=5, padx=10)
        self.var_pfsmini = StringVar()
        entry_pfsmini = Entry(self, justify='center', width=20, textvariable=self.var_pfsmini)
        self.var_pfsmini.trace('w', self.invest_friends)
        entry_pfsmini.grid(row=2, column=1, padx=5)

        """Pfs à investir"""
        label_pfsinvest = Label(self, text='Pfs à investir')
        label_pfsinvest.grid(row=3, column=0, pady=5, padx=10)
        self.var_pfsresult = StringVar()
        label_pfsresult = Label(self, justify='center', textvariable=self.var_pfsresult)
        self.var_txrenta = StringVar()
        label_pfsresult.grid(row=3, column=1, padx=5)

        """Taux de rentabilité de l'arche"""
        label_txrenta = Label(self, text="Taux de rentabilité de l'arche")
        label_txrenta.grid(row=4, column=0, pady=5, padx=10)
        entry_txrenta = Entry(self, justify='center', width=20, textvariable=self.var_txrenta)
        entry_txrenta.insert(0, res[11])  # récupération du taux de renta de l'arche dans la base de données
        self.var_txrenta.trace('w', self.invest_friends)
        entry_txrenta.grid(row=4, column=1, padx=5)

        """Info-bulle sur le taux de rentabilité de l'arche"""
        tip = Balloon(self)
        tip.bind_widget(entry_txrenta, balloonmsg="Si le taux de renta de l'arche a été modifié,\n"
                                                  "pour une mise à jour du taux dans ce champ,\n"
                                                  "fermez et réouvrez cette application")

        """Pfs gagné(s)"""
        label_pfsrenta = Label(self, text='Pfs gagnés')
        label_pfsrenta.grid(row=5, column=0, pady=5, padx=10)
        self.var_pfsrenta = StringVar()
        entry_pfsrenta = Entry(self, justify='center', width=20, textvariable=self.var_pfsrenta)
        entry_pfsrenta.grid(row=5, column=1, padx=5)


class Snippe(Frame):
    """Snipe sur les Gms des voisins (onglet Snippe)"""

    def __init__(self, master):
        super().__init__(master)
        self.pack()
        self.widgets()

    def snipper(self, *args):
        """Calcul des pfs à investir pour obtenir des gains sur les Gms des voisins"""
        try:
            my_total = self.var_total.get()
            my_invest = self.var_invest.get()
            my_place = self.var_place.get()
            my_mini = self.var_mini.get()
            my_renta = self.var_renta.get()
            res1 = int(my_total) - int(my_invest)
            self.var_balance.set(res1)
            res2 = ceil((res1 + int(my_place)) / 2)
            self.var_snippe.set(res2)
            res3 = ceil(int(my_mini) * float(my_renta) - res2)
            self.var_win.set(res3)
        except ValueError:
            pass

    def widgets(self):

        """Connection à la base de données -> récupération des données de l'Arche"""
        conn = sqlite3.connect('foe.db')
        c = conn.cursor()
        request = c.execute("SELECT * FROM foe WHERE GM = 'Arche'")
        res = request.fetchone()

        """Titre de la fenêtre'"""
        label_title = Label(self, text='Et pourquoi ne pas snipper ?', font='helvetica 10 italic')
        label_title.grid(row=0, column=0, pady=10, columnspan=2)

        """Total de pfs du GM du voisin"""
        label_total = Label(self, text='Total de Pfs du GM de notre cher voisin')
        label_total.grid(row=1, column=0, pady=5, padx=5)
        self.var_total = StringVar()
        self.entry_total = Entry(self, justify='center', width=20, textvariable=self.var_total)
        self.var_total.trace('w', self.snipper)
        self.entry_total.grid(row=1, column=1)

        """Total de Pfs déjà investis"""
        label_invest = Label(self, text='Total de Pfs déjà investis')
        label_invest.grid(row=2, column=0, pady=5, padx=5)
        self.var_invest = StringVar()
        self.entry_invest = Entry(self, justify='center', width=20, textvariable=self.var_invest)
        self.var_invest.trace('w', self.snipper)
        self.entry_invest.grid(row=2, column=1)

        """Pfs restant à investir"""
        label_balance = Label(self, text='Pfs restant à investir')
        label_balance.grid(row=3, column=0, pady=5, padx=5)
        self.var_balance = StringVar()
        self.res_balance = Label(self, width=20, textvariable=self.var_balance)
        self.res_balance.grid(row=3, column=1)

        """Pfs déjà investis sur la place requise"""
        label_place = Label(self, text='Pfs déjà investis sur la place requise')
        label_place.grid(row=4, column=0, pady=5, padx=5)
        self.var_place = StringVar()
        self.entry_place = Entry(self, justify='center', width=20, textvariable=self.var_place)
        self.var_place.trace('w', self.snipper)
        self.entry_place.grid(row=4, column=1)

        """Nombre de Pfs à mettre"""
        label_snippe = Label(self, text='Nombre de Pfs à mettre')
        label_snippe.grid(row=5, column=0, pady=5, padx=5)
        self.var_snippe = StringVar()  # variable de contrôle du nombre de pfs à mettre
        self.label2_snippe = Label(self, justify='center', width=20, textvariable=self.var_snippe)
        self.label2_snippe.grid(row=5, column=1)

        """Pfs minimum à snipper"""
        label_mini = Label(self, text='Pfs minimum à snipper')
        label_mini.grid(row=6, column=0, pady=5, padx=5)
        self.var_mini = StringVar()
        self.entry_mini = Entry(self, justify='center', width=20, textvariable=self.var_mini)
        self.var_mini.trace('w', self.snipper)
        self.entry_mini.grid(row=6, column=1)

        """Taux de rentabilité de l'arche"""
        label_additional = Label(self, text="Taux de rentabilité de l'arche")
        label_additional.grid(row=7, column=0, pady=5, padx=5)
        self.var_renta = StringVar()
        self.entry_txrenta = Entry(self, justify='center', width=20, textvariable=self.var_renta)
        self.entry_txrenta.insert(0, res[11])  # récupération du taux de renta de l'arche dans la base de données
        self.var_renta.trace('w', self.snipper)
        self.entry_txrenta.grid(row=7, column=1)

        """Info-bulle sur le taux de rentabilité de l'arche"""
        tip = Balloon(self)
        tip.bind_widget(self.entry_txrenta, balloonmsg="Si le taux de renta de l'arche a été modifié,\n"
                                                  "pour une mise à jour du taux dans ce champ,\n"
                                                  "fermez et réouvrez cette application")

        """Pfs gagnés"""
        label_win = Label(self, text='Pfs gagnés')
        label_win.grid(row=8, column=0, pady=5, padx=5)
        self.var_win = StringVar()  # variable de contrôle des gains en snipant
        self.label_win = Label(self, width=20, textvariable=self.var_win)
        self.label_win.grid(row=8, column=1)


class Note(Frame):
    """Joueurs en liste noire (onglet Blacklist)"""

    def __init__(self, master):
        super().__init__(master)
        self.pack()
        self.widgets()

    def save_file(self):
        """Fonction permettant de sauvegarder les données saisies dans la zone de texte"""
        
        """Assignation de l'obtention des données saisies dans la zone de texte"""
        enemies = self.text_players.get(1.0, END)

        """Assignation d'un nom de fichier"""
        file_name = 'enemies'

        """Assignation de l'ouverture du fichier en mode écriture"""
        output_file = open(file_name, 'wb')

        """Ajout des données de la zone de texte (variable enemies) dans le fichier en mode écriture (variable 
        output_file) """
        pickle.dump(enemies, output_file)

    def widgets(self):

        """Chargement automatique du fichier 'enemies'"""
        try:
            file_name = 'enemies'  # assignation d'un nom de fichier
            input_file = open(file_name, 'rb')  # assignation de l'ouverture du fichier en mode lecture
            enemies = pickle.load(input_file)  # assignation de la récupération des données sauvegardées
        except FileNotFoundError:
            pass

        """Titre de la fenêtre"""
        label_title = Label(self, text='Joueurs en blacklist', font='Helvetica 20 italic bold', fg='red')
        label_title.grid(row=0, column=0, pady=10, padx=10)

        """Cadre pour la zone de texte et le menu déroulant"""
        my_frame = Frame(self)
        my_frame.grid(row=1, column=0, pady=5, padx=10)

        """Barre de déroulement pour la zone de texte"""
        text_scrool = Scrollbar(my_frame)
        text_scrool.pack(side=RIGHT, fill=Y)

        """Zone de texte"""
        self.text_players = Text(my_frame, height=20, yscrollcommand=text_scrool.set)
        try:
            self.text_players.insert(1.0, enemies)  # insertion des données récupérées dans la zone de texte
        except UnboundLocalError:
            pass
        self.text_players.pack()

        """Configuration de la barre de déroulement pour la zone de texte"""
        text_scrool.config(command=self.text_players.yview)

        """Bouton de sauvegarde des données"""
        button_save = Button(self, text='Sauvegarder', command=self.save_file)
        button_save.grid(row=2, column=0, pady=10, padx=10, ipadx=30, ipady=10)


menus = Menus(root)  # menu apparaissant avec le bouton de droite de la souris
gms = Gms(my_frame1)  # onglet Mes Gms
invest = Invest(my_frame2)  # onglet Investissement
snippe = Snippe(my_frame3)  # onglet Snippe
note = Note(my_frame4)  # onglet Blacklist

"""Commit et fermeture"""
conn.commit()
conn.close()

root.mainloop()
