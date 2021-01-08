import requests
import random
import math
import os

from io import BytesIO
import base64

from PIL import (
Image,
ImageDraw,
ImageFont,
ImageOps
)

from .config import s_pic_size, theme_colors, fontt

fontt = os.path.abspath(os.path.join(os.path.dirname(__file__),'font',fontt))
if not os.path.isfile(fontt):
    print('「Biligumi」Font doesnt exist!')
class BangumiImage(object):
    '''
    title: 标题
    '''
    def __init__(self,title:str,theme=False):
        self.theme = self.gen_theme(theme)
        #print(self.theme)
        self.img = self.create_background(text=title)
        self.cover_width = 0
        try:
            self.font = ImageFont.truetype(fontt)
        except Exception as e:
            print(e)
            
        
    def gen_theme(self,theme) -> dict:
        # Choose theme
        if not theme:
            return random.choice(theme_colors)
        else:
            for i in theme_colors:
                if i.get('name') == theme:
                    return i
            return random.choice(theme_colors)

    def create_background(self,loc=s_pic_size,text:str='') -> Image:
        if not text:
            return Image.new('RGBA',loc,self.theme.get('main'))
        im = Image.new('RGBA',(loc[0],math.floor(loc[1] * 0.5)),self.theme.get('title'))
        im = self.write_title(im,text)
        
        return im
        
        
    def draw_from_url(self,img:Image,url,loc=False) -> Image:
        '''
        loc: 二元元组
        '''
        with requests.get(url) as f:
            im =Image.open(BytesIO(f.content))
            # Usually 4:3 
            p = im.width / im.height
            img = self.draw_center(img,im,p,loc)
            return img

    def draw_center(self, bg:Image, im:Image, proportion=1,loc=False) -> Image:
        '''
        Proportion: 宽 / 高
        '''
        # 如果有 loc 则使用 否则使用 5% 上下边距
        if not loc:
            f = math.floor(bg.height * 0.05)
            loc = (f,f)
        h = math.floor(bg.height - (2 * loc[0]))
        w = math.floor(h * proportion)
        im = im.resize((w,h))
        bg.paste(im,loc)
        
        # set img width for later use
        self.cover_width = math.floor(w + (2 *  loc[0]))
        self.cover_height = f
        return bg
        
    def write_title(self,im,text,w=0,h=0,offset_x=0,offset_y=0) -> Image:
        '''
        
        '''
        if not w:
            w = im.width
        if not h:
            h = im.height
        for i in range(1,s_pic_size[0]):
            imFont = ImageFont.truetype(font=fontt,size=i)
            text_size = imFont.getsize(text)
            if text_size[0] > w or text_size[1] > h:
                imFont = ImageFont.truetype(font=fontt,size=i-1)
                text_size = imFont.getsize(text)
                break
            
        
        draw = ImageDraw.Draw(im)
        
        draw.text((offset_x + math.floor((w - text_size[0])/2),offset_y + math.floor((h - text_size[1]*5/4)/2)),text,font=imFont)
        return im
        
    def to_all_decoration(self,im,texts:list) -> Image:
        times = 0
        for i in texts:
            im = self.write_title(im,i,w=im.width - self.cover_width,h=im.height/5,offset_x=self.cover_width,offset_y=self.cover_height + 
im.height/5*times)
            times += 1
        return im
        
    def pic2b64(self) -> str:
        buf = BytesIO()
        self.img.save(buf,format='png')
        base64_str = base64.b64encode(buf.getvalue()).decode()
        return 'base64://' + base64_str
        
    def gen_image(self,ep:dict,is_update:False):
        ''' generate self.img into pretty img with text & cover
                 ep: eposide dict from api'''
        
        for i in ep:
            # 救救我，我也看不懂了
            
            im_t = self.draw_from_url(self.create_background(),i.get('cover'))
            if is_update:
                im_t = self.to_all_decoration(im_t,['{}'.format(i.get('title'))])
            else:
                im_t = self.to_all_decoration(im_t,['{} - {}'.format(i.get('title'),i.get('pub_index')),i.get('pub_time')])
            self.img = ImageOps.expand(self.img,(0,0,0,im_t.height),fill=self.theme.get('main'))
            self.img.paste(im_t,(0, self.img.height - im_t.height))
            
        
            
            
