import matplotlib.pyplot as plt
import numpy as np

def generate_diagram(x_axis, y_axis, title, color, filename):
    """
    Example:
    x_axis = ["2020", "2021", "2022"]
    y_axis = [17138, 19271, 28444]
    """
    x = np.arange(len(x_axis))

    fig, ax = plt.subplots()
    rects1 = ax.bar(x, y_axis, width = 0.35, color = [color])
    ax.set_title(title)
    ax.set_ylabel('Anzahl Radfahrende')
    ax.set_xticks(x, x_axis)
    ax.bar_label(rects1, padding=3)
    fig.tight_layout()
    plt.savefig(filename, format="png")
    #plt.show()

