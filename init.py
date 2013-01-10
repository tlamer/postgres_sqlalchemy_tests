#!/usr/bin/python2
from sqlalchemy import *

meta = MetaData()

src_customers = Table('src_customers', meta,
    Column('id', Integer, primary_key = True),
    Column('name', String(256)),
    Column('address', String(256))
)


dim_customers = Table('dim_customers', meta,
    Column('id', Integer, primary_key = True),
    Column('name', String(256)),
    Column('address', String(256)),
    Column('surrogate', Integer, Sequence('dim_customers_surrogate_seq')),
    Column('valid_from', DateTime),
    Column('valid_to', DateTime)
)

eng = create_engine('postgresql://tlamer:tlamer@localhost')
conn = eng.connect()

eng.execute("DROP TABLE IF EXISTS dim_customers")
eng.execute("DROP TABLE IF EXISTS src_customers")
eng.execute("DROP TABLE IF EXISTS tmp")

meta.create_all(eng)
conn.execute(src_customers.insert(), [
    {'id':1, 'name':'peter', 'address':'kapicova'},
    {'id':2, 'name':'danko', 'address':'vavilovova'},
    {'id':3, 'name':'stivi', 'address':'foobar'},
])

