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


def create_ground(start_coord, end_coord):
    print(start_coord)
    print(end_coord)
    width = abs(end_coord[0] - start_coord[0])
    height = abs(end_coord[1] - start_coord[1])
    cmds.polyPlane(width=width, height=height)

def create_building_at_location(num=0, x=0, z=0):
    """
    Creates a building of random height at specified location in scene. 
    TODO: Currently just a single cube, but want to make a building be 1-3 cubes

    Parameters:
    num: building number used for naming
    x, y: location in world space to translate created building
    """
    scale = math.sqrt(x**2 + z**2) + 0.01
    scale = min((5/scale), 1)
    height = random.randrange(BUILDING_MIN_HEIGHT, BUILDING_MAX_HEIGHT) * scale
    width = random.randrange(BUILDING_MIN_WIDTH, BUILDING_MAX_WIDTH)
    depth = random.randrange(BUILDING_MIN_DEPTH, BUILDING_MAX_DEPTH)

    name = 'building_' + str(num)
    cmds.polyCube(name=name, height=height, width=width, depth=depth)
    cmds.group(name, parent='city')
    cmds.move(x, height/2, z)
    
    
def create_city_block(start_coord=(10,10), width=3, depth=3, padding=1.2, num=0) -> int:
    """
    Create a city block using the helper function create_building_at_location()
    TODO: Space out the buildings better. Might need to redo algorithm
    
    Params:
    start_coord: (x,y) coordinate that represents the top-left coord of the grid
    width: num buildings to create in the x-direction
    depth: num buildings to create in the z-direction
    padding: padding factor between each building created
    """
    start_x = start_coord[0]
    start_z = start_coord[1]

    # scale = math.sqrt(start_x**2 + start_z**2) + 0.01
    # scale = min((20/scale), 1)
    # width = int(width * scale)
    # depth = int(depth * scale)
    
    # Generate buildings in grid pattern
    for x in range(width):
        for z in range(depth):
            create_building_at_location(num=num, x=padding*(start_x-x), z=padding*(start_z-z))
            num += 1
    return num


def create_city(street_pad=2, original_start_coord=(30, 30), width=10, depth=10):
    """
    Create the full city using the helper functions create_city_block() and
    create_ground().

    Params:
    street_pad: padding between city blocks.
    """
    cmds.group(em=True, name='city') # Create parent group for all the cities
    curr_coord = original_start_coord
    num = 1
    min_depth = 1
    for _ in range(width):
        rand_w = random.randrange(CITY_BLOCK_MIN_WIDTH, CITY_BLOCK_MAX_WIDTH)
        for _ in range(depth):
            rand_r = random.randrange(CITY_BLOCK_MIN_DEPTH, CITY_BLOCK_MAX_DEPTH)
            num = create_city_block(start_coord=curr_coord, width=rand_w, depth=rand_r, num=num) + 1
            curr_coord = (curr_coord[0], curr_coord[1] - rand_r - street_pad)
            min_depth = min(min_depth, curr_coord[1])
        curr_coord=(curr_coord[0] - rand_w - street_pad, original_start_coord[1])
    create_ground(start_coord=original_start_coord, end_coord=(curr_coord[0], min_depth))
           

def main():
    """ main """
    clear_all()
    create_city()
    

if __name__== "__main__":
    main()
    