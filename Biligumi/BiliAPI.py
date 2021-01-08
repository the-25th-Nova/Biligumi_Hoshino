import json
import requests


bangumi_url = 'https://bangumi.bilibili.com/web_api/timeline_global'

class Bangumi(object):
    def __init__(self,day=0):
        self.all_day = self.get_all_bangumi()
        if not self.all_day:
            self.ep = dict()
        # 优先级： day > today
        if day and (day > 0 and day <=7 and isinstance(day,int)):
            for i in self.all_day[::-1]:
                if i.get('day_of_week') == day:
                    self.ep = i
                    break
        else:
            for i in self.all_day:
                if i.get('is_today'):
                    self.ep = i
                    break
    
    @classmethod
    def get_all_bangumi(self):
        with requests.get(bangumi_url) as r:
            try:
                raw = r.json()
                if raw.get('message') == 'success':
                    return raw.get('result')
                return False
            except Exception as e:
                print(e)
                return False
    
    def update_check(self,now:dict):
        if len(now) != len(self.ep):
            print('Updating raw')
            return []
        content = []
        for i in range(len(self.ep.get('seasons'))):
            if self.ep.get('seasons')[i].get('is_published') != now.get('seasons')[i].get('is_published'):
                #print(self.ep.get('seasons')[i])
                content.append(self.get_detail(epid=self.ep.get('seasons')[i].get('ep_id'),ssid=self.ep.get('seasons')[i].get('season_id'),ts=self.ep.get('seasons')[i].get('pub_ts')))
        return content
        
    def get_detail(self,ssid='',epid='',ts=0):
        if epid:
            res = requests.get('http://api.bilibili.com/pgc/view/web/season?ep_id={}'.format(epid))
        elif ssid:
            res = requests.get('http://api.bilibili.com/pgc/view/web/season?season_id={}'.format(ssid))
        else: return None
        try:
            for i in res.json().get('result').get('episodes'):
                
                if i.get('pub_time') >= ts - 1000 and i.get('pub_time') <= ts + 1000: # 误差
                    return {'title':i.get('share_copy'),'cover':i.get('cover'),'link':i.get('short_link')}
        except Exception as e:
            print(e)
            return None
        

