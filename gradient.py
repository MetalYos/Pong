

class Gradient():
    def __init__(self, first_color, last_color):
        self.gradient = [(first_color, 0.0), (last_color, 1.0)]
        self.__epsilon = 0.00001

    def add_color(self, color, position):
        if position < 0 or position > 1.0:
            return

        if position > 1.0 - self.__epsilon and position < 1.0 + self.__epsilon:
            self.gradient[-1] = (color, position)

        for i in range(len(self.gradient) - 1):
            if position > self.gradient[i][1] - self.__epsilon and position < self.gradient[i][1] + self.__epsilon:
                self.gradient[i] = (color, position)

            if position > self.gradient[i][1] and position < self.gradient[i + 1][1]:
                self.gradient.insert(i + 1, (color, position))

    def get_color(self, position):
        if position < 0:
            return self.gradient[0][0]
        if position > 1:
            return self.gradient[-1][0]
        if position > 1.0 - self.__epsilon and position < 1.0 + self.__epsilon:
            return self.gradient[-1][0]

        for i in range(len(self.gradient) - 1):
            pos1 = self.gradient[i][1]
            pos2 = self.gradient[i + 1][1]
            color1 = self.gradient[i][0]
            color2 = self.gradient[i + 1][0]

            if position > pos1 - self.__epsilon and position < pos1 + self.__epsilon:
                return color1

            if position > pos1 and position < pos2:
                t = (pos2 - position) / (pos2 - pos1)

                r = int(color1[0] * (1 - t) + color2[0] * t)
                g = int(color1[1] * (1 - t) + color2[1] * t)
                b = int(color1[2] * (1 - t) + color2[2] * t)

                return (r, g, b)

        return self.gradient[0][0]
