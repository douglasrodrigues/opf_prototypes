import os
import sys
from ctypes import *

import numpy as np


class LibOPF:
    """A class to hold the LibOPF's integration.
    """

    def __init__(self):
        """Initialization method.
        """

        # Creates the OPF property
        self._OPF = CDLL(os.environ['OPF_DIR']+'/OPF.so')

    def wrap_function(lib, funcname, restype, argtypes):
        """Wraps a function using ctypes.
        Args:
            lib (func): The function pointer to be loaded.
            funcname (string): The name of the function.
            restype (types): Function's return type.
            argtypes (types): Types of the arguments.
        """

        # Gets the function object
        func = lib.__getattr__(funcname)

        # Gets the type of the response
        func.restype = restype

        # Gets the arguments' types
        func.argtypes = argtypes

        return func

class RealHeap(Structure, LibOPF):
    """A class to hold the RealHeap's structure.
    """
    
    # Fields that belongs to the structure
    _fields_ = [
        ("cost", POINTER(c_float)),
        ("color", POINTER(c_char)),
        ("pixel", POINTER(c_int)),
        ("pos", POINTER(c_int)),
        ("last", c_int),
        ("n", c_int),
        ("removal_policy", c_char)
    ]
    
    def __init__(self):
        """Initialization method.
        """

        # Override its parent class
        super().__init__()

class Set(Structure):
    """A class to hold the Set's structure.
    """
    pass

# Fields that belongs to the structure
Set._fields_ = [
    ("elems", c_int),
    ("next", POINTER(Set))
]


class SNode(Structure):
    """A class to hold the subgraph's Node structure.
    """

    # Fields that belongs to the structure
    _fields_ = [
        ("pathvalue", c_float),
        ("dens", c_float),
        ("radius", c_float),
        ("label", c_int),
        ("root", c_int),
        ("pred", c_int),
        ("truelabel", c_int),
        ("position", c_int),
        ("feat", POINTER(c_float)),
        ("status", c_char),
        ("relevant", c_char),
        ("nplatadj", c_int),
        ("adj", POINTER(Set))
    ]


class Subgraph(Structure, LibOPF):
    """A class to hold the Subgraph structure.
    """

    # Fields that belongs to the structure
    _fields_ = [
        ("node", POINTER(SNode)),
        ("nnodes", c_int),
        ("nfeats", c_int),
        ("bestk", c_int),
        ("nlabels", c_int),
        ("df", c_float),
        ("mindens", c_float),
        ("maxdens", c_float),
        ("k", c_float),
        ("ordered_list_of_nodes", POINTER(c_int))
    ]

    def __init__(self):
        """Initialization method.
        """

        # Override its parent class
        super().__init__()


class OPF(LibOPF):
    """Wraps methods from the LibOPF.
    """

    def __init__(self):
        """Initialization method.
        """

        # Overrides its parent class
        super().__init__()

    def _createrealheap(self, n, cost):
        
        # Creates the pointer to the function
        createrealheap = self._OPF.CreateRealHeap
        
        # Gets the type of the response
        createrealheap.restype = POINTER(RealHeap)
        
        # Gets the arguments types
        createrealheap.argtypes = [c_int, POINTER(c_float)]
        
        # Actually uses the function
        q = createrealheap(n, cost)
        
        return q
    
    def _insertrealheap(self, heap, pixel):
        
        # Creates the pointer to the function
        insertrealheap = self._OPF.InsertRealHeap
        
        # Gets the type of the response
        insertrealheap.restype = c_char
        
        # Gets the arguments types
        insertrealheap.argtypes = [POINTER(RealHeap), c_int]
        
        # Actually uses the function
        q = insertrealheap(heap, pixel)
        
        return q

    def _isemptyrealheap(self, heap):
        
        # Creates the pointer to the function
        isemptyrealheap = self._OPF.IsEmptyRealHeap
        
        # Gets the type of the response
        isemptyrealheap.restype = c_char
        
        # Gets the arguments types
        isemptyrealheap.argtypes = [POINTER(RealHeap)]
        
        # Actually uses the function
        q = isemptyrealheap(heap)
        
        return q
        
    def _removerealheap(self, heap, pixel):
        
        # Creates the pointer to the function
        removerealheap = self._OPF.RemoveRealHeap
        
        # Gets the type of the response
        removerealheap.restype = c_char
        
        # Gets the arguments types
        removerealheap.argtypes = [POINTER(RealHeap), POINTER(c_int)]
        
        # Actually uses the function
        q = removerealheap(heap, pixel)
        
        return q
        
    def _updaterealheap(self, heap, p, value):
        
        # Creates the pointer to the function
        updaterealheap = self._OPF.UpdateRealHeap
        
        # Gets the arguments types
        updaterealheap.argtypes = [POINTER(RealHeap), c_int, c_float]
        
        # Actually uses the function
        updaterealheap(heap, p, value)

    def _destroyrealheap(self, heap):
        """Destroys a heap.
        Args:
            heap (RealHeap): Heap object to be destroyed.
        """

        # Creates the pointer to the function
        destroyrealheap = self._OPF.DestroyRealHeap

        # Gets the arguments types
        destroyrealheap.argtypes = [POINTER(POINTER(RealHeap))]

        # Actually uses the function
        destroyrealheap(heap)

    def _createsubgraph(self, nnodes):
        """Allocate nodes without features.
        Args:
            nnodes (int): number of nodes.
        """

        # Creates the pointer to the function
        createsubgraph = self._OPF.CreateSubgraph

        # Gets the type of the response
        createsubgraph.restype = POINTER(Subgraph)

        # Gets the arguments types
        createsubgraph.argtypes = [c_int]

        # Actually uses the function
        g = createsubgraph(nnodes)

        return g

    def _readsubgraph(self, dataset):
        """Reads a subgraph from a .opf file.
        Args:
            dataset (string): Path to .opf dataset file.
        """

        # Creates the pointer to the function
        readsubgraph = self._OPF.ReadSubgraph

        # Gets the type of the response
        readsubgraph.restype = POINTER(Subgraph)

        # Gets the arguments types
        readsubgraph.argtypes = [c_char_p]

        # Actually uses the function
        g = readsubgraph(dataset)

        return g

    def _writesubgraph(self, subgraph, file_name):
        """Writes a subgraph to a .opf file.
        Args:
            subgraph (Subgraph): Subgraph object to be written.
            file_name (string): Path to the file that will be saved.
        """

        # Creates the pointer to the function
        writesubgraph = self._OPF.WriteSubgraph

        # Gets the arguments types
        writesubgraph.argtypes = [POINTER(Subgraph), c_char_p]

        # Actually uses the function
        writesubgraph(subgraph, file_name)

    def _destroysubgraph(self, subgraph):
        """Destroys a subgraph.
        Args:
            subgraph (Subgraph): Subgraph object to be destroyed.
        """

        # Creates the pointer to the function
        destroysubgraph = self._OPF.DestroySubgraph

        # Gets the arguments types
        destroysubgraph.argtypes = [POINTER(POINTER(Subgraph))]

        # Actually uses the function
        destroysubgraph(subgraph)

    def _splitsubgraph(self, sg, sg1, sg2, perc):
        
        # Creates the pointer to the function
        splitsubgraph = self._OPF.opf_SplitSubgraph
        
        # Gets the arguments types
        splitsubgraph.argtypes = [POINTER(Subgraph), POINTER(POINTER(Subgraph)), POINTER(POINTER(Subgraph)), c_float]
        
        # Actually uses the function
        splitsubgraph(sg, sg1, sg2, perc)

    def _copysubgraph(self, subgraph):
        
        # Creates the pointer to the function
        copysubgraph = self._OPF.opf_SplitSubgraph
        
        # Gets the type of the response
        copysubgraph.restype = POINTER(Subgraph)
        
        # Gets the arguments types
        copysubgraph.argtypes = [POINTER(Subgraph)]
        
        # Actually uses the function
        copysubgraph(subgraph)

    def _writemodelfile(self, subgraph, file_name):
        """Writes a subgraph to a model file.
        Args:
            subgraph (Subgraph): Subgraph object to be written.
            file_name (string): Path to the file that will be saved.
        """

        # Creates the pointer to the function
        writemodelfile = self._OPF.opf_WriteModelFile

        # Gets the arguments types
        writemodelfile.argtypes = [POINTER(Subgraph), c_char_p]

        # Actually uses the function
        writemodelfile(subgraph, file_name)

    def _readmodelfile(self, file_name):
        """Reads a model file to a subgraph.
        Args:
            file_name (string): Path to the model file that will be read.
        """

        # Creates the pointer to the function
        readmodelfile = self._OPF.opf_ReadModelFile

        # Gets the type of the response
        readmodelfile.restype = POINTER(Subgraph)

        # Gets the arguments types
        readmodelfile.argtypes = [c_char_p]

        # Actually uses the function
        g = readmodelfile(file_name)

        return g

    def _modelfile2txt(self):
        """Converts the classifier.opf from binary to text.
        """

        print('Converting classifier.opf from binary to text ...')

        # Creates the pointer to the function
        modelfile2txt = self._OPF.opf_ModelFile2Txt

        # Actually uses the function
        modelfile2txt()

    def _writeoutputfile(self, subgraph, file_name):
        """Writes an output file.
        Args:
            subgraph (Subgraph): Subgraph object to be written.
            file_name (string): Path to the file that will be saved.
        """

        # Creates the pointer to the function
        writeoutputfile = self._OPF.opf_WriteOutputFile

        # Gets the argument types
        writeoutputfile.argtypes = [POINTER(Subgraph), c_char_p]

        # Actually uses the function
        writeoutputfile(subgraph, file_name)

    def _readoutputfile(self, file_name, subgraph):
        """Reads an output file.
        Args:
            subgraph (Subgraph): Subgraph object to be read.
            file_name (string): Path to the file that will be read.
        """

        # Creates the pointer to the function
        readoutputfile = self._OPF.opf_ReadOutputFile

        # Gets the argument types
        readoutputfile.argtypes = [c_char_p, POINTER(Subgraph)]

        # Actually uses the function
        readoutputfile(file_name, subgraph)

    def _training(self, train):
        """Trains a model using supervised OPF.
        Args:
            train (Subgraph): Training subgraph.
        """

        # Creates the pointer to the function
        training = self._OPF.opf_OPFTraining

        # Gets the argument types
        training.argtypes = [POINTER(Subgraph)]

        # Actually uses the function
        training(train)

    def _classifying(self, train, test):
        """Classifies a model.
        Args:
            train (Subgraph): Training subgraph.
            test (Subgraph): Test subgraph.
        """

        # Creates the pointer to the function
        classifying = self._OPF.opf_OPFClassifying

        # Gets the argument types
        classifying.argtypes = [POINTER(Subgraph), POINTER(Subgraph)]

        # Actually uses the function
        classifying(train, test)

    def _accuracy(self, subgraph):
        """Computes the model's accuracy.
        Args:
            subgraph (Subgraph): Subgraph to compute its accuracy.
        """

        # Creates the pointer to the function
        accuracy = self._OPF.opf_Accuracy

        # Gets the type of the response
        accuracy.restype = c_float

        # Gets the argument types
        accuracy.argtypes = [POINTER(Subgraph)]

        # Actually uses the function
        result = accuracy(subgraph)

        return result
    
    def _alloc_float_array(self, n):
        
        alloc_float = self._OPF.AllocFloatArray
        
        alloc_float.restype = POINTER(c_float)
        
        alloc_float.argtype = c_int
        
        result = alloc_float(n)
        
        return result
    
    def _eucldistlog(self, f1, f2, n):
        """Compute discretized Euclidean distance between feature vectors.
        
        """

        # Creates the pointer to the function
        eucldistlog = self._OPF.opf_EuclDistLog

        # Gets the type of the response
        eucldistlog.restype = c_float

        # Gets the argument types
        eucldistlog.argtypes = [POINTER(c_float), POINTER(c_float), c_int]

        # Actually uses the function
        result = eucldistlog(f1, f2, n)

        return result

# --------------------------------------------------------------

def train(opf, train):
    """Performs the supervised OPF traning.
    Args:
        opf (OPF): OPF class instance.
        train (subgraph): Training subgraph.
    """

    # Performs the supervised OPF training
    opf._training(train)

    # Writes the model file
    opf._writemodelfile(train, 'classifier.opf'.encode('utf-8'))

    # Writes the output file
    opf._writeoutputfile(train, 'training.dat.out'.encode('utf-8'))

    # Destroys the subgraph
    opf._destroysubgraph(train)

def classify(opf, test):
    """Performs the supervised OPF classification.
    Args:
        opf (OPF): OPF class instance.
        test (subgraph): Testing subgraph.
    """
    
    # Reads the model file
    train = opf._readmodelfile('classifier.opf'.encode('utf-8'))

    # Performs the supervised OPF classification
    opf._classifying(train, test)

    # Writes the output file
    opf._writeoutputfile(test, 'testing.dat.out'.encode('utf-8'))

    # Destroys the subgraph
    opf._destroysubgraph(test)


def acc(opf, test):
    """Performs the OPF accuracy computation.
    Args:
        opf (OPF): OPF class instance.
        test (subgraph): Testing subgraph.
    """

    # Reads the output file
    opf._readoutputfile('testing.dat.out'.encode('utf-8'), test)

    # Performs the accuracy computation
    acc = opf._accuracy(test)

    print('Accuracy: %.2f' % (acc*100))

    # Destroys the subgraph
    opf._destroysubgraph(test)

    return acc

def subgraph_from_selected_features(opf, sg, features):
    
    newsg = opf._createsubgraph(sg.contents.nnodes)
    
    newsg.contents.nlabels = sg.contents.nlabels
    
    newsg.contents.nfeats = 0;
    
    for i in range(sg.contents.nfeats):
        if (features[i]):
            newsg.contents.nfeats += 1
    
    for i in range(newsg.contents.nnodes):
        newsg.contents.node[i].feat = opf._alloc_float_array(newsg.contents.nfeats)
        newsg.contents.node[i].truelabel = sg.contents.node[i].truelabel
        newsg.contents.node[i].position = sg.contents.node[i].position
        
        k = 0
        
        for j in range(sg.contents.nfeats):
            if (features[j]):
                newsg.contents.node[i].feat[k] = sg.contents.node[i].feat[j]
                k += 1
    
    return newsg

def split_subgraph(opf, g, training_perc, evaluating_perc, testing_perc):
    
    if (training_perc + evaluating_perc + testing_perc) != 1.0:
        
        print('Percentage summation is not equal to 1')
        return
        
    if (training_perc == 0.0 and testing_perc == 0.0):
        
        print('Percentage of either training set or test set is equal to 0')
        return
    
    gaux = POINTER(Subgraph)()
    
    gtraining = POINTER(Subgraph)()
    
    gevaluating = POINTER(Subgraph)()

    gtesting = POINTER(Subgraph)()
    
    opf._splitsubgraph(g, byref(gaux), byref(gtesting), training_perc + evaluating_perc)
    
    if (evaluating_perc > 0):
        
        opf._splitsubgraph(gaux, byref(gtraining), byref(gevaluating), training_perc / (training_perc + evaluating_perc))
        
    else:
        
        gtraining = opf._copysubgraph(gaux)
        
    return gtraining, gevaluating, gtesting