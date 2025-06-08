import tkinter as tk
from tkinter import filedialog, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from zhelt_functions import ClusterAnalyzer


class ClusterAnalysisApp:

    def __init__(self, root):
        """Инициализирует приложение.

        """
        self.root = root
        self.root.title("Кластерный анализ генов")

        # Инициализация анализатора
        self.analyzer = ClusterAnalyzer()

        # Создание интерфейса
        self.create_widgets()

    def create_widgets(self):
        """Создает и размещает элементы интерфейса в главном окне."""
        # Кнопки для загрузки файлов
        tk.Label(self.root, text="Файл с экспрессией генов:").pack()
        tk.Button(self.root, text="Загрузить CSV", command=self.load_expression_file).pack()

        tk.Label(self.root, text="Файл со статистикой генов:").pack()
        tk.Button(self.root, text="Загрузить CSV", command=self.load_stats_file).pack()

        # Кнопка для запуска анализа
        self.analyze_btn = tk.Button(self.root, text="Кластерный анализ",
                                     command=self.perform_initial_clustering, state=tk.DISABLED)
        self.analyze_btn.pack(pady=10)

    def load_expression_file(self):
        """Загружает файл с данными экспрессии генов.

        Открывает диалоговое окно для выбора CSV-файла и загружает данные
        Активирует кнопку анализа, если загружены оба файла.
        """
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if file_path:
            try:
                self.analyzer.load_expression_data(file_path)
                self.check_files_loaded()
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось загрузить файл: {e}")

    def load_stats_file(self):
        """Загружает файл со статистикой генов.

        Открывает диалоговое окно для выбора CSV-файла и загружает данные
        Активирует кнопку анализа, если загружены оба файла.
        """
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if file_path:
            try:
                self.analyzer.load_stats_data(file_path)
                self.check_files_loaded()
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось загрузить файл: {e}")

    def check_files_loaded(self):
        """Проверяет, загружены ли оба файла, и активирует кнопку анализа."""
        if self.analyzer.expression_data is not None and self.analyzer.stats_data is not None:
            self.analyze_btn.config(state=tk.NORMAL)

    def perform_initial_clustering(self):
        """Выполняет кластерный анализ и отображает результаты."""
        clustered_data = self.analyzer.perform_clustering()
        self.show_results(clustered_data)

    def perform_clustering_for_cluster(self, cluster_num):
        """Выполняет кластерный анализ для указанного кластера.
        """
        cluster_data = self.analyzer.get_cluster_data(cluster_num)
        if cluster_data is not None:
            new_clusters = self.analyzer.perform_clustering(cluster_data)
            self.show_results(new_clusters)

    def show_results(self, data):
        """Отображает результаты кластерного анализа.

        """
        # Показать графики кластеров
        self.show_cluster_plots(data)

        # Показать окно с кнопками действий
        self.show_action_buttons()

    def show_cluster_plots(self, data):
        """Создает окно с графиками кластеров.

        """
        plots_window = tk.Toplevel(self.root)
        plots_window.title("Графики кластеров")

        fig = self.analyzer.create_cluster_plots(data)

        canvas = FigureCanvasTkAgg(fig, master=plots_window)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    def show_action_buttons(self):
        """Создает окно с кнопками для дополнительных действий с кластерами."""
        action_window = tk.Toplevel(self.root)
        action_window.title("Действия с кластерами")

        # для кнопок повторного анализа
        reanalyze_frame = tk.Frame(action_window)
        reanalyze_frame.pack(pady=10)

        tk.Label(reanalyze_frame, text="Выполнить кластерный анализ еще раз:").pack()

        button_frame = tk.Frame(reanalyze_frame)
        button_frame.pack()

        for i in range(4):
            btn = tk.Button(button_frame, text=str(i + 1),
                            command=lambda num=i: self.perform_clustering_for_cluster(num))
            btn.pack(side=tk.LEFT, padx=5)

        # для кнопок тепловой карты
        heatmap_frame = tk.Frame(action_window)
        heatmap_frame.pack(pady=10)

        tk.Label(heatmap_frame, text="Построить тепловую карту:").pack()

        heatmap_btn_frame = tk.Frame(heatmap_frame)
        heatmap_btn_frame.pack()

        for i in range(4):
            btn = tk.Button(heatmap_btn_frame, text=str(i + 1),
                            command=lambda num=i: self.show_heatmap(num))
            btn.pack(side=tk.LEFT, padx=5)

    def show_heatmap(self, cluster_num):
        """Отображает тепловую карту для указанного кластера.

        """
        fig = self.analyzer.create_heatmap(cluster_num)
        if fig:
            heatmap_window = tk.Toplevel(self.root)
            heatmap_window.title(f"Тепловая карта кластера {cluster_num + 1}")

            canvas = FigureCanvasTkAgg(fig, master=heatmap_window)
            canvas.draw()
            canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        else:
            messagebox.showerror("Ошибка", "Не удалось построить тепловую карту")


if __name__ == "__main__":
    """Точка входа для запуска приложения."""
    root = tk.Tk()
    app = ClusterAnalysisApp(root)
    root.mainloop()