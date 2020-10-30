import numpy

class ColorGenerator:
    COLORS = ['pink', 'skyblue', 'lightgreen', 'yellow', 'coral', 'crimson', 'cornflowerblue', 'lightseagreen', 'navy', 'saddlebrown', 'slategray', 'peru', 'darkslategray', 'darkkhaki', 'magenta', 'mediumslateblue']

    @staticmethod
    def get_color(index):
        if index < 15:
            return ColorGenerator.COLORS[index]
        else:
            return numpy.random.rand(3,)