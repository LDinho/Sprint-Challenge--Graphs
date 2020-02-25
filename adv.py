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
room_graph = literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []


backward_navigation = {'n': 's', 'e': 'w', 's': 'n', 'w': 'e'}
tracked_room = {}
visited = {}
prevRoom = []  # back to previous room

def check_navigation(roomid):
    directions = []
    # check directions
    if 'n' in room_graph[roomid][1].keys():
        directions.append('n')
    if 'e' in room_graph[roomid][1].keys():
        directions.append('e')
    if 's' in room_graph[roomid][1].keys():
        directions.append('s')
    if 'w' in room_graph[roomid][1].keys():
        directions.append('w')
    return directions


while len(visited) < len(room_graph):
    room_id = player.current_room.id
    if room_id not in tracked_room:
        visited[room_id] = room_id  # track visited
        tracked_room[room_id] = check_navigation(room_id)  # add directions

    if len(tracked_room[room_id]) < 1:  # check if more directions exist.
        prev_nav = prevRoom.pop()
        traversal_path.append(prev_nav)
        player.travel(prev_nav)  # move player

    else:
        next_direction = tracked_room[room_id].pop(0)
        traversal_path.append(next_direction)
        prevRoom.append(backward_navigation[next_direction])  # track opposite direction
        player.travel(next_direction)


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
