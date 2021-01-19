import Tree as t
import numpy as np

tree = t.kd_tree()

tree.construct_tree()

a= tree.data.loc[0,:].to_numpy()

b = tree.data.loc[1,:].to_numpy()

tree.data.sort_values(tree.data.columns[0],ascending = True,inplace = True)

tree.data.reset_index(drop=True,inplace=True)

c = tree.data

#c.loc[0:-1,:] differ from c.iloc[0:-1,:]
e =c.loc[0:3-1,:]
#type(c.loc[0:0,:]) = dataframe // type(c.loc[0,:]) = Series
f =c.loc[3+1:,:]

d = np.array([3,2])

k = tree.closest_node(tree.root,d)
