from math import radians, pi
import unittest
from source import config
from source import orbitalAnalytics as oa


class TestOrbitAnalytics(unittest.TestCase):
	def test_orbit_period(self):
		alt = 500000
		self.assertAlmostEqual(
			oa.orbit_period(config.R_E + alt),
			5668.,
			0
		)

	def test_earth_regression(self):
		"""
		Test to make sure the Earth regression (i.e. the amount of Earth rotation
		relative to an inertial reference frame) is 1 full rotation in a siderial day
		:return:
		"""
		self.assertAlmostEqual(
			oa.earth_regression(config.TAU_E) / (2 * pi),
			-1.,
			3
		)

	def test_sun_sync_from_sma(self):
		self.assertAlmostEqual(
			oa.sun_sync_from_sma(config.R_E + 500000., 0.),
			1.6998,
			3
		)

	def test_sun_sync_from_inc(self):
		self.assertAlmostEqual(
			oa.sun_sync_from_inc(radians(98.), 0.),
			7027178.06737,
			3
		)




if __name__ == '__main__':
	unittest.main()
