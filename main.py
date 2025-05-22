from tkinter import Tk, Frame, Label, Button, BOTH
from zhelt_functions import load_data_file, run_cluster_analysis, build_heatmap

root = Tk()

#  интерфейс
root.title("Анализ генетических данных")
root.geometry("400x300")

frame = Frame(root, bg="#f0f0f0")
frame.pack(fill=BOTH, expand=True, padx=10, pady=10)

Label(frame, text="Выберите действие:", font=('Arial', 12), bg="#f0f0f0").pack(pady=10)


Button(
    frame,
    text="Загрузите файл",
    command=load_data_file,
    bg="#4CAF50",
    fg="black",
    padx=20,
    pady=10,
    font=('Arial', 10),
    activebackground="#388E3C",
    activeforeground="black"
).pack(pady=5, fill="x")


Button(
    frame,
    text="Выполнить кластерный анализ",
    command=lambda: run_cluster_analysis(use_last_result=False),
    bg="#2196F3",
    fg="black",
    padx=20,
    pady=10,
    font=('Arial', 10),
    activebackground="#1976D2",
    activeforeground="black"
).pack(pady=5, fill="x")


Button(
    frame,
    text="Построить тепловую карту",
    command=build_heatmap,
    bg="#FF9800",
    fg="black",
    padx=20,
    pady=10,
    font=('Arial', 10),
    activebackground="#F57C00",
    activeforeground="black"
).pack(pady=5, fill="x")

root.mainloop()