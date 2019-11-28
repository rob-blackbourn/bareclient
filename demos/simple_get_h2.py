"""Simple GET"""

import asyncio
from typing import List
from baretypes import Header

from bareclient import HttpClient


async def main(url: str, headers: List[Header]) -> None:
    async with HttpClient(url, method='GET', headers=headers) as (send, receive):
        
        request = {
            'type': 'http.request',
            'url': url,
            'method': 'GET',
            'headers': headers,
            'body': b'',
            'more_body': False
        }
        await send(request)

        message = await receive()
        print(message)

        while message.get('more_body', False):
            message = await receive(message['stream_id'])
            print(message)
        print('body read')

        message = await receive(message['stream_id'])
        print('read the disconnect')


    print('complete')

URL = 'https://docs.python.org/3/library/cgi.html'
HEADERS = [(b'host', b'docs.python.org'), (b'connection', b'close')]

asyncio.run(main(URL, HEADERS))
