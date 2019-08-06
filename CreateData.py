def Create_Exp_Clustered_Data(mu, sigma, nobs, nclusters, lambda_param, rand_seed = 1):
    import math
    import pandas as pd
    import numpy as np

    data = np.random.normal(size = nobs, loc = mu, scale = sigma)
    val_1, val_2 = [], []
    for i in list(range(0, nclusters)):
        val_1.append(lambda_param*(math.e**(-lambda_param*i)))  
    for j in val_1:
        val_2.append(j/sum(val_1))
    del val_1
    cluster_indices = list(range(1,len(val_2)+1,1))
    cluster_df = pd.DataFrame({'index': cluster_indices, 'share': val_2}) 
    cluster_df['cumsum'] = cluster_df['share'].cumsum(axis = 0) 
    cluster_df = pd.concat([cluster_df, cluster_df['cumsum'].shift()], axis=1)
    cluster_df.fillna(0, inplace=True)
    cluster_df.columns = ['index', 'share', 'ub', 'lb']
    delimiter_tuples = list(zip(cluster_df['lb'].tolist(), cluster_df['ub'].tolist())) 
    result_tuples = []
    for val in data:
        for t in range(0, len(delimiter_tuples),1):
            if val >= delimiter_tuples[t][0] and val <= delimiter_tuples[t][1]:
                result_tuples.append((cluster_df['index'].tolist()[t], val))
                break
    return pd.DataFrame(result_tuples, columns =['Cluster', 'Value']) 


def Create_AB_Data(mu, reldiff, sigma, nobs, nclusters, lambda_param, rand_seed = 1):
    import random
    import numpy as np
    from StatExplore import CreateData as cd
    
    data = cd.Create_Exp_Clustered_Data(mu, sigma, nobs, nclusters, 
                                        lambda_param, rand_seed)
    rand = []
    for i in range(0, len(data),1):
        rand.append(random.random())
    data['rand'] = rand
    data['Treated'] = np.where(data['rand']<=0.5, 1, 0)
    data = data[['Cluster', 'Value', 'Treated']]
    return data