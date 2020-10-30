import matplotlib
matplotlib.use('Qt5Agg')

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure

class ChartCanvas(FigureCanvasQTAgg):
    def __init__(self, projection=None, parent=None, width=10, height=8, dpi=150, subplots=1):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        super(ChartCanvas, self).__init__(self.fig)
        self.axes = []

        if subplots == 1:
            rows = 1
            columns = 1
        elif subplots == 2:
            rows = 1
            columns = 2
        elif subplots == 3 or subplots == 4:
            rows = 2
            columns = 2

        last_ax = None
        for i in range(1, subplots + 1):
            ax = self.fig.add_subplot(rows, columns, i, projection=projection, sharex=last_ax, sharey=last_ax)
            if projection == "3d":
                ax.mouse_init()
            self.axes.append(ax)
            last_ax = ax

    def get_subplot(self, index):
        return self.axes[index]

    def save_chart(self, path):
        self.fig.savefig(path)

    def tight_layout(self):
        self.fig.tight_layout()

    def hide_xticklabels(self, ax):
        for tick in ax.get_xticklabels():
            tick.set_visible(False)

    def hide_yticklabels(self, ax):
        for tick in ax.get_yticklabels():
            tick.set_visible(False)
