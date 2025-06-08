import tkinter as tk
from tkinter import filedialog, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from zhelt_functions import ClusterAnalyzer


class ClusterAnalysisApp:
    """Основной класс приложения для кластерного анализа генной экспрессии.

    Предоставляет графический интерфейс для:
    - Загрузки файлов с данными экспрессии генов и статистики
    - Выполнения кластерного анализа методом K-means
    - Визуализации результатов в виде графиков и тепловых карт
    - Сохранения результатов кластеризации в CSV-файлы

    Attributes:
        root (tk.Tk): Главное окно приложения
        iteration (int): Счетчик итераций кластерного анализа
        initial_cluster (int or None): Номер исходного кластера для вложенного анализа
        current_clustered_data (pd.DataFrame or None): Текущие результаты кластеризации
        analyzer (ClusterAnalyzer): Экземпляр анализатора для выполнения расчетов
        analyze_btn (tk.Button): Кнопка запуска анализа
    """

    def __init__(self, root):
        """Инициализирует приложение и создает интерфейс.

        вход:
            root (tk.Tk): Корневое окно Tkinter
        """
        self.root = root
        self.root.title("Кластерный анализ генов")
        self.iteration = 0  # Счетчик итераций
        self.initial_cluster = None  # Номер исходного кластера
        self.current_clustered_data = None  # Текущие данные кластеризации

        # Инициализация анализатора
        self.analyzer = ClusterAnalyzer()

        # Создание интерфейса
        self.create_widgets()

    def create_widgets(self):
        """Создает и размещает элементы графического интерфейса.

        Создает:
        - Метки и кнопки для загрузки файлов экспрессии и статистики
        - Кнопку для запуска анализа (изначально неактивную)
        """
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

        Открывает диалоговое окно для выбора CSV-файла, загружает данные через ClusterAnalyzer
        и активирует кнопку анализа при успешной загрузке обоих файлов.

        Raises:
            Exception: Если произошла ошибка при загрузке файла, показывает сообщение об ошибке.
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

        Открывает диалоговое окно для выбора CSV-файла, загружает данные через ClusterAnalyzer
        и активирует кнопку анализа при успешной загрузке обоих файлов.

        Raises:
            Exception: Если произошла ошибка при загрузке файла, показывает сообщение об ошибке.
        """
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if file_path:
            try:
                self.analyzer.load_stats_data(file_path)
                self.check_files_loaded()
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось загрузить файл: {e}")

    def check_files_loaded(self):
        """Проверяет загрузку обоих файлов и активирует кнопку анализа.

        Если оба файла (экспрессии и статистики) успешно загружены,
        активирует кнопку "Кластерный анализ".
        """
        if self.analyzer.expression_data is not None and self.analyzer.stats_data is not None:
            self.analyze_btn.config(state=tk.NORMAL)

    def perform_initial_clustering(self):
        """Выполняет первоначальный кластерный анализ.

        Сбрасывает счетчики итераций и исходного кластера, выполняет кластеризацию
        и отображает результаты.
        """
        self.iteration = 1  # Сбрасываем счетчик итераций
        self.initial_cluster = None  # Сбрасываем номер исходного кластера
        self.current_clustered_data = self.analyzer.perform_clustering()
        self.show_results(self.current_clustered_data)

    def perform_clustering_for_cluster(self, cluster_num):
        """Выполняет кластерный анализ для указанного кластера.

        вход:
            cluster_num (int): Номер кластера (0-3) для повторного анализа

        Увеличивает счетчик итераций, запоминает исходный кластер (если это первая итерация),
        выполняет кластеризацию для выбранного кластера и отображает результаты.
        """
        self.iteration += 1  # Увеличиваем счетчик итераций
        if self.initial_cluster is None:
            self.initial_cluster = cluster_num  # Запоминаем номер исходного кластера

        cluster_data = self.analyzer.get_cluster_data(cluster_num)
        if cluster_data is not None:
            self.current_clustered_data = self.analyzer.perform_clustering(cluster_data)
            self.show_results(self.current_clustered_data)

    def save_cluster_to_csv(self, cluster_num):
        """Сохраняет указанный кластер в CSV-файл.

        вход:
            cluster_num (int): Номер кластера (0-3) для сохранения

        Открывает диалоговое окно для выбора места сохранения и сохраняет данные кластера.
        Показывает сообщение об успешном сохранении или ошибке.

        Raises:
            Exception: Если произошла ошибка при сохранении файла
        """
        if self.current_clustered_data is None:
            messagebox.showerror("Ошибка", "Нет данных для сохранения")
            return

        cluster_data = self.current_clustered_data[self.current_clustered_data['labels_nse'] == cluster_num]
        if cluster_data.empty:
            messagebox.showerror("Ошибка", f"Кластер {cluster_num + 1} не содержит данных")
            return

        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv")],
            title=f"Сохранить кластер {cluster_num + 1} как..."
        )

        if file_path:
            try:
                cluster_data.to_csv(file_path, index=False)
                messagebox.showinfo("Успех", f"Кластер {cluster_num + 1} успешно сохранен")
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось сохранить файл: {e}")

    def show_results(self, data):
        """Отображает результаты кластерного анализа.

        вход:
            data (pd.DataFrame): Данные с результатами кластеризации

        Показывает графики кластеров и окно с кнопками для дополнительных действий.
        """
        # Показать графики кластеров
        self.show_cluster_plots(data)

        # Показать окно с кнопками действий
        self.show_action_buttons()

    def show_cluster_plots(self, data):
        """Создает окно с графиками кластеров.

        вход:
            data (pd.DataFrame): Данные с метками кластеров

        выход:
            Создает новое окно Toplevel с 4 графиками (2x2), по одному для каждого кластера.
            В заголовке окна указывается номер итерации и исходного кластера (если есть).
        """
        plots_window = tk.Toplevel(self.root)

        # Формируем заголовок с информацией об итерации и исходном кластере
        title = "Графики кластеров"
        if self.initial_cluster is not None:
            title += f" | Итерация: {self.iteration} | Исходный кластер: {self.initial_cluster + 1}"
        plots_window.title(title)

        fig = self.analyzer.create_cluster_plots(data)

        canvas = FigureCanvasTkAgg(fig, master=plots_window)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    def show_action_buttons(self):
        """Создает окно с кнопками для работы с кластерами.

        Создает окно с тремя группами кнопок:
        1. Для повторного анализа каждого кластера (1-4)
        2. Для построения тепловых карт (1-4)
        3. Для сохранения кластеров в CSV (1-4)

        В заголовке окна указывается номер итерации и исходного кластера (если есть).
        """
        action_window = tk.Toplevel(self.root)

        # Формируем заголовок с информацией об итерации и исходном кластере
        title = "Действия с кластерами"
        if self.initial_cluster is not None:
            title += f" | Итерация: {self.iteration} | Исходный кластер: {self.initial_cluster + 1}"
        action_window.title(title)

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

        # для сохранения кластеров в CSV
        save_frame = tk.Frame(action_window)
        save_frame.pack(pady=10)

        tk.Label(save_frame, text="Сохранить кластер в CSV:").pack()

        save_btn_frame = tk.Frame(save_frame)
        save_btn_frame.pack()

        for i in range(4):
            btn = tk.Button(save_btn_frame, text=str(i + 1),
                            command=lambda num=i: self.save_cluster_to_csv(num))
            btn.pack(side=tk.LEFT, padx=5)

    def show_heatmap(self, cluster_num):
        """Отображает тепловую карту для указанного кластера.

        вход:
            cluster_num (int): Номер кластера (0-3)

        Создает новое окно Toplevel с тепловой картой экспрессии генов выбранного кластера.
        В заголовке окна указывается номер кластера, итерации и исходного кластера (если есть).
        """
        fig = self.analyzer.create_heatmap(cluster_num)
        if fig:
            heatmap_window = tk.Toplevel(self.root)

            # Формируем заголовок с информацией об итерации и исходном кластере
            title = f"Тепловая карта кластера {cluster_num + 1}"
            if self.initial_cluster is not None:
                title += f" | Итерация: {self.iteration} | Исходный кластер: {self.initial_cluster + 1}"
            heatmap_window.title(title)

            canvas = FigureCanvasTkAgg(fig, master=heatmap_window)
            canvas.draw()
            canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        else:
            messagebox.showerror("Ошибка", "Не удалось построить тепловую карту")


if __name__ == "__main__":
    """Точка входа для запуска приложения.

    Создает главное окно Tkinter и запускает главный цикл приложения.
    """
    root = tk.Tk()
    app = ClusterAnalysisApp(root)
    root.mainloop()