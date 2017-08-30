import matplotlib.pyplot as plt


class Plotter(object):
    line_style = {
        0: 'ro',
        1: 'gs',
        2: 'b^'
    }

    def __init__(self, x=None, y=[], output_file="plot.pdf"):
        self._x = x
        self._y = y
        self._output_file = output_file

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

    def plot(self):
        for i in range(len(self.y)):
            plt.subplot(len(self.y), 1, i)
            plt.plot(self.x, self.y[i], self.line_style[i])
        plt.savefig(self.output_file, format='pdf')
        plt.show()


def main():
    plotter = Plotter([0,1,2,3,4], y=[[2,3,4,5,6], [5,6,7,8,9]])
    plotter.plot()

if __name__ == "__main__":
    main()
