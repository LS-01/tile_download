import os
import sqlite3
import threading

def save_pic(c, zoom, column, row, img):
    c.execute("INSERT INTO tiles (zoom_level,tile_column,tile_row,tile_data) VALUES(?,?,?,?)", (zoom, column, row, img))

def save_to_sqlite(filepath):
    sqlite_file = open("map.mbtiles", "w+")
    sqlite_file.close()
    
    database = sqlite3.connect('map.mbtiles')
    c = database.cursor()
    c.execute('''CREATE TABLE tiles(zoom_level integer, tile_column integer, tile_row integer, tile_data blob)''')
    c.execute('''CREATE UNIQUE INDEX tile_index on tiles (zoom_level, tile_column, tile_row)''')
    
    i = 0
    paths = [filepath]
    while paths:
        fp = paths.pop()
        pathDir = os.listdir(fp)
        for allDir in pathDir:
            child = os.path.join('%s\\%s' % (fp, allDir))
            if os.path.isdir(child):
                paths.append(child)
            else:
                file_type = child.split('.')[-1]
                if file_type == 'jpg' or file_type == 'png':
                    file_detail = child.split('\\')
                    zoom = file_detail[-3]
                    row = file_detail[-2]
                    column = file_detail[-1].split('.')[0]
    
                    img_file = open(child, 'rb')
                    img = img_file.read()
                    img_file.close()
                    i += 1
                    #t = threading.Thread(target=save_pic(c, zoom, column, row, img), name='LoopThread')
                    #t.start()
                    c.execute("INSERT INTO tiles (zoom_level,tile_column,tile_row,tile_data) VALUES(?,?,?,?)", (zoom, column, row, img))
                    if i >= 20000:
                        i = 0
                        database.commit()
    database.commit()
    c.close()
    database.close()

save_to_sqlite("F:\\task\\test\\map")