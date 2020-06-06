import requests
import os
import time
from concurrent import futures
import create_tile

class Download:
    
    def __init__(self, url, flag, file_path):
        self.url = url + ('?flag=' + flag)
        self.file_path = file_path + ('\\' + flag)
        self.flag = flag
        self.threadPool = futures.ThreadPoolExecutor(max_workers=10, thread_name_prefix="test_")
        self.url_file_path = None
        self.url_path = self.file_path + '\\urls'
        
        if os.path.exists(self.url_path) and os.path.isdir(self.url_path):
            pass
        else:
            makir_file(self.url_path)
            get_url(self.url_path)
        while self.read_url(self.url_path):
            pass
        
    def read_url(self, fp):
        pathDir = os.listdir(fp)
        print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + ' -- left ' + self.flag + ' -- ' + str(len(pathDir) * 100))
        if len(pathDir) <= 0:
            print("done")
            return False
        self.url_file_path = os.path.join('%s\\%s' % (fp, pathDir[0]))
        urls_file = open(self.url_file_path, 'r')
        urls = urls_file.read()
        urls_file.close()
        url_list = urls.split("\n")
        self.handle_url(url_list)
        return True
            
    def handle_url(self, url_list):
        tasks = []
        for url in url_list:
            url_split = url.split(" ")
            if len(url_split) != 3:
                continue
            [x, y, z] = url_split
            t_url = self.url + ('&x=' + str(x) + '&y=' + str(y) + '&z=' + str(z))
            tasks.append(self.threadPool.submit(self.get_pic, z, x, y, t_url))
        futures.wait(tasks, return_when="ALL_COMPLETED")
        os.remove(self.url_file_path)
                        
    def get_pic(self, z, x, y, url):
        r = requests.get(url, verify=False, timeout=(10, 30))
        r.encoding = r.apparent_encoding
        if r.headers['Content-Type'] == 'image/png':
            self.save_pic([z, x, y, r.content])
                
    def save_pic(self, pic):
        fz = self.file_path + '\\' + str(pic[0])
        makir_file(fz)
        fx = fz + '\\' + str(pic[1])
        makir_file(fx)
        img = open(fx + '\\' + str(pic[2]) + '.png', 'wb')
        img.write(pic[3])
        img.close()

def makir_file(path):
    if os.path.exists(path) and os.path.isdir(path):
        pass
    else:
        try:
            os.makedirs(path)
        except:
            pass

def get_url(url_path):
    cou = 0
    f = open(url_path + '\\000.txt', 'a')
    tile_list = create_tile.creat_tile_list()
    for i in range(len(tile_list)):
        z, min_x, min_y, max_x, max_y = tile_list[i][0], tile_list[i][1], tile_list[i][2], tile_list[i][3], tile_list[i][4]
        for x in range(min_x, max_x + 1):
            for y in range(min_y, max_y + 1):
                f.write(str(x) + ' ' + str(y) + ' ' + str(z) + "\n")
                cou += 1
                if cou >= 100:
                    cou = 0
                    f.close()
                    f = open(url_path + '\\' + str(z) + str(y) + str(x) + '.txt', 'a')
    f.close()
