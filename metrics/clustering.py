import numpy as np
import pandas as pd
import haversine as hv


class Metrics():
    def __init__(self):
        self.intra_cluster = np.array([{'Sub_clusterId': 0.0 }])
        self.inter_cluster = np.array([{'Sub_clusterId': [] }])
        self.silhouette = np.array([{'Sub_clusterId': [] }])
        self.global_silhouette = 0.0
    
    @classmethod
    def get_elements_from_column(self, dataset:pd.DataFrame, column_name:str):
        """
        This function returns a list of distinct elements of a given column
        """
        count_series = dataset[column_name].value_counts()
        values = count_series.keys()
        return values.to_list()

    def set_intra_cluster(self, dataset:pd.DataFrame):
        """
        This function computes the intra cluster distance of each sub clutser
        It returns a list intra cluster distances
        """
        sub_clusterIds = self.get_elements_from_column(dataset, 'sub_clusterId')
        list_intra_cluster = []
        for scId in sub_clusterIds:
            sub_cluster = dataset[dataset.sub_clusterId == scId]
            dist_cc = sub_cluster.dist_cc
            list_intra_cluster.append({str(scId): dist_cc.array.sum()})
        self.intra_cluster = np.array(list_intra_cluster)


    def set_inter_cluster(self, dataset:pd.DataFrame):
        """
        This function computes the inter cluster distance of each sub clutser
        It returns a list inter cluster distances
        """
        sub_clusterIds = self.get_elements_from_column(dataset, 'sub_clusterId')
        list_inter_cluster = []
        for scId in sub_clusterIds:
            inter_dist=[]
            sub_cluster = dataset[dataset.sub_clusterId == scId]
            if len(sub_cluster)>0:
                min_dist = sub_cluster.dist_cc.array.min()
                center = sub_cluster[sub_cluster.dist_cc == min_dist]
                #
                if len(center)>1:
                    center = center.tail(1)
                center_coordinates = (center.lat.values[-1], center.lon.values[-1])
                #
                for next_scId in sub_clusterIds:
                    if next_scId != scId:
                        next_sub_cluster = dataset[dataset.sub_clusterId == next_scId]
                        if len(next_sub_cluster)>0:
                            min_dist = next_sub_cluster.dist_cc.array.min()
                            next_center = next_sub_cluster[next_sub_cluster.dist_cc == min_dist]
                            #
                            if len(next_center)>1:
                                next_center = next_center.tail(1)
                            next_center_coordinates = (next_center.lat.values[-1], next_center.lon.values[-1])
                            dist = hv.haversine(center_coordinates, next_center_coordinates, unit=hv.Unit.KILOMETERS)
                            inter_dist.append(dist)

            list_inter_cluster.append({str(scId):inter_dist})
        self.inter_cluster = np.array(list_inter_cluster)


    def set_silhouette(self, dataset:pd.DataFrame):
        """
        This function computes the silhouette coefficient for each cell clustered site
        It returns a list of silhouette coefficients
        """
        sub_clusterIds = self.get_elements_from_column(dataset, 'sub_clusterId')
        list_silhouette = []
        list_global_silhouette = []

        for scId in sub_clusterIds:
            silhouette_b=[]
            sub_cluster = dataset[dataset.sub_clusterId == scId]
            if len(sub_cluster)>1:
                dist_cc = sub_cluster.dist_cc
                a_coeff = dist_cc.array.mean()

                min_dist = sub_cluster.dist_cc.array.min()
                center = sub_cluster[sub_cluster.dist_cc == min_dist]
                if len(center)>1:
                    center = center.tail(1)
                center_coordinates = (center.lat.values[-1], center.lon.values[-1])

            for next_scId in sub_clusterIds:
                if next_scId != scId:
                    next_sub_cluster = dataset[dataset.sub_clusterId == next_scId]
                    if len(next_sub_cluster)>0:
                        min_dist = next_sub_cluster.dist_cc.array.min()
                        next_center = next_sub_cluster[next_sub_cluster.dist_cc == min_dist]
                    if len(next_center)>1:
                        next_center = next_center.tail(1)
                        next_center_coordinates = (next_center.lat.values[-1], next_center.lon.values[-1])
                        dist = hv.haversine(center_coordinates, next_center_coordinates, unit=hv.Unit.KILOMETERS)
                        silhouette_b.append(dist)
            b_coeff = np.mean(silhouette_b)
            coefficient = (b_coeff - a_coeff)/np.amax(np.array([a_coeff,b_coeff]))
            list_silhouette.append({str(scId): coefficient})
            list_global_silhouette.append(coefficient)
        self.silhouette = np.array(list_silhouette)
        self.global_silhouette = np.mean(list_global_silhouette)
