import pandas as pd
import numpy as np

class node:


    def __init__(self,d):

        self.data = d
        self.right = None
        self.left = None


class kd_tree:

    

    def __init__(self):

        self.data = pd.read_excel("Data.xlsx",engine="openpyxl")
        self.root = node(None)
        self.dimension = self.data.shape[1]
        self.p = 2


    def construct_tree(self):

        #sort data
        self.data.sort_values(self.data.columns[0],ascending = True,inplace = True)

        #reset index
        self.data.reset_index(drop=True,inplace=True)

        # Current Depth
        depth = 0

        #get median index
        ind_median = self._get_median_index(self.data,1)

        #set root
        self.root = node(self.data.to_numpy()[ind_median,:])

        #left,right data segments
        left_seg = self.data.loc[0:ind_median-1,:]
        right_seg = self.data.loc[ind_median+1:,:]

        #bulid Tree
        self.root.left = self.node_allocator(left_seg,depth+1)
        self.root.right = self.node_allocator(right_seg,depth+1)
        

    def node_allocator(self,data,in_depth = 0):

        #Stopping condition
        if data.size == 0:

            return None#node(data.to_numpy())

        # Current Depth
        depth = in_depth
        dim = depth % self.dimension + 1

        #set data
        tmp = data.sort_values(data.columns[dim-1],ascending = True)
        tmp.reset_index(drop = True,inplace=True)

        #get median index
        ind_median = self._get_median_index(tmp,dim)

        #set current node
        curr_node = node(tmp.to_numpy()[ind_median,:])

        #left,right data segments
        left_seg = tmp.loc[0:ind_median-1,:]
        right_seg = tmp.loc[ind_median+1:,:]


        #Set left right node
        curr_node.left = self.node_allocator(left_seg,depth+1)
        curr_node.right = self.node_allocator(right_seg,depth+1)

        return curr_node
            


    #[Array] point 1,2
    def distance(self,point_1,point_2,p):

        sum_dis = 0

        for i in range(len(point_1)):

            sum_dis += pow( abs((point_1[i] - point_2[i])) , p )
            

        sum_dis = pow(sum_dis,pow(p,-1))
        
        return sum_dis
        

    # median index: return int
    def _get_median_index(self,data,dim):

        #sort data
        tmp = data.sort_values(data.columns[dim -1],ascending = True)

        #get data size
        size_of_array = tmp.shape[0]

        #get index
        if (size_of_array % 2) == 1:

            index = int((size_of_array - 1)/2)
       

        else:

            index = int(size_of_array / 2)


        return index

    #node1,node2: node pivot:array
    def _closer_node(self,node1,node2,pivot):
    
        if node1 is None:
                
                return node2

        if node2 is None:
                
                return node1

        dis_node1 = self.distance(node1.data,pivot,2)
        dis_node2 = self.distance(node2.data,pivot,2)

        if dis_node1 < dis_node2 :
                
                return node1

        else:
                
                return node2

   # currnode:node, pivot:array
    def closest_node(self,currnode,pivot,depth = 0):
        
        if currnode is None:

                return None

        l = depth % self.dimension 

        pivot_node = node(pivot)

        if currnode.data[l] <= pivot_node.data[l]:

                next_node = currnode.left
                brother_node = currnode.right

        else:

                next_node = currnode.right
                brother_node = currnode.left


        best_node = self._closer_node( self.closest_node(next_node,pivot,depth+1) , currnode , pivot) 

        if self.distance(best_node.data,pivot_node.data,self.p) > abs(currnode.data[l] - pivot_node.data[l]):

                best_node = self._closer_node( self.closest_node(brother_node,pivot,depth+1) , best_node , pivot)

        return best_node
        













        

        
