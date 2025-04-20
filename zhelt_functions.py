from tkinter import *
from tkinter import filedialog
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

root = Tk()

current_file = None
normal_file = 'normal1.csv'
analyse_file = 'analyse1.csv'


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

    sns.heatmap(filter.iloc[:343, :], cmap='coolwarm', vmin=0, vmax=30, center=1)
    plt.show()


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


def cluster_analysis(filepath, use_last_result=False):
    global last_analysis_file

    try:
        # загрузка данных
        if use_last_result and last_analysis_file:
            data = pd.read_csv(last_analysis_file)
            print("Используются результаты предыдущего анализа")
        else:
            data = pd.read_csv(filepath)

            data = data.set_index('gene_id').T
            data = data.astype(float)

            scaler = StandardScaler()
            scaled_data = scaler.fit_transform(data)

            # K-means
            kmeans = KMeans(n_clusters=4, random_state=42)
            clusters = kmeans.fit_predict(scaled_data)

            data['Cluster'] = clusters

            last_analysis_file = 'clustered_data.csv'
            data.to_csv(last_analysis_file, index=False)
            print("Кластерный анализ завершен. Результаты сохранены в clustered_data.csv")

        plt.figure(figsize=(10, 6))
        sns.scatterplot(data=data, x=data.columns[0], y=data.columns[1], hue='Cluster', palette='viridis')
        plt.title("Результаты кластерного анализа")
        plt.show()

        show_analysis_options()

    except Exception as e:
        print(f"Ошибка при выполнении кластерного анализа: {e}")


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


# интерфейс
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
    fg="white",
    padx=20,
    pady=10,
    font=('Arial', 10)
).pack(pady=5, fill=X)

# анализ
Button(
    frame,
    text="Выполнить кластерный анализ",
    command=lambda: run_cluster_analysis(use_last_result=False),
    bg="#2196F3",
    fg="white",
    padx=20,
    pady=10,
    font=('Arial', 10)
).pack(pady=5, fill=X)

# тепловая карта
Button(
    frame,
    text="Построить тепловую карту",
    command=build_heatmap,
    bg="#FF9800",
    fg="white",
    padx=20,
    pady=10,
    font=('Arial', 10)
).pack(pady=5, fill=X)

root.mainloop()