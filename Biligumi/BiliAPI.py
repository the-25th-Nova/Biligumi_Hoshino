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
    

