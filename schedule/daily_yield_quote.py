from qdaserver.model import DBSession
from qdaserver.model import UST,VYM,CGB
from datetime import date,datetime
from sqlalchemy import create_engine
engine=create_engine("sqlite:///devdata.db")
DBSession.configure(bind=engine)
import transaction
import time
import tgscheduler
from bs4 import BeautifulSoup
import requests
import json
def myfloat(string):
    if "N/A" in string:
        return None
    else:
        return float(string)
def update_yields_USTVYM():
    if date.today().weekday()<5:
        """quote UST yield curve"""
        url='https://www.treasury.gov/resource-center/data-chart-center/interest-rates/Pages/TextView.aspx?data=yield'
        response=requests.get(url)
        soup=BeautifulSoup(response.text,"html.parser")
        latest_curve_row=soup.find_all("table",{"class":"t-chart"})[0].find_all("td")[-12:]
        db_latest_date=DBSession.query(UST).order_by(UST.id_date.desc()).first().id_date
        if db_latest_date.strftime("%m/%d/%y")!=latest_curve_row[0].text:
            g=(td.text for td in latest_curve_row)
            ust_yield_curve=UST(id_date=datetime.strptime(next(g),"%m/%d/%y").date(),            
                                UST1M=myfloat(next(g)),UST3M=myfloat(next(g)),UST6M=myfloat(next(g)),
                                UST1Y=myfloat(next(g)),UST2Y=myfloat(next(g)),UST3Y=myfloat(next(g)),
                                UST5Y=myfloat(next(g)),UST7Y=myfloat(next(g)),UST10Y=myfloat(next(g)),
                                UST20Y=myfloat(next(g)),UST30Y=myfloat(next(g)),user_id=1)

            DBSession.add(ust_yield_curve)

            """quote VYM Div Yield"""
            url='https://www.tickertech.net/bnkinvest/stocktable.mpl?ticker=VYM&fields=0,22,5,9,7,2,3,4,10,24,25,17,18,34,19,16,20,21&side=on&head=1&n=1'
            response=requests.get(url)
            soup=BeautifulSoup(response.text,'html.parser')
            g=(td.text for td in soup.find_all("td"))
            while True:
                if 'Div Yield' in next(g):
                    VYM_yield=VYM(id_date=date.today(),
                                  dividend_yield=float(next(g).split("'")[2]))
                    DBSession.add(VYM_yield)
                    break
    transaction.commit()
    return
def update_yields_CGB():
    
    """quote CGB Yield curve(China's bonds market may be open on weekend
    after public holidays."""
    url='http://yield.chinabond.com.cn/cbweb-mn/yc/ycDetail?ycDefIds=2c9081e50a2f9606010a3068cae70001&&zblx=txy&&workTime=%s&&dxbj=0&&qxlx=0,&&yqqxN=N&&yqqxK=K&&wrjxCBFlag=0&&locale=zh_CN'%date.today()    
    while datetime.now().hour<23:
        try:
            response=requests.post(url,timeout=100)
            if 'tablelist' not in response.text:
                continue
            else:
                break
        except requests.exceptions.ConnectionError:
            time.sleep(180)
    if datetime.now().hour<23:
        soup=BeautifulSoup(response.text,'html.parser')
        table=soup.find_all("table",{"class":"tablelist"})[0]
        g=(td.text for td in table.find_all('td'))
        CN1d=CN1M=CN2M=CN3M=CN6M=CN9M=None
        CN1Y=CN2Y=CN3Y=CN5Y=CN7Y=CN10Y=CN15Y=CN20Y=CN30Y=CN50Y=None        
        while True:
            try:
                element=next(g)
                if element=='0.0y':
                    CN1d=float(next(g))
                if element=='0.08y':
                    CN1M=float(next(g))
                if element=='0.17y':
                    CN2M=float(next(g))                
                if element=='0.25y':
                    CN3M=float(next(g))
                if element=='0.5y':
                    CN6M=float(next(g))
                if element=='0.75y':
                    CN9M=float(next(g))
                if element=='1.0y':
                    CN1Y=float(next(g))
                if element=='2.0y':
                    CN2Y=float(next(g))
                if element=='3.0y':
                    CN3Y=float(next(g))
                if element=='5.0y':
                    CN5Y=float(next(g))
                if element=='7.0y':
                    CN7Y=float(next(g))
                if element=='10.0y':
                    CN10Y=float(next(g))
                if element=='15.0y':
                    CN15Y=float(next(g))
                if element=='20.0y':
                    CN20Y=float(next(g))
                if element=='30.0y':
                    CN30Y=float(next(g))
                if element=='50.0y':
                    CN50Y=float(next(g))                        
            except StopIteration:
                break
        cgb_yield_curve=CGB(id_date=date.today(),CN1d=CN1d,CN1M=CN1M,CN2M=CN2M,
                            CN3M=CN3M,CN6M=CN6M,CN9M=CN9M,CN1Y=CN1Y,CN2Y=CN2Y,
                            CN3Y=CN3Y,CN5Y=CN5Y,CN7Y=CN7Y,CN10Y=CN10Y,
                            CN15Y=CN15Y,CN20Y=CN20Y,CN30Y=CN30Y,CN50Y=CN50Y)
        DBSession.add(cgb_yield_curve)
    transaction.commit()
    return
def start_scheduler():
    """
    cron_like_string_syntax(quoted from kronos.py in tgscheduler package):
        The time and date fields are:

    =============  ==================================
        field                allowed values
    =============  ==================================
    minute         0-59
    hour           0-23
    day of month   1-31
    month          1-12 (or names, see below)
    day of week    0-7 (0 or 7 is Sun, or use names)
    =============  ==================================

    """
    tgscheduler.start_scheduler()
    tgscheduler.add_cron_like_task(update_yields_USTVYM,'30 23 * * Mon-Fri',
                                   taskname='update_yieldsinfo_daily_UST&VYM')
    tgscheduler.add_cron_like_task(update_yields_CGB,'0 14 * * *',
                                   taskname='update_yieldsinfo_daily_CGB')
start_scheduler()
while True:
    time.sleep(10)
