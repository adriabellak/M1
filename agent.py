from mesa import Agent

class FloorTile(Agent):
    def __init__(self, pos, model):
        super().__init__(pos, model)
        self.pos = pos
        self.condition = "Clean"
        # available = True cuando el FloorTile tiene un Roomba encima, y se vuelve False cuando ese Roomba se mueve a otro FloorTile
        self.available = True

    def isAvailable(self):
        return self.available

    def step(self):
        pass

class Roomba(Agent):
    def __init__(self, id, pos, model):
        super().__init__(id, model)
        self.pos = pos
        self.nextPos = (-1, -1)
        self.model.tiles[pos].available = False
    
    def step(self):
        if self.model.tiles[self.pos].condition == "Dirty":
            self.model.tiles[self.pos].condition = "Clean"
        else:
            neighbors1 = self.model.grid.get_neighbors(self.pos, moore=True)
            # leave only available neighbors
            #neighbors = list(map(self.tile.isAvailable, neighbors))
            neighbors = []
            for i in neighbors1:
                if (isinstance(i, FloorTile) and i.available):
                    neighbors.append(i)
            # if no available neighbors, roomba doesnt move
            if (len(neighbors) == 0):
                self.nextPos = self.pos
            else:
                for neighbor in neighbors:
                    if (neighbor.condition == "Dirty"):
                        self.nextPos = neighbor.pos
                        break
                # if no dirty neighbors were found
                if self.nextPos == (-1, -1):
                    self.nextPos = neighbors[self.random.randint(0, len(neighbors)-1)].pos
            # Roomba is moved
            self.model.move_agent(self, self.nextPos)

