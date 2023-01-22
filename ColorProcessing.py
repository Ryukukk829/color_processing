#
#

import numpy as np 
import cv2
from io import BytesIO
from matplotlib import pyplot as plt
import requests
from bs4 import BeautifulSoup



class ColorProcessing(object):
    def __init__(self, img_path, threshold = 100):
        self.attrs = ["b", "g", "r",
                      "h", "s", "v", "a"]
        self.img = self.set_image(img_path)
        self.h, self.w, self.c = self.img.shape
        self.threshold = threshold
    #アルファの値を反転させてマスクとして使う
    def flip(self, arr):
        r = arr - 127.5
        r *= -1
        return (r + 127.5).astype(int)
    
    ## 画像は、リンクまたはパスで指定
    ## urlから取得する場合、取得した画像はローカルにも保存する。
    def set_image(self, img_path, target_file = "./imgs/target.png"):
        ## リンクで取得
        try:
            img_path = set_from_link(img_path, target_file)
        except:
            pass
        ## パスで取得
        try:
            #aの値を含めて読み込む
            img = cv2.imread(img_path, -1)
        except:
            pass
        #todo: α値があるかで例外処理(warning) 
        return img
        
    def set_from_link(self, url, target_file):
        r = requests.get(url)
        if r.status_code == 200:
            with BytesIO(r.content) as buf:
                img = Image.open(buf) # PIL.Imageで読込む
                target_file = f"{filename}.{img.format.lower()}" 
                img.save(target_file)
        return img_path

    #画像そのまま
    def get_mask(self, th = False):
        if th:
            pass
        else:
            th = self.threshold
        # マスク部分が黒のシルエット(背景は白), グレースケールになるようなndary
        # アルファ値が0で透明
        mask = self.img[:,:,-1]
        #mask = self.flip(mask)
        ## todo: 閾値で処理したい
        return mask > th
        

    #ピクセルの値の集合を一次元で返す
    def get_values(self, attr, mask = True):
        #rgbhsv値の集合を出力(マスク有無指定)
        if attr not in self.attrs:
            print("{} is unexpected input".format(attr))
            print("please input following attributes: ", self.attrs)
            return 0
        elif attr in self.attrs[:3]:
            img = self.img[:, :, self.attrs.index(attr)]
        elif attr in self.attrs[3:6]:
            img = cv2.cvtColor(self.img, cv2.COLOR_BGR2HSV)
            img = img[:, :, self.attrs.index(attr) - 3]
        elif attr == self.attrs[-1]:
            img = self.img[:, :, 3]
        else:
            print("{} is unexpected input".format(attr))
            print("please input following attributes: ", self.attrs)
            return 0
        if mask:
            values = img[self.get_mask()]
        else:
            values = img.reshape(-1)
        return values
    
    def isolation(self, hsv = False, mask = True):
        if hsv:
            img = cv2.cvtColor(self.img, cv2.COLOR_BGR2HSV)
        else:
            img = self.img[:,:,:3]
        zeros = np.zeros((self.h, self.w), img.dtype)
        b, g, r = cv2.split(img)
        if mask:
            img_b = cv2.merge((b * self.get_mask(), zeros, zeros))
            img_g = cv2.merge((zeros, g * self.get_mask(), zeros))
            img_r = cv2.merge((zeros, zeros, r * self.get_mask()))
        else:
            img_b = cv2.merge((b, zeros, zeros))
            img_g = cv2.merge((zeros, g, zeros))
            img_r = cv2.merge((zeros, zeros, r))
            
        return img_b, img_g, img_r

def save_img(img):
    cv2.imwrite("tmp.png", img)
    return
 
def main():
    img_path = "Reuniclus.png"
    cp = ColorProcessing(img_path)
    
if __name__ == "__main__":
    main()
