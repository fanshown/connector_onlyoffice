#  Copyright (c) Akretion 2020
#  License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html)

from odoo.tests import TransactionCase


class TestSaleChannel(TransactionCase):
    def setUp(self):
        super().setUp()

    def test_render_page(self):
