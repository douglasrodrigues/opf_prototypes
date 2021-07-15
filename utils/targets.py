

def prototypes_optimization(clf, sgtrain, sgeval, data_info):
    """Wraps the OPF prototypes optimization.

    Args:
        clf (Classifier): A classifier instance.
        sgtrain (subgraph): Subgraph of training data.
        sgeval (subgraph): Subgraph of training labels.
        data_info (DatasetInfo): object holding the dataset information.

    Returns:
        The wrapped function itself.
        
    """
    
    def opt_prototypes(g, data_info, w):
        
        # Insert code to reset opf_PROTOTYPE flag
        # (0 - nothing, 1 - prototype)
        for p in range(g.contents.nnodes):
            g.contents.node[p].status = 0
        
        for i in range(g.contents.nlabels):
            pos = 0
            for j in range(data_info.classes[i].nprots):
                
                g.contents.node[data_info.classes[i].index[int(w[pos])]].status = 1
                
                pos += 1
        
    def f(w):
        """Fits the classifier and compute its accuracy over the validation set.

        Args:
            w (float): Array of variables.

        Returns:
            1 - accuracy as the objective function.

        """
        
        opt_prototypes(sgtrain, data_info, w)
        
        # Performs the supervised OPF training
        clf._training(sgtrain)
        
        # Performs the supervised OPF classification
        clf._classifying(sgtrain, sgeval)
        
        # Performs the accuracy computation
        acc = clf._accuracy(sgeval)
        
        # Insert code to reset opf_PROTOTYPE flag
        for p in range(sgtrain.contents.nnodes):
            sgtrain.contents.node[p].status = 0

        #print(f"Acc: {acc}")
        return 1 - acc
    
    return f