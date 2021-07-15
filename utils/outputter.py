import numpy as np


def save_to_file(output_path, history, test_acc):
    """Process an optimization history object and saves its output as readable files.
    Args:
        output_path (string): Path of the output file.
        history (opytimizer.utils.History): An optimization history.
        test_acc (float): Accuracy over testing set.
    """

    # Gathering fitness
    fit = history.best_agent[-1][1]

    # Gathering optimization time
    time = history.time[0]

    # Opening the output .txt file
    with open(output_path + '.txt', 'w') as output_file:
        # Saving fitness
        np.savetxt(output_file, [fit], header=f' Val accuracy (1) | Test Accuracy (1) | Time (1)')

        np.savetxt(output_file, [test_acc])

        # Saving optimization time
        np.savetxt(output_file, [time])

    return fit, time