from tg import expose,flash
from tg.i18n import ugettext as _, lazy_ugettext as l_
from qdaserver.model import UST,VYM,CGB
from qdaserver.model import DBSession
from qdaserver.lib.base import BaseController
from datetime import date,datetime
class USvsCN_Controller(BaseController):
    """show interactive datas of U.S. and China's economy and finance
    """
    @expose('qdaserver.templates.us_vs_cn')
    def index(self):
        return dict(page='U.S. vs. China')
    
    @expose('json')
    def data(self,**kw):
        """
        form a json of UST10Y and CGB10Y yields in period of the given
        'from'-'to' date
        """
        datalist=[]
        from_date=max(datetime.strptime(kw.get("from"),"%Y-%m-%d").date(),date(2010,7,1))
        to_date=datetime.strptime(kw.get("to"),"%Y-%m-%d").date()
        for cgb_yield_element in DBSession.query(CGB).filter(CGB.id_date>=from_date,CGB.id_date<=to_date):
            try:
                if cgb_yield_element.UST.UST10Y is not None:
                    tmp_dict={}
                    tmp_dict['date']=cgb_yield_element.id_date
                    tmp_dict['CN10Y']=cgb_yield_element.CN10Y
                    tmp_dict['US10Y']=cgb_yield_element.UST.UST10Y
                    datalist.append(tmp_dict)
            except AttributeError:
                pass
        return dict(data=datalist)
        
