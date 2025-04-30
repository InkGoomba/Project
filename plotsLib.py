class plots:

    def __init__(self):
        pass

    def plots_select(num):

        match num:
            case 0:
                points = [[0, 0], [1, 2], [4, 8], [3, 1], [5, 6]]
                edges = [[0, 1], [1, 3], [0, 3], [3, 4], [1, 4], [2, 4], [2, 1]]
                return points, edges
            case 1:
                points = [[0, 0], [2, 1], [3, 3], [1, 4], [4, 5]]
                edges = [[0, 1], [1, 2], [2, 3], [3, 4], [0, 2], [0, 3], [2, 4]]
                return points, edges
            case 2:
                points = [[0, 0], [2, 2], [4, 0], [3, 3], [1, 4]]
                edges = [[0, 1], [1, 2], [2, 3], [3, 4], [0, 3], [1, 4], [0, 4], [0, 2]]
                return points, edges
            case 3:
                points = [[1, 1], [3, 1], [2, 3], [4, 4], [0, 4]]
                edges = [[0, 1], [1, 2], [2, 3], [3, 4], [0, 2], [1, 3], [2, 4], [0, 4]]
                return points, edges
            case 4:
                points = [[0, 0], [2, 0], [1, 2], [3, 3], [4, 1]]
                edges = [[0, 1], [1, 2], [2, 3], [3, 4], [0, 2], [1, 3], [1, 4]]
                return points, edges
            case 5:
                points = [[0, 0], [1, 3], [3, 1], [4, 4], [2, 5]]
                edges = [[0, 1], [1, 2], [2, 3], [3, 4], [0, 2], [1, 4], [1, 3]]
                return points, edges
            case 6:
                points = [[0, 0], [2, 0], [1, 2], [3, 2], [4, 0]]
                edges = [[0, 1], [1, 2], [2, 3], [3, 4], [0, 2], [1, 3], [1, 4]]
                return points, edges
            case 7:
                points = [[0, 0], [2, 1], [1, 3], [3, 3], [4, 1]]
                edges = [[0, 1], [1, 2], [2, 3], [3, 4], [0, 2], [1, 3], [1, 4]]
                return points, edges
            case 8:
                points = [[0, 0], [1, 1], [2, 0], [3, 2], [4, 0]]
                edges = [[0, 1], [1, 2], [2, 3], [3, 4], [0, 2], [1, 3], [2, 4]]
                return points, edges
            case 9:
                points = [[0, 0], [2, 0], [1, 2], [3, 1], [4, 3]]
                edges = [[0, 1], [1, 2], [2, 3], [3, 4], [0, 2], [4, 2], [1, 3]]
                return points, edges
            case 10:
                points = [[0, 0], [1, 3], [3, 0], [2, 2], [4, 4]]
                edges = [[0, 1], [1, 2], [2, 3], [3, 4], [0, 2], [1, 3], [4, 1], [2, 4]]
                return points, edges