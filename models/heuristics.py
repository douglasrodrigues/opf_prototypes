from opytimizer.optimizers.evolutionary import ga, hs
from opytimizer.optimizers.population import rfo
from opytimizer.optimizers.swarm import abc, ba, bwo, cs, fa, fpa, mrfo, pso
from opytimizer.optimizers.science import bh
from opytimizer.optimizers.social import bso


class Heuristic:
    """An Heuristic class helps users in selecting distinct optimization heuristics from the command line.
    """

    def __init__(self, obj, hyperparams):
        """Initialization method.
        Args:
            obj (Optimizer): An Optimizer-child instance.
            hyperparams (dict): Heuristic hyperparams.
        """

        # Creates a property to hold the class itself
        self.obj = obj

        # Creates a property to hold the hyperparams
        self.hyperparams = hyperparams


# Defines an heuristic dictionary constant with the possible values
HEURISTIC = dict(
    abc=Heuristic(abc.ABC, dict(n_trials=10)),
    ba=Heuristic(ba.BA, dict(f_min=0, f_max=2, A=0.5, r=0.5)),
    bh=Heuristic(bh.BH, dict()),
    bso=Heuristic(bso.BSO, dict(k=3, p_one_cluster=0.3, p_one_center=0.4, p_two_centers=0.3)),
    bwo=Heuristic(bwo.BWO, dict(pp=0.6, cr=0.44, pm=0.4)),
    cs=Heuristic(cs.CS, dict(alpha=1, beta=1.5, p=0.2)),
    fa=Heuristic(fa.FA, dict(alpha=0.5, beta=0.2, gamma=1.0)),
    fpa=Heuristic(fpa.FPA, dict(beta=1.5, eta=0.2, p=0.8)),
    ga=Heuristic(ga.GA, dict(p_selection=0.75, p_mutation=0.25, p_crossover=0.5)),
    hs=Heuristic(hs.HS, dict(HMCR=0.7, PAR=0.7, bw=1.0)),
    mrfo=Heuristic(mrfo.MRFO, dict(S=2)),
    pso=Heuristic(pso.PSO, dict(w=0.7, c1=1.7, c2=1.7)),
    rfo=Heuristic(rfo.RFO, dict(p_replacement=0.5))
)

def get_heuristic(name):
    """Gets an heuristic by its identifier.
    Args:
        name (str): Heuristic's identifier.
    Returns:
        An instance of the MetaHeuristic class.
    """

    # Tries to invoke the method
    try:
        # Returns the corresponding object
        return HEURISTIC[name]

    # If object is not found
    except:
        # Raises a RuntimeError
        raise RuntimeError(f'Heuristic {name} has not been specified yet.')