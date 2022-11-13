import maya.cmds as cmds
import random
import math

BUILDING_MIN_WIDTH = 1
BUILDING_MAX_WIDTH = 4
BUILDING_MIN_DEPTH = 1
BUILDING_MAX_DEPTH = 4
BUILDING_MIN_HEIGHT = 5
BUILDING_MAX_HEIGHT = 20

CITY_BLOCK_MIN_WIDTH = 3
CITY_BLOCK_MAX_WIDTH = 5
CITY_BLOCK_MIN_DEPTH = 3
CITY_BLOCK_MAX_DEPTH = 4

def clear_all():
    """ FOR TESTING. Removes all polygons created. """
    cmds.select(all=True)
    cmds.delete()
    

def create_building_at_location(num=0, x=0, z=0):
    """
    Creates a building of random height at specified location in scene

    Parameters:
    num: building number used for naming
    x, y: location in world space to translate created building
    """
    scale = math.sqrt(x**2 + z**2) + 0.01
    height = random.randrange(BUILDING_MIN_HEIGHT, BUILDING_MAX_HEIGHT) * min((8/scale), 1)
    width = random.randrange(BUILDING_MIN_WIDTH, BUILDING_MAX_WIDTH)
    depth = random.randrange(BUILDING_MIN_DEPTH, BUILDING_MAX_DEPTH)

    name = 'building_' + str(num)
    cmds.polyCube(name=name, height=height, width=width, depth=depth)
    cmds.group(name, parent='city')
    cmds.move(x, height/2, z)
    
    
def create_city_block(start_coord=(10,10), width=3, depth=3, padding=1.2, num=0):
    """
    Create a city block using the helper function create_building_at_location()
    
    Params:
    start_coord: (x,y) coordinate that represents the top-left coord of the grid
    width: num buildings to create in the x-direction
    depth: num buildings to create in the z-direction
    padding: padding factor between each building created
    """

    # Configs
    start_x = start_coord[0]
    start_z = start_coord[1]
    
    # Generate buildings in grid pattern
    for x in range(width):
        for z in range(depth):
            create_building_at_location(num=num, x=padding*(start_x-x), z=padding*(start_z-z))
            num += 1
    return num


def create_city(street_pad=2, original_start_coord=(30, 30), width=10, depth=10):
    """
    Create the full city using the helper function create_city_block().

    Params:
    street_pad: padding between city blocks.
    """
    cmds.group(em=True, name='city') # Create parent group for all the cities
    start_coord = original_start_coord
    num = 0
    for i in range(width):
        rand_w = random.randrange(CITY_BLOCK_MIN_WIDTH, CITY_BLOCK_MAX_WIDTH)
        for j in range(depth):
            rand_r = random.randrange(CITY_BLOCK_MIN_DEPTH, CITY_BLOCK_MAX_DEPTH)
            num += create_city_block(start_coord=start_coord, width=rand_w, depth=rand_r, num=num)
            start_coord=(start_coord[0], start_coord[1] - rand_r - street_pad)
        start_coord=(start_coord[0] - rand_w - street_pad, original_start_coord[1])
           

def main():
    """ main """
    clear_all()
    create_city()
    

if __name__== "__main__":
    main()
    