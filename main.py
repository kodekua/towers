from models.clustering import corad
import pandas as pd

def main():
    input_data = pd.read_csv("data/data.csv")
    clustering = corad.Clustering()

    clustering.fit(input_data, epsilon=0.5, min_cluster_size=5, iteration=10)

    print("clusters: ", clustering.clusters.head(5), "Number of clusters: ", clustering.clusters_count, "Number of outliers: ", clustering.outliers_count)

if __name__== "__main__":
    main()