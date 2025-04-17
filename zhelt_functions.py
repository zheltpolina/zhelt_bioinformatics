from tkinter import *
from tkinter import filedialog
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

root = Tk()

def temp_cardas(normal_path, analyse_path):

    normal = pd.read_csv(normal_path)
    analyse = pd.read_csv(analyse_path)

    filter = normal[normal.gene_id.isin(analyse.gene_id)].reset_index(drop=True)
    filter = filter.T

    columns = filter.iloc[1].values
    filter = filter.drop(['Unnamed: 0', 'gene_id'])
    filter.columns = columns
    filter = filter.astype(float)


    matrix = filter.corr()
    cmatrix = matrix.values


    sns.heatmap(filter.iloc[:343,:], cmap= 'coolwarm', vmin=0, vmax=30, center= 1)
    plt.show()

#def btn_click():

#def btn1_click():
def btn2_click():
    temp_cardas('normal1.csv', 'analyse1.csv')


def load_file():
    filepath = filedialog.askopenfilename(
        title="Выберите файл",
        filetypes=(("CSV файлы", "*.csv"), ("Все файлы", "*.*"))
    )
    if filepath:
        print(f"Выбран файл: {filepath}")
root.title("кластерный анализ")
root.geometry("350x250")

canvas = Canvas(root, height = 350, width = 250)
canvas.pack()

frame = Frame(root, bg="dark blue")
frame.place(relwidth=1, relheight=1 )


title = Label(frame, text="продолжить?", padx=30, pady=20)
title.grid(row=5, column=5)
title.pack()

btn_frame = Frame(frame, bg="dark blue")
btn_frame.pack(pady=5)

btn = Button(btn_frame, text="да", padx=23, pady=10)
btn1 = Button(btn_frame, text="нет", padx=23, pady=10)

btn.pack(side=LEFT, padx=5)
btn1.pack(side=LEFT, padx=5)

btn2 = Button(frame, text="построить тепловую карту", padx=80, pady=10, command=btn2_click)
btn2.pack(pady=10)

load_btn = Button(
    frame,
    text="Загрузить файл",
    padx=50,
    pady=10,
    command=load_file,
    bg="lightblue"
)
load_btn.pack(pady=5)

root.mainloop()

#command=btn_click
