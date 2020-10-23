from .classifiertester import ClassifierTester

class LeaveOneOutTester(ClassifierTester):
    def __init__(self, data, class_column_name):
        super().__init__(data, class_column_name)

    def test_classifier(self, classifier):
        correct = 0
        classifier.prepare()
        n = len(self.data.index)

        for index, test_row in self.data.iterrows():
            classify_data = self.data.drop(index)
            row_no_class = test_row.drop(self.class_column_name)
            classifier.update_data(classify_data)

            result = classifier.classify(row_no_class)
            if result == test_row[self.class_column_name]:
                correct += 1

            self.progress_callback(int(round(index / n * 100)))
        return correct
