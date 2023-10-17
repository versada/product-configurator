from odoo import SUPERUSER_ID
from odoo.exceptions import ValidationError

from . import common


class ConfigurationRules(common.TestProductConfiguratorCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.cfg_session = cls.ProductConfigSession.create(
            {"product_tmpl_id": cls.cfg_tmpl.id, "user_id": SUPERUSER_ID}
        )
        attribute_vals = cls.cfg_tmpl.attribute_line_ids.mapped("value_ids")
        cls.attr_vals = cls.cfg_tmpl.attribute_line_ids.mapped("value_ids")
        cls.attr_val_ext_ids = {
            v: k for k, v in attribute_vals.get_external_id().items()
        }

    def get_attr_val_ids(self, ext_ids):
        """Return a list of database ids using the external_ids
        passed via ext_ids argument"""

        value_ids = []

        attr_val_prefix = "product_configurator.product_attribute_value_%s"

        for ext_id in ext_ids:
            if ext_id in self.attr_val_ext_ids:
                value_ids.append(self.attr_val_ext_ids[ext_id])
            elif attr_val_prefix % ext_id in self.attr_val_ext_ids:
                value_ids.append(self.attr_val_ext_ids[attr_val_prefix % ext_id])

        return value_ids

    def test_01_valid_configuration(self):
        """Test validation of a valid configuration"""

        conf = [
            "gasoline",
            "228i",
            "model_luxury_line",
            "silver",
            "rims_384",
            "tapistry_black",
            "steptronic",
            "smoker_package",
            "tow_hook",
        ]

        attr_val_ids = self.get_attr_val_ids(conf)
        validation = self.cfg_session.validate_configuration(attr_val_ids)
        self.assertTrue(validation, "Valid configuration failed validation")

    def test_02_invalid_configuration(self):

        conf = [
            "diesel",
            "228i",
            "model_luxury_line",
            "silver",
            "rims_384",
            "tapistry_black",
            "steptronic",
            "smoker_package",
            "tow_hook",
        ]

        attr_val_ids = self.get_attr_val_ids(conf)
        with self.assertRaises(ValidationError):
            self.cfg_session.validate_configuration(attr_val_ids)

    def test_03_missing_val_configuration(self):
        conf = [
            "diesel",
            "228i",
            "model_luxury_line",
            "rims_384",
            "tapistry_black",
            "steptronic",
            "smoker_package",
            "tow_hook",
        ]

        attr_val_ids = self.get_attr_val_ids(conf)
        with self.assertRaises(ValidationError):
            self.cfg_session.validate_configuration(attr_val_ids)

    def test_04_invalid_multi_configuration(self):
        conf = [
            "gasoline",
            "228i",
            "model_luxury_line",
            "silver",
            "red",
            "rims_384",
            "tapistry_black",
            "steptronic",
            "smoker_package",
            "tow_hook",
        ]

        attr_val_ids = self.get_attr_val_ids(conf)
        with self.assertRaises(ValidationError):
            self.cfg_session.validate_configuration(attr_val_ids)

    def test_05_invalid_custom_value_configuration(self):
        conf = [
            "gasoline",
            "228i",
            "model_luxury_line",
            "rims_384",
            "tapistry_black",
            "steptronic",
            "smoker_package",
            "tow_hook",
        ]

        attr_color_id = self.env.ref("product_configurator.product_attribute_color")

        custom_vals = {attr_color_id: {"value": "#fefefe"}}

        attr_val_ids = self.get_attr_val_ids(conf)
        with self.assertRaises(ValidationError):
            self.cfg_session.validate_configuration(attr_val_ids, custom_vals)

    # TODO: Test configuration with disallowed custom type value
