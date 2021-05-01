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

spacy_summarizer = TextSummarizer('spacy')
text_to_speech = TextToSpeech()
text_to_image = TextToImage(N_IMG)
english_translator = TextTranslate('en')
german_translator = TextTranslate('german')
spanish_translator = TextTranslate('spanish')
extractor = ExtractKeywords(10)


def openfiles():
    file1 = tk.filedialog.askopenfilename(filetypes=(("Text Files", ".txt"),
                                                     ("All files", "*")))
    read_text = open(file1).read()
    displayed_file.insert(tk.END, read_text)


def get_text():
    raw_text = str(url_entry.get())
    page = urlopen(raw_text)
    soup = BeautifulSoup(page)
    fetched_text = ' '.join(map(lambda p: p.text, soup.find_all('p')))
    displayed_file.insert(tk.END, fetched_text)


def play():
    text_to_speech.play()


def pause():
    text_to_speech.pause_unpause()


def stop():
    text_to_speech.stop()


# Clear Text  with position 1.0
def clear_text_file():
    displayed_file.delete('1.0', END)


def clearText():
    tab3_display_text.delete('1.0', END)


def get_file_summary():
    global RESULT
    raw_text = displayed_file.get('1.0', tk.END)
    final_text = spacy_summarizer(raw_text)
    RESULT = '\n{}'.format(final_text)
    tab2_display_text.insert(tk.END, RESULT)
    final_text = text_to_speech.load(RESULT)

    keywords = extractor(raw_text)
    keywords = [''.join(e for e in k if e.isalnum()) for k in keywords]
    keywords = [k for k in keywords if len(k) > 2][:N_KEY]
    text = ', '.join(keywords)
    l5.configure(text=text)

    if os.path.isdir('./downloads'):
        rmtree('./downloads')
    clean_images(N_KEY)
    for i, word in enumerate(keywords[:N_KEY]):
        images = get_images(word, N_IMG)
        update_images(images, i)


def get_images(word, n_images):
    try:
        text_to_image(word)
        return glob(f'./downloads/{word}/*')[:n_images]
    except:
        return ['./Analysis/data1.jpg'] * n_images


def update_images(images, i):
    image_loc = image_dict[i]
    for y, x in enumerate(image_loc):
        img = Image.open(images[y])
        img = img.resize((H, W))
        img = ImageTk.PhotoImage(img)
        x.configure(image=img)
        x.photo = img


def clean_images(n_images):
    images = ['./Analysis/data1.jpg'] * n_images
    for i, k in enumerate(image_dict):
        update_images(images, i)


def clear_text_result():
    global RESULT
    tab2_display_text.delete('1.0', END)
    RESULT = ''
    stop()


def get_keywords_image():
    tab2_display_text.delete('1.0', END)


def convertEnglish():
    global RESULT
    final_text = english_translator(RESULT)
    tab3_display_text.insert(tk.END, final_text)


def convertGerman():
    global RESULT
    final_text = german_translator(RESULT)
    tab3_display_text.insert(tk.END, final_text)


def convertSpanish():
    global RESULT
    final_text = spanish_translator(RESULT)
    tab3_display_text.insert(tk.END, final_text)


window = Tk()
window.title("Summarizer App")
window.geometry("1500x1200")
# window2.geometry("700x900")
window.config(background='white')
# window2.config(background='white')

style = ttk.Style(window)
style.theme_create('pastel', settings={
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

style.theme_use('pastel')
style.configure('lefttab.TNotebook', tabposition='wn',)

image1 = Image.open("./icons/play.png")
image1 = image1.resize((60, 60))
icon = ImageTk.PhotoImage(image1)
image2 = Image.open("./icons/pause.png")
image2 = image2.resize((60, 60))
icon2 = ImageTk.PhotoImage(image2)
image3 = Image.open("./icons/stop.png")
image3 = image3.resize((60, 60))
icon3 = ImageTk.PhotoImage(image3)

tab_control = ttk.Notebook(window, width=200, height=200)
tab1 = ttk.Frame(tab_control, height=20)

tab_control.add(tab1)
tab_control.pack(expand=True, fill=tk.BOTH)


l1 = Label(tab1, text="INPUT", padx=0, pady=0, font=("Arial Bold", 15))
l1.grid(row=1, column=0)

b0 = Button(tab1, text="Open File", width=12, height=3, command=openfiles,
            bg='#03A9F4', fg='#000')
b0.grid(row=2, column=0, padx=0, pady=0)

raw_entry = StringVar()
url_entry = Entry(tab1, textvariable=raw_entry, width=40)
url_entry.grid(row=2, column=1)

button2 = Button(tab1, text="open from url", command=get_text, width=12,
                 height=3, bg='#03A9F4', fg='#000')
button2.grid(row=2, column=2)

displayed_file = ScrolledText(tab1, height=20)
displayed_file.grid(row=3, column=0, columnspan=3, padx=5, pady=3)

b1 = Button(tab1, text="Reset", width=12, height=3, command=clear_text_file,
            bg='#03A9F4', fg='#000')
b1.grid(row=4, column=0, padx=10, pady=10)


b3 = Button(tab1, text="Summarize", width=12, height=3,
            command=get_file_summary, bg='Purple', fg='#fff')
b3.grid(row=4, column=2, padx=10, pady=10)


l2 = Label(tab1, text="OUTPUT", padx=0, pady=0, font=("Arial Bold", 15))
l2.grid(row=5, column=0)

tab2_display_text = ScrolledText(tab1, height=30)
tab2_display_text.grid(row=6, column=0, columnspan=3, padx=5, pady=5)

b4 = Button(tab1, image=icon, width=60, height=60, command=play,
            bg='#fff', fg='#000')
b4.grid(row=8, column=0, padx=1, pady=1)

b4 = Button(tab1, image=icon2, width=60, height=60, command=pause,
            bg='#fff', fg='#000')
b4.grid(row=8, column=1, padx=1, pady=1)

b4 = Button(tab1, image=icon3, width=60, height=60, command=stop, bg='#fff',
            fg='#000')
b4.grid(row=8, column=2, padx=1, pady=1)

b2 = Button(tab1, text="Clear Result", width=12, height=3,
            command=clear_text_result, bg='#03A9F4', fg='#000')
b2.grid(row=10, column=0, padx=10, pady=10)

b5 = Button(tab1, text="Close", width=12, height=3, command=window.destroy,
            bg='#03A9F4', fg='#000')
b5.grid(row=10, column=2, padx=10, pady=10)


l3 = Label(tab1, text="TRANSALTOR", padx=0, pady=0, font=("Arial Bold", 15))
l3.grid(row=5, column=6)

tab3_display_text = ScrolledText(tab1, height=30, width=100)
tab3_display_text.grid(row=6, column=5, columnspan=3, padx=5, pady=5)

tb1 = Button(tab1, text="CLEAR", width=12, height=3, command=clearText,
             bg='#03A9F4', fg='#000')
tb1.grid(row=6, column=8)

tb1 = Button(tab1, text="ENGLISH", width=12, height=3, command=convertEnglish,
             bg='#03A9F4', fg='#000')
tb1.grid(row=8, column=5)

tb3 = Button(tab1, text="GERNAN", width=12, height=3, command=convertGerman,
             bg='#03A9F4', fg='#fff')
tb3.grid(row=8, column=6)

tb3 = Button(tab1, text="SPANISH", width=12, height=3, command=convertSpanish,
             bg='#03A9F4', fg='#fff')
tb3.grid(row=8, column=7)


img1 = Image.open("./Analysis/data1.jpg")
img1 = img1.resize((H, W))
i1 = ImageTk.PhotoImage(img1)
image1 = Label(tab1, image=i1)
image1.grid(row=2, column=5)

l4 = Label(tab1, text="TOP 5 KEYWORDS: ", padx=0, pady=0, font=("Arial Bold",
           15))
l4.grid(row=1, column=5)
l5 = Label(tab1, text='', padx=0, pady=0, font=("Arial Bold", 15))
l5.grid(row=1, column=6)

image11 = Label(tab1, image=i1)
image11.grid(row=2, column=4)

image12 = Label(tab1, image=i1)
image12.grid(row=2, column=5)

image13 = Label(tab1, image=i1)
image13.grid(row=2, column=6)

image14 = Label(tab1, image=i1)
image14.grid(row=2, column=7)

image15 = Label(tab1, image=i1)
image15.grid(row=2, column=8)

image21 = Label(tab1, image=i1)
image21.grid(row=3, column=4)

image22 = Label(tab1, image=i1)
image22.grid(row=3, column=5)

image23 = Label(tab1, image=i1)
image23.grid(row=3, column=6)

image24 = Label(tab1, image=i1)
image24.grid(row=3, column=7)

image25 = Label(tab1, image=i1)
image25.grid(row=3, column=8)

image31 = Label(tab1, image=i1)
image31.grid(row=4, column=4)

image32 = Label(tab1, image=i1)
image32.grid(row=4, column=5)

image33 = Label(tab1, image=i1)
image33.grid(row=4, column=6)

image34 = Label(tab1, image=i1)
image34.grid(row=4, column=7)

image35 = Label(tab1, image=i1)
image35.grid(row=4, column=8)

image_dict = {0: [image11, image21, image31],
              1: [image12, image22, image32],
              2: [image13, image23, image33],
              3: [image14, image24, image34],
              4: [image15, image25, image35]}

window.mainloop()
