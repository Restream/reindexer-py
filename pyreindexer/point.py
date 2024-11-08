class Point:
    """An object representing the context of a Reindexer 2D point

    #### Attributes:
        x (float): x coordinate of the point
        y (float): y coordinate of the point
    """

    def __init__(self, x: float, y: float):
        """Constructs a new Reindexer query object

        #### Arguments:
            x (float): x coordinate of the point
            y (float): y coordinate of the point

        """

        self.x: float = x
        self.y: float = y
