import world as wd
import utils
import render as rd
import input as inp
import pathfinder

gridWidth = 10
gridHeight = 10

world = wd.World(gridWidth, gridHeight)
render = rd.Render(world)
input = inp.Input(rd.pygame,world,render)



while True:
    #world.update()
    world.update()
    input.update()
    render.update()

