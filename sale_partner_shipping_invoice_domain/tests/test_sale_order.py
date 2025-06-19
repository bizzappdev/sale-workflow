import json

from odoo.tests.common import TransactionCase, tagged


@tagged("post_install", "-at_install")
class TestSaleOrderPartnerDomains(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.parent_partner = cls.env.ref("base.res_partner_2")
        cls.delivery_contact = cls.env.ref("base.res_partner_4")
        cls.invoice_contact = cls.env.ref("base.res_partner_address_7")
        cls.partner = cls.env.ref("base.res_partner_3")
        cls.sale_order = cls.env.ref("sale.sale_order_2")

    def test_01_shipping_and_invoice_domain(self):
        """Test that shipping/invoice partner domain only includes child_of
        commercial partner"""

        # Load computed domains
        shipping_domain = json.loads(self.sale_order.partner_shipping_id_domain)
        invoice_domain = json.loads(self.sale_order.partner_invoice_id_domain)

        Partner = self.env["res.partner"]
        shipping_partners = Partner.search(shipping_domain)
        invoice_partners = Partner.search(invoice_domain)

        self.assertIn(
            self.delivery_contact,
            shipping_partners,
            "Delivery contact not in shipping domain",
        )
        self.assertIn(
            self.invoice_contact,
            invoice_partners,
            "Invoice contact not in invoice domain",
        )
        self.assertNotIn(
            self.partner,
            shipping_partners,
            "Invalid shipping partner included",
        )
        self.assertNotIn(
            self.partner,
            invoice_partners,
            "Invalid invoice partner included",
        )
