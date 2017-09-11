import matplotlib.pyplot as plt


class Plotter(object):
    line_style = {
        0: 'ro',
        1: 'gs',
        2: 'b^'
    }

    def __init__(self, x=None, y=[], output_file="plot.pdf", title=None, x_label=None, y_label=None):
        self._x = x
        self._y = y
        self._output_file = output_file
        self._x_label = x_label
        self._y_label = y_label
        self._title = title

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, x):
        self._x = x

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, y):
        self._y = y

    @property
    def output_file(self):
        return self._output_file

    @output_file.setter
    def output_file(self, output_file):
        self._output_file = output_file

    @property
    def x_label(self):
        return self._x_label

    @x_label.setter
    def x_label(self, x_label):
        self._x_label = x_label

    @property
    def y_label(self):
        return self._y_label

    @y_label.setter
    def y_label(self, y_label):
        self._y_label = y_label

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, title):
        self._title = title

    def plot(self):
        for i in range(len(self.y)):
            #plt.subplot(len(self.y), 1, i)
            plt.plot(self.x, self.y[i], self.line_style[i])
            plt.xlabel(self.x_label)
            plt.ylabel(self.y_label)
        plt.title(self.title)
        plt.savefig(self.output_file, format='pdf')
        plt.show()


def main():
    plotter = Plotter([0,1,2,3,4], y=[[2,3,4,5,6], [5,6,7,8,9]])
    plotter.plot()

if __name__ == "__main__":
    main()
