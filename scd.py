#!/usr/bin/python2
# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

from sqlalchemy import *
import sqlalchemy.sql as sql

# <codecell>

engine  = create_engine("postgres://tlamer:tlamer@localhost")
schema = "public"
metadata = MetaData(bind=engine)

# <codecell>

dim_table = Table("dim_customers", metadata, schema=schema, autoload=True)
src_table = Table("src_customers", metadata, schema=schema, autoload=True)

# <codecell>

src_table

# <codecell>

print type(src_table.select())

# <codecell>

print list(src_table.select().execute())

# <codecell>

str(src_table.select())

# <codecell>

src_key = src_table.c["id"]
target_key = dim_table.c["id"]

print src_key
print target_key

# <markdowncell>

# Vytvorime dva selecty na vytiahnutie ID-ciek zo zdrojovej tabulky `src_customers` a z cielovej (dimenznej) tabulky `dim_customers`.

# <codecell>

src_ids = sql.select([src_key], from_obj=src_table)
target_ids = sql.select([target_key], from_obj=dim_table)
print "--- zo zdroja:\n%s" % src_ids
print "--- z dimenzie:\n%s" % target_ids

# <codecell>

diff = src_ids.except_(target_ids)
print diff

# <codecell>

result = engine.execute(diff)

# <codecell>

for row in result:
    print row

# <markdowncell>

# Toto nezbehne.

# <codecell>

#diff.join(src_table)

# <markdowncell>

# Potrebujeme podmienku na join. Najprv ziskame ID stlpec z toho diff selectu:

# <codecell>

diff = diff.alias("diff")
print diff

# <markdowncell>

# Toto je ID vsetkych novych zaznamov:

# <codecell>

diff_key = diff.c["id"]
diff_key

# <codecell>

condition = (src_key == diff_key)
# ^^ toto je ekvivalent k low level:
condition = src_key.__eq__(diff_key)

print repr(condition)
print str(condition)

# <codecell>

joined_source = diff.join(src_table, condition)

# SELECT source.* FROM ....
new_source_data = sql.select(src_table.columns, from_obj=joined_source)
print new_source_data

# <codecell>

for row in new_source_data.execute():
    print row

# <codecell>

insert = dim_table.insert()
str(insert)

# <codecell>

for row in new_source_data.execute():
    print "INSERTING %s" % (row, )
    engine.execute(insert, row)

# <codecell>

for row in dim_table.select().execute():
    print row

# <codecell>

def print_table(selectable, is_table=True):
    if is_table:
        selectable = selectable.select()

    for row in selectable.execute():
        print "\t".join([str(value) for value in row])

# <codecell>

print_table(dim_table)

# <codecell>

condition = (dim_table.c["name"] == "feri")
trash = sql.delete(dim_table, whereclause=condition)
print trash

# <codecell>

trash.execute()
print_table(dim_table)

# <codecell>

new_source_data = sql.select(src_table.columns, from_obj=joined_source)
print new_source_data

# <codecell>

timestamp = sql.functions.current_timestamp()
timestamp = timestamp.label("valid_from")
columns = src_table.columns + [timestamp]
columns

# <codecell>

new_source_data = sql.select(columns, from_obj=joined_source)
print str(new_source_data)

# <codecell>

print_table(new_source_data, is_table=False)

# <codecell>

def insert_from(table, statement):
    insert = table.insert()
    for row in statement.execute():
        engine.execute(insert, row)

# <codecell>

insert_from(dim_table, new_source_data)

# <codecell>

print_table(dim_table)

# <codecell>


