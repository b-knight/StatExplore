def CreateData(ob_mean = 0.5, 
               mde = 0.01,
               ob_sigma = 0.1, 
               n_obs = 10000,
               n_clusters = 100, 
               lambda_param = 1.0):
    import random
    import numpy as np
    import pandas as pd
    from scipy.stats import expon
    # create the observations

    data = list(np.random.normal(size = n_obs, loc = ob_mean, scale = ob_sigma))
    rand = [random.random() for i in data]
    data_list_of_lists = [list(i) for i in zip(data, rand)]

    # https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.expon.html#scipy.stats.expon
    # A common parameterization for expon is in terms of the rate parameter lambda, 
    # such that pdf = lambda * exp(-lambda * x). 
    # This parameterization corresponds to using scale = 1 / lambda.

    # divide 5 standard deviations worth of probability space into 'n_clusters' number of subspaces
    cdf = list(np.linspace(0, 5, n_clusters, endpoint = False))
    ppf = []
    for i in range(0,len(cdf),1):
        ppf.append(expon.cdf(cdf[i], scale = (1.0 / lambda_param)))
    ppf.append(1.0)

    # create a list of tuples with the probaility space delimitations
    a = ppf[0:len(ppf)-1]
    b = ppf[1:len(ppf)]
    delimiter_list_of_lists = [list(i) for i in zip(a, b)]
    k = 1
    for i in delimiter_list_of_lists:
        i.append(k)
        k +=1

    # assign the data to the appropriate cluster based on where the random float
    # falls within the delimiter_list_of_lists
    for i in data_list_of_lists:
        for j in delimiter_list_of_lists:
            if (i[1] >= j[0]) and (i[1] < j[1]):
                i.append(j[2])
                break

    # assemble the dataframe 
    cluster_df = pd.DataFrame(data_list_of_lists) 
    cluster_df.drop(cluster_df.columns[1], axis=1, inplace=True)
    cluster_df.columns = ['Value', 'Cluster']

    rand = []
    for i in range(0, len(list(cluster_df['Cluster'].unique())),1):
        if random.random() <= 0.5:
            rand.append(0)
        else:
            rand.append(1)

    cluster_list = list(cluster_df['Cluster'].unique())        
    rand_df = pd.DataFrame({'Cluster': cluster_list, 'Treatment': rand})  
    df = pd.merge(cluster_df, rand_df, on='Cluster', how='inner')

    # apply the mde
    df['Post-Treatment Value'] = np.where(df['Treatment']==1, df['Value']*(1+mde), df['Value'])
    df = df[['Post-Treatment Value', 'Cluster', 'Treatment']]
    df.columns = ['Value', 'Cluster', 'Treatment']
    
    # transparency of result set
    treated_mean = round(df[df['Treatment']==1]['Value'].mean(), 4)
    treated_std = round(df[df['Treatment']==1]['Value'].std(), 4)
    untreated_mean = round(df[df['Treatment']==0]['Value'].mean(), 4)
    untreated_std = round(df[df['Treatment']==0]['Value'].std(), 4)
    print("The dataset contains {:,} observations with {} distinct clusters.".format(len(df), 
          len(cluster_list)))
    print("{} of these clusters ({}%) are denoted as treated.".format(sum(rand), 
          int((sum(rand)/len(rand))*100)))
    print("The data is clustered exponentially with a lambda value of {}.".format(lambda_param))
    print("The treated observations have a mean of {} ".format(treated_mean) + \
          "and a standard deviation of {}.".format(treated_std ))
    print("The untreated observations have a mean of {} ".format(untreated_mean) + \
          "and a standard deviation of {}.".format(untreated_std ))
    return df