from odoo.tests import TransactionCase


class TestSaleOrderIntroductionText(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env.company.write(
            {"sale_order_introduction_text": "Test sale order introduction text"}
        )
        cls.partner = cls.env.ref("base.res_partner_1")

    def test_introduction_text(self):
        self.sale_order = self.env["sale.order"].create({"partner_id": self.partner.id})
        self.assertTrue(
            self.sale_order.sale_order_introduction_text,
            "Introduction text is not set",
        )
