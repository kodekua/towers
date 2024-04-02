def is_intra_cluster_min(sub_cluster_Id, total_dist_cc, total_dist_road, threshold1, threshold2):
    # This function checks, for a given sub-cluster,
    # if the intra cluster values are below the predefined thresholds
    # It returns True if the sum of distance to cluster center
    # and the sum of distance to road are less than threshold1 and threshold2 respectively
    # It also outputs the ratios of the sum of distances of each cluster to the overall sum

    sub_clusters= get_sub_dataframe(cluster, 'sub_clusterId', sub_cluster_Id)
    # computing the ratios
    rate_dist_cc= (sub_clusters['dist_cc'].sum())/ total_dist_cc
    rate_dist_road= (sub_clusters['dist_road'].sum())/ total_dist_road
    
    return (rate_dist_cc< threshold1) and (rate_dist_road< threshold2), rate_dist_cc, rate_dist_road 

def intra_cluster_cost(cluster, threshold1, threshold2):
    # This function computes the intra cluster costs of a clustering process
    # It takes as inputs, the set of clusters and two predefined thresholds
    # then returns True if the clustering process is optimal or False otherwise,
    # it also outputs the minimum and maximum intra cluster values
    
    sub_clusters_Id= get_elements(cluster, 'sub_clusterId')
    total_dist_cc= cluster['dist_cc'].sum()
    total_dist_road= cluster['dist_road'].sum()
    # Variables to store results
    rates_dist_cc= []
    rates_dist_road= []
    bool_output= True


    for item in sub_clusters_Id:
        tmp= is_intracluster_min(sub_cluster_Id, total_dist_cc,  total_dist_road, threshod1, threshold2)
        bool_output= bool_output and tmp[0]
        rates_dist_cc.append(tmp[1])
        rates_dist_road.append(tmp[-1])

    return bool_output, (min(rates_dist_cc), max(rates_dist_cc)), (min(rates_dist_road), max(rate_dist_road))
