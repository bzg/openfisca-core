# -*- coding: utf-8 -*-


"""
    base_function is an optional variable attribute that can optionally be set to one of the functions defined in this module.

    If a variable is calculated at a period for which it does not have a formulas, its base_function will be called to try to infere a value based on past or future values of the variable.
"""

from __future__ import unicode_literals, print_function, division, absolute_import


def requested_period_last_value(holder, period, *extra_params):
    """
        This formula is used for variables that are constants between events and period size independent.
        If the variable has no formula, it will return the latest known value of the variable
    """

    known_periods = holder.get_known_periods()
    if not known_periods:
        return holder.default_array()
    known_periods = sorted(known_periods, key=lambda period: period.start, reverse = True)
    for last_period in known_periods:
        if last_period.start <= period.start:
            return holder.get_array(last_period, extra_params)
    return None


def missing_value(holder, period, *extra_params):
    raise ValueError("Missing value for variable {} at {}".format(holder.variable.name, period))
