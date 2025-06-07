import pandas as pd
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import seaborn as sns


class ClusterAnalyzer:
    def __init__(self):
        self.expression_data = None
        self.stats_data = None
        self.current_clusters = None

    def load_expression_data(self, file_path):
        self.expression_data = pd.read_csv(file_path)

    def load_stats_data(self, file_path):
        self.stats_data = pd.read_csv(file_path)

    def perform_clustering(self, data=None):
        if data is None:
            data = self.stats_data

        # Выбираем признаки для кластеризации
        features = data[['median_tum', 'median_norm', 'M_W']]

        # Выполняем кластеризацию
        model = KMeans(n_clusters=4, random_state=42)
        model.fit(features)
        cluster_labels = model.labels_

        # Добавляем метки кластеров в данные
        data['labels_nse'] = cluster_labels
        self.current_clusters = data.copy()

        return data

    def get_cluster_data(self, cluster_num):
        if self.current_clusters is not None:
            return self.current_clusters[self.current_clusters['labels_nse'] == cluster_num]
        return None

    def create_cluster_plots(self, data):
        fig, axes = plt.subplots(2, 2, figsize=(12, 10))
        fig.suptitle("Кластерный анализ генов")

        for i in range(4):
            row, col = divmod(i, 2)
            cluster_data = data[data['labels_nse'] == i]

            if not cluster_data.empty:
                axes[row, col].plot(cluster_data['median_tum'], label='Опухоль')
                axes[row, col].plot(cluster_data['median_norm'], label='Норма')
                axes[row, col].set_title(f'Кластер {i + 1}')
                axes[row, col].legend()

        return fig

    def create_heatmap(self, cluster_num):
        if self.current_clusters is None:
            return None

        cluster_data = self.get_cluster_data(cluster_num)
        filter_df = self.expression_data[self.expression_data.gene_id.isin(cluster_data.gene_id)].reset_index(drop=True)
        filter_df = filter_df.T

        columns = filter_df.iloc[1].values
        filter_df = filter_df.drop(['Unnamed: 0', 'gene_id'])
        filter_df.columns = columns
        filter_df = filter_df.astype(float)

        fig, ax = plt.subplots(figsize=(10, 8))
        sns.heatmap(filter_df.iloc[:343, :], cmap='coolwarm', vmin=0, vmax=30, center=1, ax=ax)
        ax.set_title(f"Тепловая карта кластера {cluster_num + 1}")

        return fig