from mesa.visualization.UserParam import UserSettableParameter
from model import Floor, FloorTile, Roomba
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer

colors = {"Dirty" : "#999999", "Clean" : "#FFFFFF"}
width = 10
height = 10
max_iterations = 300
num_agentes = 1

def agent_portrayal(agent):
    if agent is None: return
    if type(agent) == Roomba:
        portrayal = {"Shape": "circle",
                 "Filled": "true",
                 "Layer": 1,
                 "Color": "red",
                 "r": 0.5}
    else:
        portrayal = {"Shape": "rect",
                 "Filled": "true",
                 "w" : 0.9,
                 "h" : 0.9,
                 "Layer": 0}
        (x, y) = agent.pos
        portrayal["x"] = x
        portrayal["y"] = y
        portrayal["Color"] = colors[agent.condition]
    return portrayal

model_params = {
    "width":width, 
    "height":height, 
    "density":UserSettableParameter("slider", "Dirt density", 0.5, 0.01, 1.0, 0.1),
    "roombas":num_agentes,
    "max_iterations":max_iterations
}

grid = CanvasGrid(agent_portrayal, width, height)
server = ModularServer(Floor, [grid], "Roomba", model_params)

server.port = 8521 # The default
server.launch()