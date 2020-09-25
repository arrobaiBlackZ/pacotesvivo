from httpx import Client

import patches
from settings import headers, base_url

client = Client(
	headers=headers,
	base_url=base_url,
	timeout=15
)
