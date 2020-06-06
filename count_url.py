import create_tile

def count_url():
    cou = 0
    tile_list = create_tile.creat_tile_list()
    for i in range(len(tile_list)):
        min_x, min_y, max_x, max_y = tile_list[i][1], tile_list[i][2], tile_list[i][3], tile_list[i][4]
        for x in range(min_x, max_x + 1):
            for y in range(min_y, max_y + 1):
                cou += 1
    print(cou)

count_url()
