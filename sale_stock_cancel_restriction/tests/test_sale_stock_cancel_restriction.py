# Copyright 2021 Tecnativa - Ernesto Tejeda
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.exceptions import UserError
from odoo.tests import Form, TransactionCase


class TestSaleStockCancelRestriction(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.product = cls.env["product.product"].create(
            {"name": "Product test", "is_storable": True}
        )
        cls.partner = cls.env["res.partner"].create({"name": "Partner test"})
        so_form = Form(cls.env["sale.order"])
        so_form.partner_id = cls.partner
        with so_form.order_line.new() as soline_form:
            soline_form.product_id = cls.product
            soline_form.product_uom_qty = 2
        cls.sale_order = so_form.save()
        cls.sale_order.action_confirm()
        cls.picking = cls.sale_order.picking_ids
        cls.picking.move_ids.quantity = 2
        cls.partner_1 = cls.env["res.partner"].create(
            {
                "name": "Test Partner",
            }
        )
        cls.product_1 = cls.env["product.product"].create(
            {
                "name": "Test Product",
                "standard_price": 100.0,
            }
        )
        cls.sale_order_1 = cls.env["sale.order"].create(
            {
                "partner_id": cls.partner_1.id,
                "order_line": [
                    (
                        0,
                        0,
                        {
                            "product_id": cls.product_1.id,
                        },
                    ),
                ],
            }
        )
        cls.sale_order_2 = cls.env["sale.order"].create(
            {
                "partner_id": cls.partner_1.id,
                "order_line": [
                    (
                        0,
                        0,
                        {
                            "product_id": cls.product_1.id,
                        },
                    ),
                ],
            }
        )

    def test_cancel_sale_order_restrict(self):
        """Validates the picking and do the assertRaises cancelling the
        order for checking that it's forbidden
        """
        self.picking.button_validate()
        with self.assertRaises(UserError):
            self.sale_order.action_cancel()

    def test_cancel_sale_order_ok(self):
        """When canceling the order, the wizard is generated with the
        model 'sale.order.cancel
        """
        wizz = self.sale_order.action_cancel()
        self.assertEqual(
            wizz["res_model"],
            "sale.order.cancel",
        )

    def test_cancel_sale_order_from_list_view_with_done_picking(self):
        """New method that check sale orders cancellation from list view
        raises a UserError when sale orders have pickings that are in
        the 'done' state."""
        self.sale_order_1.action_confirm()
        self.sale_order_2.action_confirm()
        self.picking_1 = self.sale_order_1.picking_ids[:1]
        self.picking_2 = self.sale_order_2.picking_ids[:1]
        self.picking_1.button_validate()
        self.picking_2.button_validate()
        self.mass_cancel = self.env["sale.mass.cancel.orders"].create(
            {"sale_order_ids": [(6, 0, [self.sale_order_1.id, self.sale_order_2.id])]}
        )
        with self.assertRaises(UserError):
            self.mass_cancel.action_mass_cancel()

    def test_cancel_sale_orders_from_list_view(self):
        """New method that check sale order cancellation from list view"""
        self.sale_order_1.action_confirm()
        self.sale_order_1._action_cancel()
        self.assertEqual(self.sale_order_1.state, "cancel")
