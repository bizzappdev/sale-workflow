# Copyright 2021 Tecnativa - Ernesto Tejeda
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def action_cancel(self):
        """Force to call the cancel method on done picking for having the
        expected error, as Odoo has now filter out such pickings from the
        cancel operation.
        """
        self.mapped("picking_ids").filtered(lambda r: r.state == "done").action_cancel()
        return super().action_cancel()

    def _action_cancel(self):
        """Inherited method to handle the case when the pickings of sale
        orders are confirmed and attempting to cancel the sale orders from
        the list view;this method raises a validation error."""
        self.picking_ids.filtered(
            lambda picking: picking.state == "done"
        ).action_cancel()
        return super()._action_cancel()
