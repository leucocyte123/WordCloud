# -*- coding: utf-8 -*-

import getpass

import asyncio
import mysql.connector

from blivedm.blivedm import BLiveClient, DanmakuMessage

VtuberOfInterest = {
    'xuehusang': 24393,
    'kitzuki': 22889484,
}

selected_vtuber = 'xuehusang'
room_id = VtuberOfInterest[selected_vtuber]

mysqlHost = '172.17.0.4'
mysqlUsername = 'root'
mysqlPassword = ''

def inputMysqlPassword():
    global mysqlPassword
    mysqlPassword = getpass.getpass(prompt='MySQL Password: ')

def parseMessage(message: DanmakuMessage):
    uname = message.username
    uid = message.uid
    danmu = message.msg
    return uname, uid, danmu

def writeMySQL(val):
    mydb = mysql.connector.connect(
        host=mysqlHost,
        user=mysqlUsername,
        password=mysqlPassword,
        database=selected_vtuber
    )
    mycursor = mydb.cursor()

    sql = "INSERT INTO messages (uname, uid, message) VALUES (%s, %s, %s)"

    mycursor.execute(sql, val)
    mydb.commit()

class MyBLiveClient(BLiveClient):
    async def _on_receive_danmaku(self, message: DanmakuMessage):
        val = parseMessage(message)
        writeMySQL(val)

async def main():
    client = MyBLiveClient(room_id, ssl=True)
    future = client.start()
    try:
        await future
    finally:
        await client.close()

if __name__ == '__main__':
    inputMysqlPassword()
    asyncio.get_event_loop().run_until_complete(main())
