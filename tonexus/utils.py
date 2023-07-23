# -*- coding=utf-8 -*-


def print_raw_sql(query):
    print(query.statement.compile(compile_kwargs={"literal_binds": True}))
