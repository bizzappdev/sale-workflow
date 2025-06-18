import json

from odoo.tests.common import TransactionCase


class TestSaleOrderPartnerDomains(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        Partner = cls.env["res.partner"]

        # Create parent company (commercial partner)
        cls.parent_partner = Partner.create(
            {
                "name": "Test Company",
                "company_type": "company",
            }
        )
        # Create child delivery and invoice contact
        cls.delivery_contact = Partner.create(
            {
                "name": "Delivery Contact",
                "parent_id": cls.parent_partner.id,
                "type": "delivery",
            }
        )
        cls.invoice_contact = Partner.create(
            {
                "name": "Invoice Contact",
                "parent_id": cls.parent_partner.id,
                "type": "invoice",
            }
        )

        cls.unrelated_partner = Partner.create(
            {
                "name": "Unrelated Partner",
            }
        )
        cls.sale_order = cls.env["sale.order"].create(
            {
                "partner_id": cls.parent_partner.id,
            }
        )

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
            self.unrelated_partner,
            shipping_partners,
            "Unrelated partner in shipping domain",
        )
        self.assertNotIn(
            self.unrelated_partner,
            invoice_partners,
            "Unrelated partner in invoice domain",
        )
