# coding=utf-8

# Copyright (c) 2001-2016, Canal TP and/or its affiliates. All rights reserved.
#
# This file is part of Navitia,
#     the software to build cool stuff with public transport.
#
# Hope you'll enjoy and contribute to this project,
#     powered by Canal TP (www.canaltp.fr).
# Help us simplify mobility and open public transport:
#     a non ending quest to the responsive locomotion way of traveling!
#
# LICENCE: This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
# Stay tuned using
# twitter @navitia
# IRC #navitia on freenode
# https://groups.google.com/d/forum/navitia
# www.navitia.io
from __future__ import absolute_import, print_function, unicode_literals, division
from importlib import import_module
import logging


def get_args(**kwargs):
    args = {}
    for key, value in kwargs.items():
        if key == 'service_args':
            for k, v in value.items():
                if k != 'directions_options':
                    if key not in args:
                        args[key] = {}
                    args[key][k] = {}
        else:
            if key not in ['service_url',  'costing_options', 'api_key', 'timeout']:
                args[key] = value
    return args


class StreetNetwork(object):

    @staticmethod
    def get_street_network(instance, street_network_configuration):
        log = logging.getLogger(__name__)
        try:
            cls = street_network_configuration['class']
        except KeyError, TypeError:
            log.critical('impossible to build a routing, missing mandatory field in configuration')
            raise KeyError('impossible to build a routing, missing mandatory field in configuration')

        args = street_network_configuration.get('args', {})
        service_url = args.get('service_url', None)
        try:
            if '.' not in cls:
                log.critical('impossible to build StreetNetwork, wrongly formated class: {}'.format(cls))
                raise ValueError('impossible to build StreetNetwork, wrongly formated class: {}'.format(cls))

            module_path, name = cls.rsplit('.', 1)
            module = import_module(module_path)
            attr = getattr(module, name)
        except AttributeError:
            log.critical('impossible to build StreetNetwork, cannot find class: {}'.format(cls))
            raise AttributeError('impossible to build StreetNetwork, cannot find class: {}'.format(cls))

        log.info('** StreetNetwork {} used for direct_path **'.format(name))
        return attr(instance=instance, url=service_url, **args)
