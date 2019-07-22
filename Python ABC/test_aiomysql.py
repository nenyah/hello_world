#!/usr/bin/env python3.5
# -*- coding:utf-8 -*-
"""
Function:
携程操作mysql Demo
Version:    2016-08-29
Author:     Steven
Contact:    lucibriel (at) 163.com
"""
import asyncio
import aiomysql

loop = asyncio.get_event_loop()


async def test_example():
    conn = await aiomysql.connect(host='localhost',
                                  port=3306,
                                  user='root',
                                  password='mysql',
                                  db='awesome',
                                  loop=loop)

    cur = await conn.cursor()
    await cur.execute("SELECT * FROM blogs")
    print(cur.description)
    r = await cur.fetchall()
    print(r)
    await cur.close()
    conn.close()


loop.run_until_complete(test_example())
