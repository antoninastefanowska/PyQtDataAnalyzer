from PyQt5.QtCore import QThreadPool

from classification.utils.testingworker import TestingWorker
from classification.gui.progresswindow import ProgressWindow

from classification.knn.knnclassifier import KNNClassifier
from metrics.metricsfactory import MetricsFactory
from metrics.precalculateddistance import PrecalculatedDistance
from classification.utils.testingmanager import TestingManager
from classification.leaveoneouttester import LeaveOneOutTester

from visualization.chartcanvas import ChartCanvas
from visualization.gui.chartwindow import ChartWindow
from visualization.utils.colorgenerator import ColorGenerator

class KNNTestingManager(TestingManager):
    def __init__(self, context, data, class_column_name):
        super().__init__(context, data, class_column_name)

    def run_parameter_testing(self):
        self.progress_window = ProgressWindow(self.context)
        self.progress_window.show()
        self.run_single_parameter_test(0)

    def run_single_parameter_test(self, metrics_id):
        k_values = range(1, len(self.data.index) + 1)
        metrics = MetricsFactory.get_by_id(metrics_id, self.data)

        distances = PrecalculatedDistance(self.data, self.class_column_name, metrics)
        classifier = KNNClassifier(self.data, self.class_column_name, distances)
        tester = LeaveOneOutTester(self.data, self.class_column_name)

        worker = TestingWorker(tester, classifier, k_values)
        worker.signals.progress.connect(self.update_progress)
        worker.signals.status.connect(self.update_status)
        worker.signals.result_set.connect(self.finish_test_session)

        QThreadPool.globalInstance().start(worker)

    def finish_test_session(self, result_set):
        self.test_count += 1
        self.all_results.append(result_set)
        if self.test_count < MetricsFactory.get_count():
            self.run_single_parameter_test(self.test_count)
        else:
            count = MetricsFactory.get_count()
            chart_canvas = ChartCanvas(subplots=count)
            data_count = len(self.data.index)

            x = range(1, len(self.data.index) + 1)
            for i in range(0, MetricsFactory.get_count()):
                chart = chart_canvas.get_subplot(i)
                y = [int(round(value / data_count * 100)) for value in self.all_results[i]]

                chart.plot(x, y, color=ColorGenerator.get_color(i), marker="o")
                chart.set_title("Metryka " + MetricsFactory.NAMES[i])

                if i == 2 or i == 3:
                    chart.set_xlabel("Liczba K")
                else:
                    chart_canvas.hide_xticklabels(chart)
                if i == 0 or i == 2:
                    chart.set_ylabel("Jakość klasyfikacji [%]")
                else:
                    chart_canvas.hide_yticklabels(chart)

            chart_canvas.tight_layout()
            chart_window = ChartWindow(self.context, chart_canvas)
            chart_window.show()
            self.progress_window.finish()
            self.progress_window = None
