from requests import get
import os
from tldextract import extract
from aiomultiprocess import Pool
import asyncio
import aiohttp
import time

os.environ['NO_PROXY'] = '127.0.0.1'

async def fetch(url):
	#return content in url
	fn = 'screenshots/' +extract(url).domain + '.png'
	url = 'http://18.219.180.248:8080/?url={}'.format(url)
	try:
		async with aiohttp.ClientSession() as client:
			async with client.get(url, timeout = 20) as resp:
				with open(fn, 'wb') as f:
					try:
						c = await resp.content.read()
						f.write(c)
						print(url)
					except:
						print('err on {}'.format(url))
						pass
	except:
		print('error')
		pass

def chunks(lst, n):
    """Chop the list up"""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

async def main():
	urls = open('urls.txt', 'r').read()
	urls = urls.split('\n')
	
	batch_size = 10
	async with Pool(processes = 5) as pool:
		for l in list(chunks(urls, batch_size)):
			loop_start = time.time()
			found = await pool.map(fetch, l)
			loop_end = time.time()
			print('\nTime for this batch of {} items: {} \nTime per result: {}\n'.format(batch_size, loop_end-loop_start, (loop_end-loop_start) / batch_size))

if __name__ == '__main__':
	asyncio.run(main())