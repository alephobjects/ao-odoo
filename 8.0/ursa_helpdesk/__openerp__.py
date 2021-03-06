# -*- coding: utf-8 -*-
##############################################################################
#
#    Ursa Information Systems
#    Copyright (C) 2013 (<http://www.ursainfosystems.com>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
############################################################################################################################################################

{
    "name" : "HelpDesk Set Reply-To",
    "version" : "1.0",
    "author" : ["Ursa Information Systems, USA"],
    "category": 'Sales Management',
    'complexity': "normal",
    "description": """
Sets reply-to in the helpdesk item.

This allows a standard reply-to address to be set when chatter is used to respond to help desk issues.

    """,
    'website': 'http://www.ursainfosystems.com',
    "depends" : ["mail", "crm_helpdesk","fetchmail"],
    'data': ['ursa_helpdesk.xml'],
    'demo': [],
    'installable': True,
    'auto_install': False,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
