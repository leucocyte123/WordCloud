# -*- coding: utf-8 -*-
import os
from datetime import date
import asyncio

from blivedm.blivedm import BLiveClient, DanmakuMessage

filename = None
def getFilename():
    global filename
    if filename is None:
        filename = 'log/danmu-%s.txt' % date.today().strftime('%Y-%m-%d')
    return filename

class MyBLiveClient(BLiveClient):
    async def _on_receive_danmaku(self, danmaku: DanmakuMessage):
        print(f'{danmaku.uname}：{danmaku.msg}')
        with open(getFilename(), 'a', encoding='utf-8') as f:
            f.write(danmaku.msg)
            f.write('\n')

async def main():
    # 参数1是直播间ID
    # 如果SSL验证失败就把ssl设为False
    room_id = 21711976
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
