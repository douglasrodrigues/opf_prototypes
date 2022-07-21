# Defining the dataset to be used
DATA="ionosphere"

# Defiing the training split
TRAIN_SPLIT=0.2

# Defining the validation split
VAL_SPLIT=0.3

# Defining the test split
TEST_SPLIT=0.5

# Defining a constant to hold the possible meta-heuristics
MH=("pso")

# Defining the number of agents
N_AGENTS=30

# Defining the number of iterations
N_ITER=10

# Defining the number of runs
N_RUNS=1

# Iterates through all possible seeds
for RUN in $(seq 1 $N_RUNS); do

    # Creating a loop of meta-heuristics
    for M in "${MH[@]}"; do
        # Performs the feature selection procedure
        python prototypes.py ${DATA} ${M} -n_agents ${N_AGENTS} -n_iter ${N_ITER} -train_split ${TRAIN_SPLIT} -val_split ${VAL_SPLIT} -test_split ${TEST_SPLIT} -seed ${RUN}

    done

done
