from math import pi, sqrt, cos, acos
from typing import Union


MU = 398600000000000
TAU_S = 86400  # Synodic day length (seconds)
TAU_ES = 365.25 * TAU_S  # Solar period (seconds)
J2 = 0.0010826  # J2 perturbation
R_E = 6371000.8  # Earth radius, average (m)


def sun_sync(
		sma: Union[int, float] = None,
		inc: Union[int, float] = None,
		ecc: Union[int, float] = 0.
) -> tuple:
	"""
	Retuns the semi-major axis and inclination for a Sun-synchronous orbit, given an
	input of EITHER SMA or Inc, plus some orbit eccentricity.

	Note: passing both SMA and inc will result in an Attribute Error

	:param sma: Semi-major axis (m)
	:param inc: Inclination (radians)
	:param ecc: Eccentricity
	:return: Tuple containing the Semi-major axis (m) and Inclination (radians)
	"""
	if sma and inc:
		raise AttributeError(
			"Cannot specify both Semi-major axis and Inclination. Define one or the other"
		)

	if sma:
		if sma < R_E:
			raise ValueError(
				"Semi-major axis must be greater than the radius of the Earth"
			)

		if sma * (1-ecc) - R_E < 100000:
			p = (sma * (1-ecc) - R_E) / 1000
			string = "Orbit perigee must be greater than 100km, currently is %2d km" % p
			raise ValueError(string)

		# Orbit period (s)
		tau = 2 * pi * sqrt(sma ** 3 / MU)

		# Regression of the line of nodes (rad/orbit)
		phi = 2 * pi * tau / TAU_ES

		inc = acos(-phi * sma**2 * ((1 - ecc**2)**2) / (3 * pi * J2 * R_E**2))

	elif inc:
		sma = (-3*sqrt(MU)*TAU_ES*J2*R_E**2*cos(inc)/(4*pi*((1-ecc**2)**2)))**(2/7)

	else:
		raise AttributeError("Must specify either semi-major axis OR inclination")

	return sma, inc
