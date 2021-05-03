from utils import TextSummarizer, TextToSpeech, TextToImage, TextTranslate,\
    ExtractKeywords
from tkinter import ttk, Tk, Label, Button, StringVar, Entry, END
from tkinter.scrolledtext import ScrolledText
import tkinter as tk
import tkinter.filedialog
from PIL import Image, ImageTk
from urllib.request import urlopen
from bs4 import BeautifulSoup
from glob import glob
from shutil import rmtree
import os

RESULT = ''
H, W = (120, 120)
N_KEY = 5
N_IMG = 3

genrateSummarizer = TextSummarizer()
textToSpeech = TextToSpeech()
textToImage = TextToImage(N_IMG)
english_translator = TextTranslate('en')
german_translator = TextTranslate('german')
spanish_translator = TextTranslate('spanish')
keywordsExtractor = ExtractKeywords(100)


def openFilesFromPC():
    file1 = tk.filedialog.askopenfilename(filetypes=(("Text Files", ".txt"),
                                                     ("All files", "*")))
    read_text = open(file1).read()
    inputDisplay.insert(tk.END, read_text)


def openFilesFromURL():
    raw_text = str(textFromUrl.get())
    page = urlopen(raw_text)
    soup = BeautifulSoup(page)
    fetched_text = ' '.join(map(lambda p: p.text, soup.find_all('p')))
    inputDisplay.insert(tk.END, fetched_text)


def playSummary():
    textToSpeech.play()


def pauseSummary():
    textToSpeech.pause_unpause()


def stopSummary():
    textToSpeech.stop()


# Clear Text  with position 1.0
def resetTextFile():
    inputDisplay.delete('1.0', END)


def clearTextFile():
    translatorDisplay.delete('1.0', END)


def displayFileSummary():
    global RESULT
    raw_text = inputDisplay.get('1.0', tk.END)
    final_text = genrateSummarizer(raw_text)
    RESULT = '\n{}'.format(final_text)
    print(RESULT)
    outputDisplay.insert(tk.END, RESULT)
    final_text = textToSpeech.load(RESULT)

    keywords = keywordsExtractor(RESULT)
    # shuffle(keywords)
    keywords = [''.join(e for e in k if e.isalnum()) for k in keywords]
    keywords = [k for k in keywords if len(k) > 2][:N_KEY]
    text = ', '.join(keywords)
    l5.configure(text=text)

    if os.path.isdir('./downloads'):
        rmtree('./downloads')
    cleanImages(N_KEY)
    for i, word in enumerate(keywords[:N_KEY]):
        images = getImagesFromKeywords(word, N_IMG)
        updateImages(images, i)


def getImagesFromKeywords(word, n_images):
    try:
        textToImage(word)
        return glob(f'./downloads/{word}/*')[:n_images]
    except:
        return ['./Analysis/data1.jpg'] * n_images


def updateImages(images, i):
    image_loc = image_dict[i]
    for y, x in enumerate(image_loc):
        img = Image.open(images[y])
        img = img.resize((H, W))
        img = ImageTk.PhotoImage(img)
        x.configure(image=img)
        x.photo = img


def cleanImages(n_images):
    images = ['./Analysis/data1.jpg'] * n_images
    for i, k in enumerate(image_dict):
        updateImages(images, i)


def deleteSummaryResult():
    global RESULT
    outputDisplay.delete('1.0', END)
    RESULT = ''
    stop()


# def get_keywords_image():
#     outputDisplay.delete('1.0', END)


def convertEnglish():
    global RESULT
    final_text = english_translator(RESULT)
    translatorDisplay.insert(tk.END, final_text)


def convertGerman():
    global RESULT
    final_text = german_translator(RESULT)
    translatorDisplay.insert(tk.END, final_text)


def convertSpanish():
    global RESULT
    final_text = spanish_translator(RESULT)
    translatorDisplay.insert(tk.END, final_text)


panelWindowOfApp = Tk()
panelWindowOfApp.title("Summarizer App")
panelWindowOfApp.geometry("1500x1200")
# panelWindowOfApp2.geometry("700x900")
panelWindowOfApp.config(background='white')
# panelWindowOfApp2.config(background='white')

panelStyle = ttk.Style(panelWindowOfApp)
panelStyle.theme_create('SummarizerApplication', settings={
    ".": {
        "configure": {
            "background": '#ffffff',
            "font": 'red'
        }
    },
    "TNotebook": {
        "configure": {
            "background": '#000000',
            "tabmargins": [2, 5, 0, 0],
        }
    },
    "TNotebook.Tab": {
        "configure": {
            "background": '#4267B2',
            "padding": [10, 2],
            "font": "white"
        },
        "map": {
            "background": [("selected", '#ccffff')],
            "expand": [("selected", [1, 1, 1, 0])]
        }
    }
})

panelStyle.theme_use('SummarizerApplication')
panelStyle.configure('lefttab.TNotebook', tabposition='wn',)

imagePlay = Image.open("./icons/play.png")
imagePlay = imagePlay.resize((50, 50))
icon = ImageTk.PhotoImage(imagePlay)
imagePause = Image.open("./icons/pause.png")
imagePause = imagePause.resize((50, 50))
icon2 = ImageTk.PhotoImage(imagePause)
imageStop = Image.open("./icons/stop.png")
imageStop = imageStop.resize((50, 50))
icon3 = ImageTk.PhotoImage(imageStop)

windowTabControl = ttk.Notebook(panelWindowOfApp, width=200, height=200)
firstWndow = ttk.Frame(windowTabControl, height=20)

windowTabControl.add(firstWndow)
windowTabControl.pack(expand=True, fill=tk.BOTH)


l1 = Label(firstWndow, text="INPUT", font=("Arial Bold", 18), anchor="center",
           bg='#686766', fg='#fff', padx=50)
l1.grid(row=1, column=0)

b0 = Button(firstWndow, text="Open File", width=12, height=3,
            command=openFilesFromPC, bg='#03A9F4', fg='#000')
b0.grid(row=2, column=0, padx=0, pady=0)

textBoxEntry = StringVar()
textFromUrl = Entry(firstWndow, textvariable=textBoxEntry, width=40)
textFromUrl.grid(row=2, column=1)

b2 = Button(firstWndow, text="open from url", command=openFilesFromURL,
            width=12, height=3, bg='#03A9F4', fg='#000')
b2.grid(row=2, column=2)

inputDisplay = ScrolledText(firstWndow, height=20)
inputDisplay.grid(row=3, column=0, columnspan=3, padx=5, pady=3)

b1 = Button(firstWndow, text="Reset", width=12, height=3,
            command=resetTextFile, bg='#03A9F4', fg='#000')
b1.grid(row=4, column=0, padx=10, pady=10)


b3 = Button(firstWndow, text="Summarize", width=12, height=3,
            command=displayFileSummary, bg='Purple', fg='#fff')
b3.grid(row=4, column=2, padx=10, pady=10)


l2 = Label(firstWndow, text="OUTPUT", font=("Arial Bold", 18), anchor="center",
           bg='#686766', fg='#fff', padx=50)
l2.grid(row=5, column=0)

outputDisplay = ScrolledText(firstWndow, height=30)
outputDisplay.grid(row=6, column=0, columnspan=3, padx=5, pady=5)

b4 = Button(firstWndow, image=icon, width=50, height=50, command=playSummary,
            bg='#fff', fg='#000')
b4.grid(row=8, column=0, padx=1, pady=1)

b4 = Button(firstWndow, image=icon2, width=50, height=50, command=pauseSummary,
            bg='#fff', fg='#000')
b4.grid(row=8, column=1, padx=1, pady=1)

b4 = Button(firstWndow, image=icon3, width=50, height=50, command=stopSummary,
            bg='#fff', fg='#000')
b4.grid(row=8, column=2, padx=1, pady=1)

b6 = Button(firstWndow, text="Clear Result", width=12, height=3,
            command=deleteSummaryResult, bg='#03A9F4', fg='#000')
b6.grid(row=10, column=0, padx=10, pady=10)

b5 = Button(firstWndow, text="Close", width=12, height=3,
            command=panelWindowOfApp.destroy, bg='#03A9F4', fg='#000')
b5.grid(row=10, column=2, padx=10, pady=10)


l3 = Label(firstWndow, text="TEXT TRANSALTOR", font=("Arial Bold", 18),
           anchor="center", bg='#686766', fg='#fff', padx=50)
l3.grid(row=5, column=5)

translatorDisplay = ScrolledText(firstWndow, height=30, width=100)
translatorDisplay.grid(row=6, column=5, columnspan=3, padx=5, pady=5)

tb1 = Button(firstWndow, text="CLEAR", width=12, height=3,
             command=clearTextFile, bg='#03A9F4', fg='#000')
tb1.grid(row=6, column=8)

tb1 = Button(firstWndow, text="ENGLISH", width=12, height=3,
             command=convertEnglish, bg='#03A9F4', fg='#000')
tb1.grid(row=8, column=5)

tb3 = Button(firstWndow, text="GERMAN", width=12, height=3,
             command=convertGerman, bg='#03A9F4', fg='#fff')
tb3.grid(row=8, column=6)

tb3 = Button(firstWndow, text="SPANISH", width=12, height=3,
             command=convertSpanish, bg='#03A9F4', fg='#fff')
tb3.grid(row=8, column=7)


img1 = Image.open("./Analysis/data1.jpg")
img1 = img1.resize((H, W))
i1 = ImageTk.PhotoImage(img1)
defaultImage = Label(firstWndow, image=i1)
defaultImage.grid(row=2, column=5)

l4 = Label(firstWndow, text="TOP 5 KEYWORDS : ", font=("Arial Bold", 18),
           anchor="center", bg='#686766', fg='#fff', padx=50)
l4.grid(row=1, column=5)
l5 = Label(firstWndow, text='', padx=0, pady=0, font=("Arial Bold", 18),
           anchor="center", bg='#686766', fg='#fff')
l5.grid(row=1, column=6)

image11 = Label(firstWndow, image=i1)
image11.grid(row=2, column=4)

image12 = Label(firstWndow, image=i1)
image12.grid(row=2, column=5)

image13 = Label(firstWndow, image=i1)
image13.grid(row=2, column=6)

image14 = Label(firstWndow, image=i1)
image14.grid(row=2, column=7)

image15 = Label(firstWndow, image=i1)
image15.grid(row=2, column=8)

image21 = Label(firstWndow, image=i1)
image21.grid(row=3, column=4)

image22 = Label(firstWndow, image=i1)
image22.grid(row=3, column=5)

image23 = Label(firstWndow, image=i1)
image23.grid(row=3, column=6)

image24 = Label(firstWndow, image=i1)
image24.grid(row=3, column=7)

image25 = Label(firstWndow, image=i1)
image25.grid(row=3, column=8)

image31 = Label(firstWndow, image=i1)
image31.grid(row=4, column=4)

image32 = Label(firstWndow, image=i1)
image32.grid(row=4, column=5)

image33 = Label(firstWndow, image=i1)
image33.grid(row=4, column=6)

image34 = Label(firstWndow, image=i1)
image34.grid(row=4, column=7)

image35 = Label(firstWndow, image=i1)
image35.grid(row=4, column=8)

image_dict = {0: [image11, image21, image31],
              1: [image12, image22, image32],
              2: [image13, image23, image33],
              3: [image14, image24, image34],
              4: [image15, image25, image35]}

panelWindowOfApp.mainloop()
