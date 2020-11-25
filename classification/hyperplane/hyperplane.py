class Hyperplane:
    def __init__(self, orientation, point, column_name, class_value):
        self.orientation = orientation
        self.point = point
        self.column_name = column_name
        self.class_value = class_value

    def in_area(self, data_object):
        if self.orientation == 0:
            return data_object[self.column_name] <= self.point
        elif self.orientation == 1:
            return data_object[self.column_name] >= self.point
