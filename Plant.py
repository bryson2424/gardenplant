# Defines our plant class


class Plant:
    """
    Represents our plant
    """
    def __init__(self, name=None):
        self.name = name
        self.imageKey = name+'-image'
        self.tempKey = name+'-temp'
        self.moistureKey = name+'-moisture'

