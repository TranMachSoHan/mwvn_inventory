# Copyright 2016 Savoir-faire Linux
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

{
    "name": "Million Win Sales",
    "version": "17.0.1.0.0",
    "license": "AGPL-3",
    "category": "Web",
    "summary": "Add size and inseam to sale order field",
    "depends": ["mrp"],
    "data": [
        'security/ir.model.access.csv',
        'data/data.xml',
        'wizards/mrp_bom_lines_wizard.xml',
        "views/mrp_bom_views.xml"
    ],
    "installable": True,
    "application": False,
    "assets": {},
}
