from tkinter import filedialog
from tkinter import Toplevel, Label, Button, X
from zhelt_bioinformatics.analyse import temp_cardas, cluster_analysis

current_file = None
normal_file = 'normal1.csv'
analyse_file = 'analyse1.csv'
last_analysis_file = None

def show_analysis_options():
    options_window = Toplevel(root)
    options_window.title("Дальнейшие действия")
    options_window.geometry("350x150")

    Label(options_window, text="Выберите следующее действие:", font=('Arial', 12)).pack(pady=10)

    Button(
        options_window,
        text="Построить тепловую карту",
        command=lambda: [options_window.destroy(), build_heatmap()],
        bg="#FF9800",
        fg="white",
        padx=20,
        pady=10,
        font=('Arial', 10)
    ).pack(pady=5, fill=X)

    Button(
        options_window,
        text="Выполнить кластерный анализ еще раз",
        command=lambda: [options_window.destroy(), run_cluster_analysis(use_last_result=True)],
        bg="#2196F3",
        fg="white",
        padx=20,
        pady=10,
        font=('Arial', 10)
    ).pack(pady=5, fill=X)

def run_cluster_analysis(use_last_result=False):
    if use_last_result and last_analysis_file:
        cluster_analysis(None, use_last_result=True)
    elif current_file:
        cluster_analysis(current_file)
    else:
        print("Сначала загрузите файл данных")

def build_heatmap():
    temp_cardas(normal_file, analyse_file)

def load_data_file():
    global current_file
    filepath = filedialog.askopenfilename(
        title="Выберите файл данных",
        filetypes=(("CSV файлы", "*.csv"), ("Все файлы", "*.*"))
    )
    if filepath:
        current_file = filepath
        print(f"Выбран файл: {filepath}")