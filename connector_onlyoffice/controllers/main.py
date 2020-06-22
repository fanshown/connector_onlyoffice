#  Copyright (c) Akretion 2020
#  License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html)

from odoo import http
from odoo import fields, models, _
from odoo.http import Controller, request
from odoo.exceptions import ValidationError

class OnlyOfficeController(Controller):

    @property
    def onlyoffice_url(self):

    @http.route("onlyoffice/callback", auth="public", type="json")
    def onlyoffice_callback(self):
        pass

