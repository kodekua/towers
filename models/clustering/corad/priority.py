def update_cell_priority(sub_cluster, cellId, threshold1, threshold2):
    # This function updates the priority of a given cell site

    cell_site= get_sub_dataframe(sub_cluster, 'cell', cellId)
    priority= cell_site['priority']

    if threshold1 > threshod2:
        if cell_site['traffic'] >= threshod1:
            priority= 1
        elif cell_site['traffic'] >= threshod2:
            priority= 2
        else:
            if cell_site['type']=='c3':
                priority= 3
            else:
                priority= 4
    return priority


def update_cluster_priority(sub_cluster_Id, threshold1, threshold2):
    #
    sub_cluster= get_sub_dataframe(dataframe, 'sub_clusterId', sub_cluster_Id)
    cell_sites_Id= get_elements(sub_cluster, 'cell')
    cluster_priority= []

    for cId in cell_sites_Id:
        tmp= update_cell_priority(sub_cluster, cId, threshold1, threshold2)
        cluster_priority.append(tmp)
    
    return cluster_priority

def update_priorities(dataframe, threshold1, threshold2):
    #
    clusters_Id= get_elements(dataframe, 'sub_clusterId')
    priorities= []
    
    for cId in clusters_Id:
        tmp= update_cluster_priority(cId, threshold1, threshold2):
        priorities= priorities + tmp
    
    dataframe.priority= priorities