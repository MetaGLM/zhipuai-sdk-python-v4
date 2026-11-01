"""Run with ``python -I`` after installing a wheel in a clean environment."""

import asyncio
import unittest


class InstalledSDKTests(unittest.TestCase):
	def test_public_sdk_import(self):
		from zhipuai import ZhipuAI

		with ZhipuAI(api_key='test-key') as client:
			self.assertFalse(client.is_closed())
		self.assertTrue(client.is_closed())

	def test_async_library_detection(self):
		from zhipuai.core._utils import get_async_library

		self.assertEqual(get_async_library(), 'false')

		async def detect():
			return get_async_library()

		self.assertEqual(asyncio.run(detect()), 'asyncio')


if __name__ == '__main__':
	unittest.main()
