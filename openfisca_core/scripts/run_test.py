# -*- coding: utf-8 -*-

import argparse
import logging
import sys
import os
import importlib

from openfisca_core.test_runner import run_tests

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('path', help = "paths (files or directories) of tests to execute", nargs = '+')
    parser.add_argument('-c', '--country_package', action = 'store', required = True)
    parser.add_argument('-f', '--force', action = 'store_true', default = False,
        help = 'force testing of tests with "ignore" flag and formulas belonging to "ignore_output_variables" list')
    parser.add_argument('-n', '--name_filter', default = None, help = "partial name of tests to execute")
    parser.add_argument('-v', '--verbose', action = 'store_true', default = False, help = "increase output verbosity")
    parser.add_argument('-m', '--relative_error_margin', help = "default relative error margin", action = 'store', type = float)
    parser.add_argument('-M', '--absolute_error_margin', help = "default absolute error margin", action = 'store', type = float)
    args = parser.parse_args()
    logging.basicConfig(level = logging.DEBUG if args.verbose else logging.WARNING, stream = sys.stdout)

    try:
        country_package = importlib.import_module(args.country_package)
        tax_benefit_system = country_package.CountryTaxBenefitSystem()
    except:
        print('ERROR: `{}` does not seem to be a valid Openfisca country package.'.format(args.country_package))
        sys.exit(1)

    options = {
        'verbose': args.verbose,
        'force': args.force,
        'name_filter': args.name_filter,
        'default_relative_error_margin': args.relative_error_margin,
        'default_absolute_error_margin': args.absolute_error_margin,
    }

    tests_found = False

    for path in args.path:
        path = os.path.abspath(path)
        nb_tests = run_tests(tax_benefit_system, path, options)
        tests_found = tests_found or nb_tests > 0

    if not tests_found:
        print("No test found!")
        sys.exit(1)

    sys.exit(0)

if __name__ == "__main__":
    main()