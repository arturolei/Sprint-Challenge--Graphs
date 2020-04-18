from room import Room
from player import Player
from world import World

import random
from ast import literal_eval

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []


def dft_recur_modified(current_room):
	# Let's create a set of visited rooms!
    visited = set()

    # Let's set up a path. 
    path = []

    def dft_recur(current_room, previous_direction=None): # Previous_direction will be set up later for backtrackingpurposes

		# When you visit a room add it to the visited list
        visited.add(current_room.id)

        for exit in current_room.get_exits():

			# For every exit in the current room, get the next room in each direction
            next_room=current_room.get_room_in_direction(exit)

            if next_room.id in visited: #if we've been there already...
                continue # Ignore and move on
            else: 
                visited.add(next_room.id) # Add the next room id to the list of visited rooms
                path.append(exit) # Attach the exit path/room to the path (so we back track)
			
            #Run again until all rooms have been visited and all exits appended to path
            dft_recur(next_room, previous_direction=exit)
        
        if previous_direction is not None: #If we've passed in an exit from the recursion process above.
            back = {"n": "s", "e": "w", "s": "n", "w": "e"} 
            previous = back[previous_direction] #  Get the opposite of the exit direction

            path.append(previous) # Append it to the path to be explored
    dft_recur(current_room)

    return path

traversal_path= dft_recur_modified(world.starting_room)



# TRAVERSAL TEST
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")



#######
# UNCOMMENT TO WALK AROUND
#######
player.current_room.print_room_description(player)
while True:
    cmds = input("-> ").lower().split(" ")
    if cmds[0] in ["n", "s", "e", "w"]:
        player.travel(cmds[0], True)
    elif cmds[0] == "q":
        break
    else:
        print("I did not understand that command.")
