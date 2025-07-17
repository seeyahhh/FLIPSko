#Dependencies
import tkinter as tk
from tkinter import *
from PIL import ImageTk, Image
from customtkinter import *
import customtkinter as ctk
from tkinter import messagebox
from EASYMODE_module import load_easy_mode
from NORMALMODE_module import load_normal_mode
from DIFFICULTMODE_module import load_difficult_mode

def toMainMenu():
    #WINDOW
    window = ctk.CTk()

    #WINDOW SIZE
    screenWidth = window.winfo_screenwidth()
    screenHeight = window.winfo_screenheight()
    appWidth = 1366
    appHeight = 768
    x = (screenWidth / 2) - (appWidth / 2)
    y = (screenHeight / 2) - (appHeight / 2)
    window.geometry(f'{appWidth}x{appHeight}+{int(x)}+{int(y)}')
    window.title("FLIPSKO")
    window.resizable(False, False)

    # ICON
    window.iconbitmap('logo/FLIPSKOLOGO.ico')

    def toDifficultyPage():
        difficultyPage.place(relheight=1, relwidth=1)
        homePage.place_forget()
        easyPage.place_forget()
        normalPage.place_forget()
        difficultPage.place_forget()

    def toDifficultyPage1(event):
        difficultyPage.place(relheight=1, relwidth=1)
        homePage.place_forget()
        easyPage.place_forget()
        normalPage.place_forget()
        difficultPage.place_forget()

    def toHomePage(event):
        homePage.place(relheight=1, relwidth=1)
        difficultyPage.place_forget()
        easyPage.place_forget()
        normalPage.place_forget()
        difficultPage.place_forget()

    def toEasyPage(event):
        load_easy_mode(easyPage, lambda c: load_normal_mode(c, load_difficult_mode))
        easyPage.place(relheight=1, relwidth=1)
        homePage.place_forget()
        difficultyPage.place_forget()
        normalPage.place_forget()
        difficultPage.place_forget()
        
    def toNormalPage(event):
        load_normal_mode(normalPage, lambda c: load_difficult_mode)
        load_normal_mode(normalPage, load_difficult_mode)
        normalPage.place(relheight=1, relwidth=1)
        homePage.place_forget()
        difficultyPage.place_forget()
        easyPage.place_forget()
        difficultPage.place_forget()

    def toDifficultPage(event):
        load_difficult_mode(difficultPage)
        difficultPage.place(relheight=1, relwidth=1)
        homePage.place_forget()
        difficultyPage.place_forget()
        easyPage.place_forget()
        normalPage.place_forget()

    #HOMEPAGE FRAME
    homepage = Image.open("background/HOMEPAGEBG.png")
    homepage_Photo = ctk.CTkImage(light_image= homepage, dark_image= homepage, size= (1366,768))

    homePage = Frame(window, bg="white")
    homePage.place(relheight=1, relwidth=1)

    #DIFFICULTYPAGE CANVAS
    difficultyPage = tk.Canvas(window, width=1366, height=768, highlightthickness=0)

    difficultypageBGPicture = Image.open("background/difficultyBG1.png")
    difficultypageBGResized = difficultypageBGPicture.resize((1366,768))
    difficultypageBGFinal = ImageTk.PhotoImage(difficultypageBGResized)

    difficultypageBG = difficultyPage.create_image(0,0, image=difficultypageBGFinal, anchor=tk.NW)

    #EASYPAGE CANVAS
    easyPage = tk.Canvas(window, width=1366, height=768, highlightthickness=0)

    easypageBGPicture = Image.open("background/GAMEPLAY.png")
    easypageBGResized = easypageBGPicture.resize((1366,768))
    easypageBGFinal = ImageTk.PhotoImage(easypageBGResized)

    easypageBG = easyPage.create_image(0,0, image=easypageBGFinal, anchor=tk.NW)

    #NORMALPAGE CANVAS
    normalPage = tk.Canvas(window, width=1366, height=768, highlightthickness=0)

    normalpageBGPicture = Image.open("background/GAMEPLAY.png")
    normalpageBGResized = normalpageBGPicture.resize((1366,768))
    normalpageBGFinal = ImageTk.PhotoImage(normalpageBGResized)

    normalpageBG = normalPage.create_image(0,0, image=normalpageBGFinal, anchor=tk.NW)

    #DIFFICULTPAGE CANVAS
    difficultPage = tk.Canvas(window, width=1366, height=768, highlightthickness=0)

    difficultpageBGPicture = Image.open("background/GAMEPLAY.png")
    difficultpageBGResized = difficultpageBGPicture.resize((1366,768))
    difficultpageBGFinal = ImageTk.PhotoImage(difficultpageBGResized)

    difficultpageBG = difficultPage.create_image(0,0, image=difficultpageBGFinal, anchor=tk.NW)

    #HOMEPAGE
    homePage_label = ctk.CTkLabel(homePage, image=homepage_Photo, text="")
    homePage_label.place(x=0, y=0, relwidth=1, relheight=1)

    start_logo = Image.open("buttons/START.png")
    start_logoResized = start_logo.resize((455, 162))
    s_Button = ImageTk.PhotoImage(start_logoResized)

    start_Button = Button(homePage, text="", image=s_Button, bd=0, highlightthickness=0,
                            activebackground='orange',command=toDifficultyPage)
    start_Button.place(x=414, y=438)

    # DIFFICULTY PAGE
    selectLPicture = Image.open("label/selectLevel1.png")
    selectLResized = selectLPicture.resize((793,130))
    selectLFinal = ImageTk.PhotoImage(selectLResized)
    difficultyPage.create_image(673, 150, image=selectLFinal, anchor=tk.CENTER)

    easyBPicture = Image.open("buttons/easyB.png")
    easyBResized = easyBPicture.resize((392,157))
    easyBFinal = ImageTk.PhotoImage(easyBResized)
    easyButton = difficultyPage.create_image(673, 320, image=easyBFinal, anchor=tk.CENTER,)
    difficultyPage.tag_bind(easyButton, "<Button-1>", toEasyPage)

    normalBPicture = Image.open("buttons/normalB.png")
    normalBResized = normalBPicture.resize((392,157))
    normalBFinal = ImageTk.PhotoImage(normalBResized)
    normalButton = difficultyPage.create_image(673, 480, image=normalBFinal, anchor=tk.CENTER)
    difficultyPage.tag_bind(normalButton, "<Button-1>", toNormalPage)

    difficultBPicture = Image.open("buttons/difficultB.png")
    difficultBResized = difficultBPicture.resize((392,157))
    difficultBFinal = ImageTk.PhotoImage(difficultBResized)
    difficultButton =difficultyPage.create_image(673, 650, image=difficultBFinal, anchor=tk.CENTER)
    difficultyPage.tag_bind(difficultButton, "<Button-1>", toDifficultPage)

    returnPicture = Image.open("buttons/RETURN.png")
    returnResized = returnPicture.resize((108,92))
    returnFinal = ImageTk.PhotoImage(returnResized)
    returnHomeButton = difficultyPage.create_image(70,90, image= returnFinal)
    difficultyPage.tag_bind(returnHomeButton, "<Button-1>", toHomePage)

    #EASYGAME PAGE

    settingBPicture = Image.open("buttons/settingB.png")
    settingBResized = settingBPicture.resize((96,101))
    settingBFinal = ImageTk.PhotoImage(settingBResized)
    #settingButton =easyPage.create_image(100, 90, image=settingBFinal, anchor=tk.CENTER)
    easyPage.bind("<<ToDifficultyPage>>", toDifficultyPage1)
    #easyPage.bind("<<ToDifficultyPage>>", toDifficultyPage1)

    flipskoTitle = ImageTk.PhotoImage(Image.open("label/flipskoTitle.png")) 
    #easyPage.create_image(683, 90, image=flipskoTitle, anchor=tk.CENTER)

    easyLPicture = Image.open("label/easyL.png")
    easyLResized = easyLPicture.resize((237,98))
    easyLFinal = ImageTk.PhotoImage(easyLResized)
    #easyPage.create_image(1200, 90, image=easyLFinal, anchor=tk.CENTER)


    #NORMALGAME PAGE
    #settingButton =normalPage.create_image(100, 90, image=settingBFinal, anchor=tk.CENTER)
    #normalPage.tag_bind(settingButton, "<Button-1>", toHomePage)
    normalPage.bind("<<ToDifficultyPage>>", toDifficultyPage1)

    #normalPage.create_image(683, 90, image=flipskoTitle, anchor=tk.CENTER)

    #normalLPicture = Image.open("label/normalL.png")
    #normalLResized = normalLPicture.resize((237,98))
    #normalLFinal = ImageTk.PhotoImage(normalLResized)
    #normalPage.create_image(1200, 90, image=normalLFinal, anchor=tk.CENTER)

    #DIFFICULTGAME PAGE
    #settingButton =difficultPage.create_image(100, 90, image=settingBFinal, anchor=tk.CENTER)
    #difficultPage.tag_bind(settingButton, "<Button-1>", toHomePage)
    difficultPage.bind("<<ToDifficultyPage>>", toDifficultyPage1)

    #difficultPage.create_image(683, 90, image=flipskoTitle, anchor=tk.CENTER)

    #difficultLPicture = Image.open("label/difficultL.png")
    #difficultLResized = difficultLPicture.resize((237,98))
    #difficultLFinal = ImageTk.PhotoImage(difficultLResized)
    #difficultPage.create_image(1200, 90, image=difficultLFinal, anchor=tk.CENTER)

    window.mainloop()
toMainMenu()