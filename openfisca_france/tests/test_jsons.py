#! /usr/bin/env python
# -*- coding: utf-8 -*-


# OpenFisca -- A versatile microsimulation software
# By: OpenFisca Team <contact@openfisca.fr>
#
# Copyright (C) 2011, 2012, 2013, 2014 OpenFisca Team
# https://github.com/openfisca
#
# This file is part of OpenFisca.
#
# OpenFisca is free software; you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# OpenFisca is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

########### DESCRIPTION ############
## Ce programme teste tous les fichiers .json créés par un script et renvoie les erreurs d'OpenFisca

import json
import os
import sys

import numpy as np
import openfisca_france
from openfisca_france.scripts.compare_openfisca_impots import compare_variable


TaxBenefitSystem = openfisca_france.init_country()
tax_benefit_system = TaxBenefitSystem()

def test():
    path = os.path.join(os.path.dirname(__file__), 'json')
    err = 1
    for filename in os.listdir(path):
        with open(os.path.join(path, filename)) as officiel:
            try:
                content = json.load(officiel)
            except:
                print filename
                continue
            official_result = content['resultat_officiel']
            json_scenario = content['scenario']

            scenario, error = tax_benefit_system.Scenario.make_json_to_instance(
                tax_benefit_system = tax_benefit_system)(json_scenario)
            if error is not None:
                print 'error:', filename, scenario, error
                continue

            year = json_scenario['year']
            totpac = scenario.test_case['foyers_fiscaux'].values()[0].get('personnes_a_charge')

            simulation = scenario.new_simulation()

            for code, field in official_result.iteritems():
                if compare_variable(code, field, simulation, totpac, filename, year):
                    err = 0

    assert err, "Erreur"


if __name__ == "__main__":
    sys.exit(test())