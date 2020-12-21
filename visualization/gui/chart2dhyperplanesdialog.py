from .chart2ddialog import Chart2DDialog
from classification.hyperplane.hyperplaneclassifier import HyperplaneClassifier

class Chart2DHyperplanesDialog(Chart2DDialog):
    def __init__(self, parent, data, chart_canvas):
        super().__init__(parent, data, chart_canvas)
        self.hyperplanes = None
        self.xlims = None
        self.ylims = None

    def generate_chart(self):
        super().generate_chart()
        data2d = self.data[[self.x_column_name, self.y_column_name, self.class_column_name]]
        hyperplane_classifier = HyperplaneClassifier(data2d, self.class_column_name)
        hyperplane_classifier.build()

        x_min = data2d[self.x_column_name].min()
        x_max = data2d[self.x_column_name].max()
        y_min = data2d[self.y_column_name].min()
        y_max = data2d[self.y_column_name].max()

        self.xlims = (x_min, x_max)
        self.ylims = (y_min, y_max)
        self.hyperplanes = hyperplane_classifier.hyperplanes
