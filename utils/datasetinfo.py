import numpy as np

class ClassInfo:
    
    def __init__(self, nelems):
        
        # Number of elements on the list
        self.nelems = nelems
        
        # Number of prototypes in the given class
        self.nprots = 0
        
        # Index of the node in the subgraph
        self.index = np.zeros(self.nelems, dtype=int)
        
        # Position of the node in the full graph
        self.position = np.zeros(self.nelems, dtype=int)
        
        # (0) not used or (1) used
        self.flag = np.zeros(self.nelems, dtype=int)

class DatasetInfo:
    
    def __init__(self, g):

        self.g = g
        
        self.classes = []
        
        self.nelems = np.zeros(self.g.contents.nlabels, dtype=int)

        for i in range(self.g.contents.nnodes):
            self.nelems[self.g.contents.node[i].truelabel-1] += 1
        
        for i in range(self.g.contents.nlabels):
            self.classes.append(ClassInfo(self.nelems[i]))
    
    def populate(self, perc):
        
        list_position = np.zeros(self.g.contents.nlabels, dtype=int)

        for i in range(self.g.contents.nnodes):
            # Current position on the list
            curr_pos = list_position[self.g.contents.node[i].truelabel-1]

            self.classes[self.g.contents.node[i].truelabel-1].index[curr_pos] = i
            self.classes[self.g.contents.node[i].truelabel-1].position[curr_pos] = self.g.contents.node[i].position
            
            list_position[self.g.contents.node[i].truelabel-1] += 1
        
        # Number of decision variables
        n = 0
        
        # Defining the number of prototypes for each class
        for i in range(self.g.contents.nlabels):
            
            self.classes[i].nprots = int(max(perc * self.classes[i].nelems, 1))
            
            n += self.classes[i].nprots
        
        return n