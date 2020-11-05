from ..testingresultwindow import TestingResultWindow

class TestingManager:
    def __init__(self, context, data, class_column_name):
        self.context = context
        self.data = data
        self.class_column_name = class_column_name

        self.progress_window = None
        self.test_count = 0
        self.all_results = []

    def show_single_testing_result(self, result):
        result_window = TestingResultWindow(self.context, self.data, result)
        result_window.show()
        self.progress_window.finish()
        self.progress_window = None

    def update_progress(self, progress):
        self.progress_window.update(progress)

    def update_status(self, status):
        self.progress_window.update_status(status)
