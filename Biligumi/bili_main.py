import re

from .Biligumi.BiliAPI import Bangumi
from .Biligumi.ImageGenerator import BangumiImage
from hoshino import Service, MessageSegment
import hoshino

sv2 = Service('biligumi_daily',enable_on_default=True,bundle='biligumi')

bot = hoshino.get_bot()

week_c = ['','一','二','三','四','五','六','日']

@bot.on_message()
async def main(ctx):
    msg = ctx['raw_message']
    m_id = str(ctx['message_id'])
    if msg == '今日新番':
        res = Bangumi()
        r = BangumiImage('{}「星期{}」新番时间表'.format(res.ep.get('date'),week_c[res.ep.get('day_of_week')]))
        r.gen_image(res.ep.get('seasons'))
        
        await bot.send(ctx,MessageSegment(type_='reply',data={'id':m_id}) + MessageSegment.image(file=r.pic2b64()))
    elif ｋ := re.match('(星期([一二三四五六日天])|周([一二三四五六日]))+?新番',msg):
        if k.group(2):
            if k.group(2) == '天':
                el = '日'
            else:
                el = k.group(2)
        elif k.group(3):
            el = k.group(3)
        res = Bangumi(day=el)
        r = BangumiImage('{}「星期{}」新番时间表'.format(res.ep.get('date'),week_c[res.ep.get('day_of_week')]))
        r.gen_image(res.ep.get('seasons'))
        
        await bot.send(ctx,MessageSegment(type_='reply',data={'id':m_id}) + MessageSegment.image(file=r.pic2b64()))