import matplotlib
matplotlib.use('Qt5Agg')

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure

class ChartCanvas(FigureCanvasQTAgg):
    def __init__(self, projection=None, parent=None, width=10, height=8, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        super(ChartCanvas, self).__init__(fig)
        self.axes = fig.add_subplot(111, projection=projection)
        if projection == "3d":
            self.axes.mouse_init()

    def save_chart(self, path):
        self.fig.savefig(path)
