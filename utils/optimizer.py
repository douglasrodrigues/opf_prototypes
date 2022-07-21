from opytimizer import Opytimizer
from opytimizer.core import Function
from opytimizer.spaces import SearchSpace
from opytimizer.utils.callback import DiscreteSearchCallback

def optimize(opt, target, n_agents, n_variables, n_iterations, lb, ub, hyperparams):
    """Abstracts all Opytimizer's mechanisms into a single method.
    Args:
        opt (Optimizer): An Optimizer-child class.
        target (callable): The method to be optimized.
        n_agents (int): Number of agents.
        n_variables (int): Number of variables.
        n_iterations (int): Number of iterations.
        lb (list): List of lower bounds.
        ub (list): List of upper bounds.
        hyperparams (dict): Dictionary of hyperparameters.
    Returns:
        A History object containing all optimization's information.
    """
    
    # Defines the allowed values for performing the discrete search
    allowed_values = [list(range(lower_bound, upper_bound+1)) for lower_bound, upper_bound in zip(lb, ub)]

    # Creates space, optimizer and function
    space = SearchSpace(n_agents, n_variables, lb, ub)
    optimizer = opt(hyperparams)
    function = Function(target)

    # Creates the optimization task
    task = Opytimizer(space, optimizer, function)

    # Initializing task
    task.start(n_iterations, callbacks=[DiscreteSearchCallback(allowed_values=allowed_values)])

    return task.history