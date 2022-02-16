from math import pi, sqrt, cos, acos, radians
from typing import Union
from source import config


def orbit_period(sma):
	return 2 * pi * sqrt(sma ** 3 / config.MU)


def nodal_regression(tau):
	"""
	Regression of the line of nodes (rads/orbit)
	:param tau: orbit period (s)
	:return:
	"""
	return 2 * pi * tau / config.TAU_ES


def earth_regression(tau):
	"""
	Rotation of the Earth underneath the orbit plane (rads/orbit)
	:param tau: orbit period (s)
	:return:
	"""
	return -2 * pi * tau / config.TAU_E


def nodal_regression_sidereal(sma, inc, ecc):
	return (-3 * pi * config.J2 * config.R_E**2 * cos(inc)) / (sma**2 * ((1 - ecc**2)**2))


def sun_sync_from_sma(
		sma: Union[int, float] = config.R_E + 500000.,
		ecc: Union[int, float] = 0.
) -> float:
	"""
	Retuns the inclination for a Sun-synchronous orbit, given an input semi-major axis
	and eccentricity.

	:param sma: Semi-major axis (m)
	:param ecc: Eccentricity
	:return: Inclination (radians)
	"""
	if sma < config.R_E:
		raise ValueError(
			"Semi-major axis must be greater than the radius of the Earth"
		)

	if sma * (1-ecc) - config.R_E < 100000:
		p = (sma * (1-ecc) - config.R_E) / 1000
		string = "Orbit perigee must be greater than 100km, currently is %2d km" % p
		raise ValueError(string)

	# Orbit period (s)
	tau = orbit_period(sma)

	# Regression of the line of nodes (rad/orbit)
	phi = nodal_regression(tau)

	inc = acos(-phi * sma**2 * ((1 - ecc**2)**2) / (3 * pi * config.J2 * config.R_E**2))

	return inc


def sun_sync_from_inc(
		inc: Union[int, float] = radians(98.),
		ecc: Union[int, float] = 0.
) -> float:
	"""
	Retuns the semi-major axis (m) for a Sun-synchronous orbit, given an inclination and
	eccentricity.

	:param inc: Inclination (radians)
	:param ecc: Eccentricity
	:return: Semi-major axis (m)
	"""

	sma = (-3*sqrt(config.MU)*config.TAU_ES*config.J2*config.R_E**2*cos(inc)/(4*pi*((1-ecc**2)**2)))**(2/7)

	return sma


# def earth_sync_from_inc(
# 		inc: Union[int, float] = radians(60.),
# 		m: int = 1,
# 		n: int = 16,
# 		ecc: Union[int, float] = 0.
# ) -> float:
# 	"""
# 	Return the Semi-major axis that results in a repeat ground track after an integer
# 	number of orbits (n) and integer number of days (m)
# 	:param inc:
# 	:param m:
# 	:param n:
# 	:param ecc:
# 	:return sma:
# 	"""
# 	phi = 1.
# 	tol = 0.000001
# 	while abs(phi + (m * 2 * pi / n)) > tol:
# 		# TODO adjust SMA to get us closer to the desired regression
# 		# sma = ...
# 		tau = orbit_period(sma)
# 		phi1 = earth_regression(tau)
# 		phi2 = nodal_regression_sidereal(sma, inc, ecc)
# 		phi = phi1 + phi2

