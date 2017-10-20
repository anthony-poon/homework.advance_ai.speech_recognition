import numpy
class DynamicProgrammer:
    def __init__(self, a_matrix, b_matrix):
        # discard first 2 row
        self.__a_matrix = a_matrix[2::, ::]
        self.__b_matrix = b_matrix[2::, ::]

    def get_distortion(self):
        distortion_matrix = numpy.empty([self.__a_matrix.shape[1],self.__a_matrix.shape[1]])
        for a_index, a_segment in enumerate(self.__a_matrix.T):
            for b_index, b_segment in enumerate(self.__b_matrix.T):
                total = 0
                for a, b in zip(a_segment, b_segment):
                    total = total + (a - b) ** 2
                distortion_matrix[a_index, b_index] = total
        return distortion_matrix

    def get_accumulated(self):
        distortion_matrix = self.get_distortion()
        accumulated_matrix = numpy.empty(distortion_matrix.shape)
        for row, col in numpy.ndindex(distortion_matrix.shape):
            if row == 0 and col == 0:
                total = distortion_matrix[row, col]
            elif row == 0:
                total = distortion_matrix[row, col] + accumulated_matrix[row, col - 1]
            elif col == 0:
                total = distortion_matrix[row, col] + accumulated_matrix[row - 1, col]
            else:
                total = distortion_matrix[row, col] + min([
                    accumulated_matrix[row - 1, col],
                    accumulated_matrix[row, col - 1],
                    accumulated_matrix[row - 1, col - 1]
                ])
            accumulated_matrix[row, col] = total
        return accumulated_matrix

    def get_min_path(self):
        accumulated_matrix = self.get_accumulated()
        min_path_matrix = numpy.zeros(accumulated_matrix.shape, dtype=bool)
        min_path = [];
        min_value = float('inf')
        min_path_score = 0
        min_tuple = (0, 0)
        for row in range(accumulated_matrix.shape[0]):
            # find least in last col first then check last row
            if accumulated_matrix[row, -1] < min_value:
                min_tuple = (row, accumulated_matrix.shape[1] - 1)
                min_value = accumulated_matrix[row, -1]
        for col in range(accumulated_matrix.shape[1]):
            # find least in last col first then check last row
            if accumulated_matrix[-1, col] < min_value:
                min_tuple = (accumulated_matrix.shape[0] -1, col)
                min_value = accumulated_matrix[row, -1]
        runner = min_tuple
        min_path_matrix[runner] = True
        min_path.append(runner)
        min_path_score += accumulated_matrix[runner]
        while runner != (0, 0):
            if runner[0] == 0:
                runner = (0, runner[1] - 1)
                min_path_matrix[runner] = True
                min_path.append(runner)
                min_path_score += accumulated_matrix[runner]
            elif runner[1] == 0:
                runner = (runner[0] - 1, 0)
                min_path_matrix[runner] = True
                min_path.append(runner)
                min_path_score += accumulated_matrix[runner]
            else:
                next_runner_list = (
                    (runner[0] - 1, runner[1]),
                    (runner[0], runner[1] - 1),
                    (runner[0] - 1, runner[1] - 1),
                )
                next_value = float('inf')
                for n in next_runner_list:
                    if accumulated_matrix[n] < next_value:
                        next_value = accumulated_matrix[n]
                        runner = n
                min_path.append(runner)
            min_path_matrix[runner] = True
            min_path_score += accumulated_matrix[runner]
        return min_path_score, min_path, min_path_matrix
