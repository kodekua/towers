# Towers
## How to
```bash
python3
>>> from models.clustering import corad
>>> clustering_instance=corad.Clustering()
>>> import pandas as pd
>>> input_data=pd.read_csv("data/data.csv")
>>> clustering_instance.fit(input_data, epsilon=0.5, min_cluster_size=5, iteration=10)
>>> print("clusters: ", clustering_instance.clusters.head(5))
```