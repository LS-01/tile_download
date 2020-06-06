import os
import create_tile

def check_maps(url, flag, file_path):
    cou = 0
    url = url + ('?flag=' + flag)
    file_path = file_path + ('\\' + flag)
    
    url_path = file_path + '\\urls'
    f = open(url_path + '\\000.txt', 'a')
    tile_list = create_tile.creat_tile_list()
    for i in range(len(tile_list)):
        z, min_x, min_y, max_x, max_y = tile_list[i][0], tile_list[i][1], tile_list[i][2], tile_list[i][3], tile_list[i][4]
        for x in range(min_x, max_x + 1):
            for y in range(min_y, max_y + 1):
                t_url = url + ('&x=' + str(x) + '&y=' + str(y) + '&z=' + str(z))
                fp = file_path + '\\' + str(z) + '\\' + str(x) + '\\' + str(y) + '.png'
                if os.path.exists(fp) is False or os.path.getsize(fp) <= 0:
                    f.write(str(x) + ' ' + str(y) + ' ' + str(z) + "\n")
                    cou += 1
                    if cou >= 100:
                        cou = 0
                        f.close()
                        f = open(url_path + '\\' + str(z) + str(y) + str(x) + '.txt', 'a')
                    print(t_url)
    f.close()
