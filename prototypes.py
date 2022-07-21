import argparse
import pickle

import numpy as np

import opf_wrapper as wp

import models.heuristics as h
import utils.optimizer as p
import utils.targets as t
import utils.datasetinfo as d
import utils.outputter as o


def get_arguments():
    """Gets arguments from the command line.
    Returns:
        A parser with the input arguments.
    """

    # Creates the ArgumentParser
    parser = argparse.ArgumentParser(
        usage='OPF prototypes optimization using meta-heuristic approach.')
    
    parser.add_argument('dataset', help='Dataset identifier', choices=['iris', 'ionosphere'])

    parser.add_argument(
        'mh', help='Meta-heuristic identifier', choices=['abc', 'ba', 'bh', 'bso', 'bwo', 'cs', 'fa',
                                                         'fpa', 'ga', 'hs', 'mrfo', 'pso', 'rfo'])

    parser.add_argument(
        '-n_agents', help='Number of meta-heuristic agents', type=int, default=10)

    parser.add_argument(
        '-n_iter', help='Number of meta-heuristic iterations', type=int, default=3)

    parser.add_argument('-train_split', help='Percentage of the training set', type=float, default=0.3)
    
    parser.add_argument('-val_split', help='Percentage of the validation set', type=float, default=0.2)

    parser.add_argument('-test_split', help='Percentage of the testing set', type=float, default=0.5)

    parser.add_argument('-seed', help='Seed identifier', type=int, default=0)

    return parser.parse_args()


if __name__ == '__main__':
    # Gathers the input parsed arguments
    args = get_arguments()

    # Defining the numpy seed
    np.random.seed(args.seed)

    # Gathering the classifier
    clf = wp.OPF()

    g = clf._readsubgraph(f'./data/{args.dataset}.opf'.encode('utf-8'))

    gtrain, geval, gtest = wp.split_subgraph(clf, g, args.train_split, args.val_split, args.test_split)

    data_info = d.DatasetInfo(gtrain)

    # Initializes the optimization target
    opt_fn = t.prototypes_optimization(clf, gtrain, geval, data_info)

    mh = h.get_heuristic(args.mh).obj

    n_agents = args.n_agents

    n_iterations = args.n_iter

    n_variables = data_info.populate(0.2)

    # Setting lower and upper bounds
    lb = []
    ub = []

    for i in range(g.contents.nlabels):
        for j in range(data_info.classes[i].nprots):
            lb.append(0)
            ub.append(data_info.classes[i].nelems - 1)

    hyperparams = h.get_heuristic(args.mh).hyperparams

    history = p.optimize(mh, opt_fn, n_agents, n_variables,
                         n_iterations, lb, ub, hyperparams)
    
    # Dumps the object to file
    file_path = f'history/{args.dataset}_{args.train_split}_{args.val_split}_{args.test_split}_{args.mh}_{n_agents}ag_{n_iterations}iter_{args.seed}'
    with open(file_path+'.pkl', 'wb') as output_file:
        # Dumps object to file
        pickle.dump(history, output_file)

    # Gathering the best agent's position
    prototypes = [i[0] for i in history.best_agent[-1][0]]

    # Insert code to reset opf_PROTOTYPE flag
    # (0 - nothing, 1 - prototype)
    for node in range(gtrain.contents.nnodes):
        gtrain.contents.node[node].status = 0

    for i in range(gtrain.contents.nlabels):
        pos = 0
        for j in range(data_info.classes[i].nprots):
            
            gtrain.contents.node[data_info.classes[i].index[int(prototypes[pos])]].status = 1
            
            pos += 1

    # Performs the supervised OPF training
    clf._training(gtrain)

    # Performs the supervised OPF classification on test set
    clf._classifying(gtrain, gtest)

    # Performs the accuracy computation
    acc = clf._accuracy(gtest)

    # Process the optimization history
    fit, time = o.save_to_file(file_path, history, acc)

    print(f'------------------------------')
    print(f'Validation accuracy: {100-fit}')
    print(f'Testing accuracy: {acc*100}')
    print(f'Optimization time: {time}')