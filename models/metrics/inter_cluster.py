def dist_min_cluster_to_cellsite(sub_cluster_Id, cellId):
    # This functions computes the minimum distance between a cell site and a cluster

    sub_cluster= get_sub_dataframe(cluster, 'sub_clusterId', sub_cluster_Id)
    cell_site= get_sub_dataframe(cluster, 'cell', cellId)
    cell_sites_Id= get_elements(sub_cluster, 'cell')
    harv_dist= []

    for item in cell_sites_Id:
        tmp= get_sub_dataframe(cluster, 'cell', item)
        harv= harvesine_distance(cell_site.lon, cell_site.lat, tmp.lon, tmp.lat)
        harv_dist.append(harv)
    
    return min(harv_dist)


def dist_min_cluster_to_cluster(sub_cluster_Id1, sub_cluster_Id2):
    # This function computes the minimum distance between two clusters
    
    sub_cluster1= get_sub_dataframe(cluster, 'sub_clusterId', sub_cluster_Id1)
    sub_cluster2= get_sub_dataframe(cluster, 'sub_clusterId', sub_cluster_Id2)
    cell_sites_Id= get_elements(sub_cluster1, 'cell')
    min_dist=[]
    
    for cellId in cell_sites_Id:
        tmp= dist_min_cluster_to_cellsite(sub_cluster_2, cellId)
        min_dist.append(tmp)
    
    return min(min_dist)


def dist_clusters_to_cluster(cluster, sub_cluster_Id):
    # This function computes the minimun distances between one cluster and N clusters

    cluster_min_dist= []
    clusters_Id= get_elements(sub_cluster1, 'sub_clusterId')

    for cId in clusters_Id:
        if cId != sub_cluster_Id:
            tmp= dist_min_cluster_to_cluster(sub_cluster_Id1, cId)
            cluster_min_dist.append(tmp)
    
    return min(cluster_min_dist)


def inter_cluster_cost(cluster, threshold):
    # This function computes the inter cluster cost of a clustering process
    # and outputs True if the inter cluster cost is bigger than a predefined threshold
    # it also output the maximum of the minimum distance between clusters
    
    clusters_Id= get_elements(cluster, 'sub_clusterId')
    cluster_max_dist= []

    for cId in clusters_Id:
        tmp= dist_clusters_to_cluster(cluster, cId)
        cluster_max_dist.append(tmp)
    max_dist= max(cluster_max_dist)
    
    return (max_dist> threshold), max_dist


