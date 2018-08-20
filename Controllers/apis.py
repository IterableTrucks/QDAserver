
from tgext.crud import EasyCrudRestController
from sprox.fillerbase import TableFiller
from tg import expose,flash,abort
from tg import request
from tg.i18n import ugettext as _, lazy_ugettext as l_
from qdaserver.model import UST,VYM,CGB
from qdaserver.model import DBSession
from qdaserver.lib.base import BaseController
from sqlalchemy.orm import load_only
from datetime import date,datetime 
from tg.predicates import not_anonymous
class table_filler_for_dates(TableFiller):
    def __init__(self,session,model,*args):
        super().__init__(session)
        self.__entity__=model
        self.fields_args=(model.id_date.label('date'),)+tuple((getattr(model,field) for field in args))
    def _do_get_provider_count_and_objs(self,**kw):
        from_date=datetime.strptime(kw.get('from'),'%Y-%m-%d').date()
        to_date=datetime.strptime(kw.get('to'),'%Y-%m-%d').date()       
        results=DBSession.query(*self.fields_args).filter(self.__entity__.id_date>=from_date,self.__entity__.id_date<=to_date).all()
        return len(results),[r._asdict() for r in results]

class Yield_for_dates_Controller(EasyCrudRestController):
    def __init__(self,session):
        super().__init__(session)
        self.table_filler=table_filler_for_dates(DBSession,self.model,*self.fields_args)
    def _before(self,*args,**kw):
        if request.response_type!='application/json':
            abort(406,'Only JSON requests are supported')
        super()._before(*args,**kw)
    def get_one(self,*args,**kw):
        pass
    def edit(self,*args,**kw):
        pass
    def new(self, *args, **kw):
        pass
    def post(self, *args, **kw):
        pass
    def put(self, *args, **kw):
        pass
    def post_delete(self, *args, **kw):
        pass
    def get_delete(self, *args, **kw):
        pass

class USTController(Yield_for_dates_Controller):

    title="UST yield curves"
    pagination=False
    model=UST
    fields_args=('UST1M','UST3M','UST6M','UST1Y','UST2Y','UST3Y','UST5Y','UST7Y','UST10Y','UST20Y','UST30Y')
class VYMController(Yield_for_dates_Controller):

    title="VYM div yield"
    pagination=False
    model=VYM
    fields_args=('dividend_yield',)
class CGBController(Yield_for_dates_Controller):

    allow_only=not_anonymous(msg=l_('Only logged users can use this API'))
    title="CGB yield curve"
    pagination=False
    model=CGB
    fields_args=('CN1d','CN1M','CN2M','CN3M','CN6M','CN9M','CN1Y','CN2Y','CN3Y','CN5Y','CN7Y','CN10Y','CN15Y','CN20Y','CN30Y','CN50Y')

class APIController(BaseController):
    """APIs entrance
    """
    @expose('qdaserver.templates.apis')
    def index(self):
        return dict(page='APIs',models=["ust","vym","cgb"])
    ust=USTController(DBSession)
    vym=VYMController(DBSession)
    cgb=CGBController(DBSession)
    

