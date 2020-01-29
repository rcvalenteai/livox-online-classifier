from mlxtend.plotting import plot_confusion_matrix
import matplotlib.pyplot as plt
import numpy as np


def confusion_matrix(tn, fp, fn, tp):
    binary = np.array([[tn, fp],
                       [fn, tp]])

    fig, ax = plot_confusion_matrix(conf_mat=binary,
                                    show_absolute=True,
                                    show_normed=True,
                                    colorbar=True)
    plt.show()


confusion_matrix(500, 0, 67, 473)