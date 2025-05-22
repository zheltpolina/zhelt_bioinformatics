import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler


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


def cluster_analysis(filepath, use_last_result=False):
    last_analysis_file = None

    try:
        #загрузка данных
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
            print("Кластерный анализ завершен")

        plt.figure(figsize=(10, 6))
        sns.scatterplot(data=data, x=data.columns[0], y=data.columns[1], hue='Cluster', palette='viridis')
        plt.title("Результаты кластерного анализа")
        plt.show()

    except Exception as e:
        print(f"Ошибка при выполнении: {e}")