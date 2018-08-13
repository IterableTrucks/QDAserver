from tg import expose,flash
from tg.i18n import ugettext as _, lazy_ugettext as l_
from qdaserver.model import UST,VYM,CGB
from qdaserver.model import DBSession
from qdaserver.lib.base import BaseController
from datetime import date,datetime
class VYMController(BaseController):
    """show the vym_dividend_yield in the gauge of US treatury yield
        of different durations
    """
        
    @expose('qdaserver.templates.vym')
    def index(self):
        return dict(page='VYM Yield Chart')
    @expose('json')
    def data(self,**kw):
        """
        form a json of dividend yield in period of the given 'from'-'to' date
        """
        datalist=[]
        from_date=max(datetime.strptime(kw.get("from"),"%Y-%m-%d").date(),date(2018,1,30))
        latest_date=DBSession.query(VYM).order_by(VYM.id_date.desc()).first().id_date
        to_date=min(datetime.strptime(kw.get("to"),"%Y-%m-%d").date(),latest_date)
        for vym_yield_element in DBSession.query(VYM).filter(VYM.id_date>=from_date,VYM.id_date<=to_date):
            tmp_dict={}
            tmp_dict['date']=vym_yield_element.id_date
            tmp_dict['dividend_yield']=vym_yield_element.dividend_yield
            ust_yield_curve=vym_yield_element.UST            
        
            tmp_dict['UST1M']=ust_yield_curve.UST1M
            tmp_dict['UST3M']=ust_yield_curve.UST3M
            tmp_dict['UST6M']=ust_yield_curve.UST6M
            tmp_dict['UST1Y']=ust_yield_curve.UST1Y
            tmp_dict['UST2Y']=ust_yield_curve.UST2Y
            tmp_dict['UST3Y']=ust_yield_curve.UST3Y
            tmp_dict['UST5Y']=ust_yield_curve.UST5Y
            tmp_dict['UST7Y']=ust_yield_curve.UST7Y
            tmp_dict['UST10Y']=ust_yield_curve.UST10Y
            tmp_dict['UST20Y']=ust_yield_curve.UST20Y
            tmp_dict['UST30Y']=ust_yield_curve.UST30Y

            datalist.append(tmp_dict)
        return dict(data=datalist)
