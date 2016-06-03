# -*- coding: utf-8 -*-
# © 2016 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from openerp.tests.common import TransactionCase


class TestDeliverySingle(TransactionCase):

    def setUp(self):
        super(TestDeliverySingle, self).setUp()
        # Products
        p1 = self.env.ref('product.product_product_15')
        p2 = self.env.ref('product.product_product_25')

        # Locations
        l1 = self.env.ref('stock.stock_location_stock')
        self.l2 = self.env['stock.location'].create({
            'location_id': l1.id,
            'name': 'Shelf 1',
            'usage': 'internal'
        })

        # 2 dates we can use to test the features
        self.date_sooner = '2015-01-01'
        self.date_later = '2015-12-13'

        self.po = self.env['purchase.order'].create({
            'partner_id': self.ref('base.res_partner_3'),
            'location_id': self.ref('stock.stock_location_stock'),
            'pricelist_id': self.ref('purchase.list0'),
            'order_line': [
                (0, 0, {'product_id': p1.id,
                        'name': p1.name,
                        'price_unit': p1.standard_price,
                        'date_planned': self.date_sooner,
                        'product_qty': 42.0,
                        'location_dest_id': l1.id}),
                (0, 0, {'product_id': p2.id,
                        'name': p2.name,
                        'price_unit': p2.standard_price,
                        'date_planned': self.date_sooner,
                        'product_qty': 12.0,
                        'location_dest_id': l1.id}),
                (0, 0, {'product_id': p1.id,
                        'name': p1.name,
                        'price_unit': p1.standard_price,
                        'date_planned': self.date_sooner,
                        'product_qty': 1.0,
                        'location_dest_id': l1.id})]})

    def test_check_single_date(self):
        self.assertEquals(
            len(self.po.picking_ids), 0,
            "There must not be pickings for the PO when draft")

        self.po.signal_workflow('purchase_confirm')
        self.assertEquals(
            len(self.po.picking_ids), 1,
            "There must be 1 picking for the PO when confirmed")
        self.assertEquals(
            self.po.picking_ids[0].min_date[:10], self.date_sooner,
            "The picking must be planned at the expected date")

    def test_check_multiple_dates(self):
        # Change the date of the first line
        self.po.order_line[0].date_planned = self.date_later

        self.assertEquals(
            len(self.po.picking_ids), 0,
            "There must not be pickings for the PO when draft")

        self.po.signal_workflow('purchase_confirm')
        self.assertEquals(
            len(self.po.picking_ids), 2,
            "There must be 2 pickings for the PO when confirmed")

        sorted_pickings = sorted(self.po.picking_ids, key=lambda x: x.min_date)
        self.assertEquals(
            sorted_pickings[0].min_date[:10], self.date_sooner,
            "The first picking must be planned at the soonest date")
        self.assertEquals(
            sorted_pickings[1].min_date[:10], self.date_later,
            "The second picking must be planned at the latest date")

    def test_check_multiple_locations_same_date(self):
        # Change the location of the first line
        self.po.order_line[0].location_dest_id = self.l2

        self.assertEquals(
            len(self.po.picking_ids), 0,
            "There must not be pickings for the PO when draft")

        self.po.signal_workflow('purchase_confirm')
        self.assertEquals(
            len(self.po.picking_ids), 2,
            "There must be 2 pickings for the PO when confirmed")

    def test_check_multiple_locations_multiple_dates(self):
        # Change the location of the first line and date of the second line
        self.po.order_line[0].location_dest_id = self.l2
        self.po.order_line[1].date_planned = self.date_later

        self.assertEquals(
            len(self.po.picking_ids), 0,
            "There must not be pickings for the PO when draft")

        self.po.signal_workflow('purchase_confirm')
        self.assertEquals(
            len(self.po.picking_ids), 3,
            "There must be 3 pickings for the PO when confirmed")

        sorted_pickings = sorted(self.po.picking_ids, key=lambda x: x.min_date)
        self.assertEquals(
            sorted_pickings[0].min_date[:10], self.date_sooner,
            "The first picking must be planned at the soonest date")
        self.assertEquals(
            sorted_pickings[2].min_date[:10], self.date_later,
            "The second picking must be planned at the latest date")
