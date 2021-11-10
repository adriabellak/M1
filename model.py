from mesa import Model
from mesa.time import RandomActivation
from mesa.space import Grid
from agent import FloorTile, Roomba

class Floor(Model):
    def __init__(self, width, height, density, roombas, max_iterations):
        super().__init__(width, height)
        self.grid = Grid(width, height, torus = False)
        self.schedule = RandomActivation(self)
        self.running = True
        self.tiles = {}
        self.max_iterations = max_iterations
        self.iterations = 0

        for (contents, x, y) in self.grid.coord_iter():
            new_floor_tile = FloorTile((x, y), self)
            if self.random.random() < density:
                new_floor_tile.condition = "Dirty"
            self.grid._place_agent((x, y), new_floor_tile)
            self.schedule.add(new_floor_tile)
            self.tiles[(x, y)] = new_floor_tile
        
        for i in range(roombas):
            new_roomba = Roomba(i, (1, 1), self)
            self.grid._place_agent((1, 1), new_roomba)
            self.schedule.add(new_roomba)
    
    def move_agent(self, agent, nextPos):
        """
        Move an agent from its current position to a new position.

        Args:
            agent: Agent object to move. Assumed to have its current location
                   stored in a 'pos' tuple.
            nextPos: Tuple of new position to move the agent to.

        """

        nextPos = self.grid.torus_adj(nextPos)
        self.tiles[agent.pos].available = True
        self.grid._remove_agent(agent.pos, agent)
        # self.grid._place_agent(nextPos, self.tiles[nextPos])
        self.grid._place_agent(nextPos, agent)
        self.grid._place_agent(agent.pos, self.tiles[agent.pos])
        agent.pos = nextPos
        agent.nextPos = (-1, -1)
        self.tiles[agent.pos].available = False

    def step(self):
        self.schedule.step()
        self.iterations += 1
        dirty_tiles = 0
        for agent in self.schedule.agents:
            if (type(agent) is FloorTile and agent.condition == "Dirty"):
                dirty_tiles += 1
        if (dirty_tiles == 0 or self.iterations == self.max_iterations):
            self.running = False