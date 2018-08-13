# -*- coding: utf-8 -*-
"""UST_yield_curve model module."""
from sqlalchemy import *
from sqlalchemy import Table, ForeignKey, Column
from sqlalchemy.types import Integer, Unicode, Date, LargeBinary,Float
from sqlalchemy.orm import relationship, backref

from qdaserver.model import DeclarativeBase, metadata, DBSession

class UST(DeclarativeBase):
    __tablename__ = 'ust_yield_curves'

    id_date = Column(Date, primary_key=True,index=True)
    UST1M = Column(Float)
    UST3M=Column(Float)
    UST6M=Column(Float)
    UST1Y=Column(Float)
    UST2Y=Column(Float)
    UST3Y=Column(Float)
    UST5Y=Column(Float)
    UST7Y=Column(Float)
    UST10Y=Column(Float)
    UST20Y=Column(Float)
    UST30Y=Column(Float)
    
    user_id = Column(Integer, ForeignKey('tg_user.user_id'), index=True)
    user = relationship('User', uselist=False,
                        backref=backref('ust_yield_curves',
                                        cascade='all, delete-orphan'))
class VYM(DeclarativeBase):
    __tablename__ = 'VYM_yields'

    id_date = Column(Date, ForeignKey('ust_yield_curves.id_date'),primary_key=True,index=True)
    dividend_yield=Column(Float,nullable=False)
    UST=relationship('UST',uselist=False,
                     backref=backref('VYM_yields'))


class CGB(DeclarativeBase):
    __tablename__ = 'cgb_yield_curves'

    id_date = Column(Date, ForeignKey('ust_yield_curves.id_date'),primary_key=True,index=True)
    CN1d=Column(Float)
    CN1M = Column(Float)
    CN2M=Column(Float)
    CN3M=Column(Float)
    CN6M=Column(Float)
    CN9M=Column(Float)
    CN1Y=Column(Float)
    CN2Y=Column(Float)
    CN3Y=Column(Float)
    CN5Y=Column(Float)
    CN7Y=Column(Float)
    CN10Y=Column(Float)
    CN15Y=Column(Float)
    CN20Y=Column(Float)
    CN30Y=Column(Float)
    CN50Y=Column(Float)
    UST=relationship('UST',uselist=False,backref=backref('cgb_yield_curves'))

__all__ = ['UST','VYM','CGB']
