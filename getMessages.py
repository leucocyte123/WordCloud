# -*- coding: utf-8 -*-
import os
import sys
from datetime import datetime
import asyncio

from blivedm.blivedm import BLiveClient, DanmakuMessage
from config import all_room_ids

filename = 'log/undefined.txt'
def setFilename(name):
    global filename
    filename = 'log/danmu-%s-%s.txt' % (name, datetime.now().strftime('%Y-%m-%d-%H-%M-%S'))
def getFilename():
    global filename
    return filename

class MyBLiveClient(BLiveClient):
    async def _on_receive_danmaku(self, danmaku: DanmakuMessage):
        print(f'{danmaku.uname}：{danmaku.msg}')
        with open(getFilename(), 'a', encoding='utf-8') as f:
            f.write(danmaku.msg)
            f.write('\n')

async def main():
    if len(sys.argv) > 1:
        room_name = sys.argv[1]
    else:
        room_name = '雪狐桑'
    room_id = all_room_ids[room_name]
    setFilename(room_name)

    # 如果SSL验证失败就把ssl设为False
    client = MyBLiveClient(room_id, ssl=True)
    future = client.start()
    try:
        # 5秒后停止，测试用
        # await asyncio.sleep(5)
        # future = client.stop()
        # 或者
        # future.cancel()

        await future
    finally:
        await client.close()


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())
