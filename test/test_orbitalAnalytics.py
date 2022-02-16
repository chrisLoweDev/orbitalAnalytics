from math import radians
import unittest
from source import config
from source import orbitalAnalytics as oa


class TestOrbitAnalytics(unittest.TestCase):
	def test_sun_sync_from_sma(self):
		self.assertEqual(
			round(oa.sun_sync_from_sma(config.R_E + 500000., 0.), 4),
			1.6998
		)

	def test_sun_sync_from_inc(self):
		self.assertEqual(
			round(oa.sun_sync_from_inc(radians(98.), 0.)),
			7027178.
		)


if __name__ == '__main__':
	unittest.main()
