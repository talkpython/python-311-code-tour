import asyncio
from asyncio import TaskGroup
from pprint import pprint
from typing import List, Optional

import httpx
import pydantic
from pydantic import BaseModel


class SearchItem(BaseModel):
    category: str
    id: Optional[int]
    item_id: Optional[int]
    url: str
    title: str
    description: str


class SearchResponse(BaseModel):
    elapsed_ms: float
    keywords: List[str]
    results: List[SearchItem] = pydantic.Field(default_factory=list)
    episodes: List[SearchItem] = pydantic.Field(default_factory=list)


def cleanup(resp: SearchResponse):
    # Unfortunately, Talk Python's and Python Bytes' APIs vary slightly.
    # This method will unify them.
    resp.episodes = resp.episodes or resp.results
    resp.results = resp.episodes or resp.results

    for r in resp.results:
        r.id = r.id or r.item_id


async def search_podcast(text: str, server: str) -> list[str]:
    search_url = f'https://{server}/api/search?q={text}'
    async with httpx.AsyncClient() as client:
        resp = await client.get(search_url)
        resp.raise_for_status()

    data = resp.json()
    resp = SearchResponse(**data)
    cleanup(resp)

    return [f'{r.id}: {r.title}' for r in resp.results if r.category.lower() == 'episode']


async def search():
    # pydantic beanie mongodb odm <-- is a good search string
    text = input("What keyword to you want to look for? ").strip().lower()

    async with TaskGroup() as tg:
        tp = tg.create_task(search_podcast(text, 'search.talkpython.fm'))
        pb = tg.create_task(search_podcast(text, 'search.pythonbytes.fm'))

    # results = await asyncio.gather(tp, pb)
    # pprint(results)

    print("Done with search.")
    print()
    print("Results from Talk Python:")
    for title in tp.result():
        print(f'* {title}')
    print()
    print("Results from Python Bytes:")
    for title in pb.result():
        print(f'* {title}')


if __name__ == '__main__':
    asyncio.run(search())
