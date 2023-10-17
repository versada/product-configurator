from odoo.addons.product_configurator.tests import common


class TestProductConfiguratorSale(common.TestProductConfiguratorCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.SaleOrder = cls.env["sale.order"]
        cls.ProductPricelist = cls.env["product.pricelist"]
        cls.partner_sale_1 = cls.env.ref("product_configurator_sale.partner_sale_1")
        cls.currency_usd = cls.env.ref("base.USD")
        cls.ProductConfiguratorSale = cls.env["product.configurator.sale"]

    def test_01_reconfigure_product(self):
        pricelist = self.ProductPricelist.create(
            {
                "name": "Test Pricelist",
                "currency_id": self.currency_usd.id,
            }
        )
        sale_order_id = self.SaleOrder.create(
            {
                "partner_id": self.partner_sale_1.id,
                "partner_invoice_id": self.partner_sale_1.id,
                "partner_shipping_id": self.partner_sale_1.id,
                "pricelist_id": pricelist.id,
            }
        )
        context = dict(
            default_order_id=sale_order_id.id,
            wizard_model="product.configurator.sale",
        )

        self.ProductConfigurator = self.ProductConfiguratorSale.with_context(**context)

        sale_order_id.action_config_start()
        self._configure_product_nxt_step()
        sale_order_id.order_line.reconfigure_product()
        product_tmpl = sale_order_id.order_line.product_id.product_tmpl_id
        self.assertEqual(
            product_tmpl.id,
            self.cfg_tmpl.id,
            "Error: If product_tmpl not exsits\
            Method: action_config_start()",
        )
