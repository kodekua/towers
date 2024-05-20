
import pandas as pd
import numpy as np
import math
import haversine as hv
import concurrent.futures as ft

class Clustering:
    def __init__(self):
        self.clusters = pd.DataFrame(columns=['cell','mcc','net','area','lon','lat','zone','road', \
                                              'dist_road','traffic','priority','clusterId','dist_cc','sub_clusterId'])
        self.outliers = pd.DataFrame(columns=['cell','mcc','net','area','lon','lat','zone','road', \
                                              'dist_road','traffic','priority','clusterId','dist_cc','sub_clusterId'])
        self.clusters_count=0
        self.outliers_count=0


    @classmethod
    def  init_clusters(self, dataset:pd.DataFrame):
        """
        - set distance to cluster center to 999999999
        - set the sub clusters Id to zero
        """
        n_rows, n_cols = dataset.shape
        init_dist = 999999999*np.ones(n_rows)
        init_zeros = np.zeros(n_rows)
        dataset.insert(n_cols, 'dist_cc', init_dist, allow_duplicates=True)
        # sub-cluster initialisation
        dataset.insert(n_cols, 'sub_clusterId', init_zeros, allow_duplicates=True)


    @classmethod
    def get_elements_from_column(self, dataset:pd.DataFrame, column_name:str):
        """
        This function returns a list of distinct elements of a given column
        """
        count_series = dataset[column_name].value_counts()
        values = count_series.keys()
        return values.to_list()


    @classmethod
    def dist_to_cluster_center(self, dataset:pd.DataFrame, cluster_center:pd.DataFrame):
        """
        This function computes the distance between a cluster center and the cluster members.
        It takes as input a dataframe and Id of the cluster center
        and ouputs the dataframe with the computed distances as an additional column
        """
        haversine_dist = []

        cluster_center_coordinates = (cluster_center.lat.values[-1], cluster_center.lon.values[-1])
        cell_coordinates = [(dataset.lat.values[i],dataset.lon.values[i]) for i in range(len(dataset.lon.values))]

        for coordinates in cell_coordinates:
            dist = hv.haversine(cluster_center_coordinates, coordinates, unit=hv.Unit.KILOMETERS)
            haversine_dist.append(dist)

        dataset.loc[:, 'dist_cc'] = haversine_dist


    @classmethod
    def generate_cluster_centers(self, dataset:pd.DataFrame, number_of_clusters:int) -> list:
        """
        This function generates randomly cluster centers
        """
        list_of_cellIds = self.get_elements_from_column(dataset, 'cell')
        list_of_random_index = np.random.randint([i+3 for i in range(number_of_clusters)], len(list_of_cellIds))

        # Generate randomly number_of_clusters cluster centers
        cluster_centers_Id = [list_of_cellIds[index] for index in list_of_random_index]
        cluster_centers = []

        for k in range(number_of_clusters):
            center = dataset[dataset.cell == cluster_centers_Id[k]]
            if len(center)>1:
                center = center.tail(1)
            cluster_centers.append(center)
            # Remove cluster center from the dataset
            dataset = dataset.drop(center.index.values)

        return cluster_centers


    @classmethod
    def create_cluster(self,dataset:pd.DataFrame, epsilon:float, min_cluster_size:int):
        """
        This function generates randomly #number_of_clusters cluster centers
        and create a set of clusters whose distance to each center is lower than epsilon
        Input: -dataset = set of clusters obtained from the pre_clustering,
               -epsilon = threshold for the distance to cluster center
               -cluster_size = optimal number of elements of each cluster
        """

        self.init_clusters(dataset)
        data_size = len(dataset)
        number_of_clusters = math.ceil(data_size / min_cluster_size)

        # Generate randomly cluster centers
        cluster_centers = self.generate_cluster_centers(dataset, number_of_clusters)
        c_size = 0

        for k in range(number_of_clusters):
            cluster_tmp = pd.DataFrame(columns=['cell','mcc','net','area','lon','lat','zone','road', \
                                              'dist_road','traffic','priority','clusterId','dist_cc','sub_clusterId'])
            outlier_tmp = pd.DataFrame(columns=['cell','mcc','net','area','lon','lat','zone','road', \
                                              'dist_road','traffic','priority','clusterId','dist_cc','sub_clusterId'])

            if len(cluster_centers[k])!= 0:
                for index in dataset.index:
                    data_tmp = dataset[dataset.index == index]
                    self.dist_to_cluster_center(data_tmp, cluster_centers[k])

                    if data_tmp.dist_cc.values[-1] < epsilon:
                        data_tmp.loc[:, 'sub_clusterId'] = k+1
                        cluster_tmp = pd.concat([data_tmp, cluster_tmp])
                        print(f"[DEBUG] : Cluster size - {len(cluster_tmp)}\n {cluster_tmp}\n")
                        # Remove the cell site from dataset
                        dataset =  dataset.drop(data_tmp.index.values)

                self.clusters = pd.concat([self.clusters, cluster_tmp])
                print("Sub cluster:\t", k, "\t\t of size\t", len(cluster_tmp), "\tcreated")
                c_size = c_size + len(cluster_tmp)
        self.outliers = pd.concat([self.outliers, dataset[dataset.dist_cc >= epsilon]])
        print("----------- Number cellsites clustered:\t\t", c_size, "---------------")



    def fit(self, dataset:pd.DataFrame, epsilon:float, min_cluster_size:int):
        """
        This function run the correlation clustering algorithm for several datasets
        """
        # Get all the clusters ID
        dataframe = dataset.copy()
        list_of_clusterIds = self.get_elements_from_column(dataframe, 'clusterId')
        # with ft.ThreadPoolExecutor(max_workers=200) as executor:
        #     future = {executor.submit(self.create_cluster, dataframe[dataframe.clusterId == cId], epsilon, min_cluster_size): cId for cId in list_of_clusterIds}
        for cId in list_of_clusterIds:
            pre_cluster = dataframe[dataframe.clusterId == cId]
            if len(pre_cluster) > math.ceil(min_cluster_size / 1):
                print("--------- Creating sub_clusters for the precluster:\t",cId, "\t\t size of the precluster:\t", len(pre_cluster),"-----------")
                self.create_cluster(pre_cluster, epsilon, min_cluster_size)
            else:
                self.outliers = pd.concat([self.outliers, pre_cluster])
