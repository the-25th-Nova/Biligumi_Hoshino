import re

from .BiliAPI import Bangumi
from .ImageGenerator import BangumiImage
from hoshino import Service, MessageSegment
import hoshino

sv = Service('biligumi_update',enable_on_default=False,bundle='biligumi')

sv2 = Service('biligumi_daily',enable_on_default=False,bundle='biligumi')

bot = hoshino.get_bot()
cache = None

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
        res = Bangumi(day=week_c.index(el))
        r = BangumiImage('{}「星期{}」新番时间表'.format(res.ep.get('date'),week_c[res.ep.get('day_of_week')]))
        r.gen_image(res.ep.get('seasons'))
        
        await bot.send(ctx,MessageSegment(type_='reply',data={'id':m_id}) + MessageSegment.image(file=r.pic2b64()))
        
        
@sv2.scheduled_job('cron',hour='0',minute='1')
async def daily_report():
    res = Bangumi()
    r = BangumiImage('{}「星期{}」新番时间表'.format(res.ep.get('date'),week_c[res.ep.get('day_of_week')]))
    r.gen_image(res.ep.get('seasons'))
    await sv2.broadcast('又是美好的一天(*•̀ᴗ•́*)و\n' + MessageSegment.image(file=r.pic2b64()),'biligumi_broadcast',0)
    
@sv.scheduled_job('cron',minute='*/1')
async def update_report():
    sv.logger.info('Checking Update')
    global cache
    if not cache:
        ri = Bangumi()
        cache = ri.ep
        return
    res = Bangumi()
    updates = res.update_check(cache)
    cache = res.ep
    #sv.logger.info(updates)
    if not updates:
        return
    r = BangumiImage('Lately Update')
    r.gen_image(updates,is_update=True)
    '''
    link = '\n'.join('{} - {}'.format(i.get('title'),i.get('link')) for i in updates)
    await sv.broadcast(MessageSegment.image(file=r.pic2b64()) + link,'biligumi_broadcast',0)
    '''
    await sv.broadcast(MessageSegment.image(file=r.pic2b64()),'biligumi_broadcast',0)
    for im in updates:
        await sv.broadcast('{} - {}'.format(im.get('title'),im.get('link')),'biligumi_broadcast')