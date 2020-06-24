from random import randint
import numpy as np  		   	  			  	 		  		  		    	 		 		   		 		  
  		   	  			  	 		  		  		    	 		 		   		 		  
class RTLearner(object):  		   	  			  	 		  		  		    	 		 		   		 		  
  		   	  			  	 		  		  		    	 		 		   		 		  
    def __init__(self, leaf_size=1, verbose = False):  		   	  			  	 		  		  		    	 		 		   		 		  
        self.leaf_size = leaf_size
        self.verbose = verbose
        self.tree = None
        
  		   	  			  	 		  		  		    	 		 		   		 		  
    def author(self):  		   	  			  	 		  		  		    	 		 		   		 		  
        return 'tsaranga3' 
  		   	  			  	 		  		  		    	 		 		   		 		  
    def addEvidence(self,dataX,dataY):  		   	  			  	 		  		  		    	 		 		   		 		  
        """  		   	  			  	 		  		  		    	 		 		   		 		  
        @summary: Add training data to learner  		   	  			  	 		  		  		    	 		 		   		 		  
        @param dataX: X values of data to add  		   	  			  	 		  		  		    	 		 		   		 		  
        @param dataY: the Y training values  		   	  			  	 		  		  		    	 		 		   		 		  
        """  		   	  			  	 		  		  		    	 		 		   		 		  
        dataY = np.array([dataY])
        dataY_T = dataY.T
        dataXY = np.append(dataX,dataY_T,axis=1)
        self.tree = self.build_Tree(dataXY)
        
    
    
    def build_Tree(self,data):
        
        if(data.shape[0]<=self.leaf_size):
            return np.array([["Leaf",data[0,-1],None,None]])
        if(np.all(data[0,-1]==data[:,-1],axis=0)):
            return np.array([["Leaf",data[0,-1],None,None]])
        else:
            ## Dtermine the best feature to split
            feature_col = randint(0,data.shape[1]-2)
            ## use the best feature to split
            split_val = np.median(data[:,feature_col])
            if(split_val == max(data[:,feature_col])):
                return np.array([["Leaf",np.mean(data[:,-1]),None,None]])
            
            left_tree = self.build_Tree(data[data[:,feature_col]<=split_val])
            right_tree = self.build_Tree(data[data[:,feature_col]>split_val])
            root = np.array([[feature_col,split_val,1,left_tree.shape[0]+1]])
            left = np.append(root,left_tree,axis=0)
            return (np.append(left,right_tree,axis=0))
    

  	  			  	 		  		  		    	 		 		   		 		  
    def query(self,points):  		   	  			  	 		  		  		    	 		 		   		 		  
        """  		   	  			  	 		  		  		    	 		 		   		 		  
        @summary: Estimate a set of test points given the model we built.  		   	  			  	 		  		  		    	 		 		   		 		  
        @param points: should be a numpy array with each row corresponding to a specific query.  		   	  			  	 		  		  		    	 		 		   		 		  
        @returns the estimated values according to the saved model.  		   	  			  	 		  		  		    	 		 		   		 		  
        """  		   	  			  	 		  		  		    	 		 		   		 		  
        ans = []
        row_count = points.shape[0]
        for row in range(0,row_count):
            value = self.query_tree(points[row,:])
            ans.append(float(value))
            
        return ans
    
    def query_tree(self,points):
        
        row = 0
        
        while(self.tree[row,0]!='Leaf'):
            feature = self.tree[row,0]
            split_val = self.tree[row,1]
            
            if(points[int(float(feature))]<=float(split_val)):
                row = row + int(float(self.tree[row,2]))
            else:
                row = row + int(float(self.tree[row,3]))
                
        return self.tree[row,1]
    

if __name__=="main":
    print("RTLearner Implementation")