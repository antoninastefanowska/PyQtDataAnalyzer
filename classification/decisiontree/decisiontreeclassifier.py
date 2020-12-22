import math
import numpy as np

from ..classifier import Classifier
from .treenode import TreeNode

class DecisionTreeClassifier(Classifier):
    def __init__(self, data, class_column_name):
        super().__init__(data, class_column_name)
        self.tree = None
        self.node_count = 0

    def entropy(self, data):
        classes = data[self.class_column_name].unique()
        entropy = 0
        for class_key in classes:
            count = len(data[data[self.class_column_name] == class_key])
            probability = count / len(data)
            entropy -= probability * math.log2(probability)
        return entropy

    def find_attribute(self, data):
        min_entropy = -1
        best_attribute = None
        for column_name in data.columns:
            if column_name != self.class_column_name:
                values = data[column_name].unique()
                entropy = 0
                for value in values:
                    data_part = data[data[column_name] == value]
                    probability = len(data_part) / len(data)
                    class_entropy = self.entropy(data_part)
                    entropy += probability * class_entropy
                if entropy < min_entropy or min_entropy == -1:
                    min_entropy = entropy
                    best_attribute = column_name
        return best_attribute

    def build_node(self, data, test_value):
        self.node_count += 1
        entropy = self.entropy(data)
        if entropy == 0:
            class_value = data[self.class_column_name].iloc[0]
            return TreeNode(test_value=test_value, class_value=class_value, node_size=len(data))

        else:
            attribute = self.find_attribute(data)
            class_value = data[self.class_column_name].mode().iloc[0]
            if attribute is None:
                return TreeNode(test_value=test_value, class_value=class_value, node_size=len(data))

            node = TreeNode(attribute, test_value, class_value=class_value, node_size=len(data))
            values = np.sort(data[attribute].unique())
            for value in values:
                data_part = data[data[attribute] == value]
                data_part = data_part.drop(attribute, axis=1)
                node.add_child(self.build_node(data_part, value))
            return node

    def prune(self, tree):
        class_value = None
        homogenous = True
        for child in tree.children:
            self.prune(child)
            if child.is_leaf():
                if class_value is None:
                    class_value = child.class_value
                elif class_value != child.class_value:
                    homogenous = False
            else:
                homogenous = False
        if not tree.is_leaf() and homogenous:
            self.node_count -= tree.child_count()
            tree.turn_to_leaf(class_value)

    def build(self):
        self.tree = self.build_node(self.data, None)
        self.prune(self.tree)

    def update_data(self, data):
        super().update_data(data)
        self.build()

    def classify(self, data_object):
        return self.tree.get_class(data_object)

    def get_param_string(self):
        return "Liczba węzłów: " + str(self.node_count)

    def get_result_info_string(self):
        return "Liczba węzłów: " + str(self.node_count)

    def get_param_list(self):
        return [("Liczba węzłów", str(self.node_count))]

    def get_name(self):
        return "Drzewo"

    def get_classifier_output_data(self):
        return self.tree