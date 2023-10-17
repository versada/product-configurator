from odoo.exceptions import ValidationError
from odoo.tests import Form

from . import common


class ProductAttributes(common.TestProductConfiguratorCommon):
    def test_01_onchange_custome_type(self):
        self.attr_fuel.min_val = 20
        self.attr_fuel.max_val = 30
        self.attr_fuel.custom_type = "char"
        self.attr_fuel.onchange_custom_type()
        self.assertEqual(self.attr_fuel.min_val, 0, "Min value is not False")
        self.assertEqual(self.attr_fuel.max_val, 0, "Max value is not False")

        self.attr_fuel.min_val = 20
        self.attr_fuel.max_val = 30
        self.attr_fuel.custom_type = "integer"
        self.attr_fuel.onchange_custom_type()
        self.assertEqual(
            self.attr_fuel.min_val,
            20,
            "Min value is not equal to existing min value",
        )
        self.assertEqual(
            self.attr_fuel.max_val,
            30,
            "Max value is not equal to existing max value",
        )

        self.attr_fuel.custom_type = "float"
        self.attr_fuel.onchange_custom_type()
        self.assertEqual(
            self.attr_fuel.min_val,
            20,
            "Min value is equal to existing min value \
            when type is changed to integer to float",
        )
        self.assertEqual(
            self.attr_fuel.max_val,
            30,
            "Max value is equal to existing max value \
            when type is changed to integer to float",
        )
        self.attr_fuel.custom_type = "binary"
        self.attr_fuel.onchange_custom_type()
        self.assertFalse(
            self.attr_fuel.search_ok,
            "Error: if search true\
            Method: onchange_custom_type()",
        )

    def test_02_onchange_val_custom(self):
        self.attr_fuel.val_custom = False
        self.attr_fuel.custom_type = "integer"
        self.attr_fuel.onchange_val_custom_field()
        self.assertFalse(self.attr_fuel.custom_type, "custom_type is not False")

    def test_03_check_searchable_field(self):
        self.attr_fuel.custom_type = "binary"
        with self.assertRaises(ValidationError):
            self.attr_fuel.search_ok = True

    def test_04_validate_custom_val(self):
        self.attr_fuel.write({"max_val": 20, "min_val": 10})
        self.attr_fuel.custom_type = "integer"
        with self.assertRaises(ValidationError):
            self.attr_fuel.validate_custom_val(5)

        self.attr_fuel.write({"max_val": 0, "min_val": 10})
        self.attr_fuel.custom_type = "integer"
        with self.assertRaises(ValidationError):
            self.attr_fuel.validate_custom_val(5)

        self.attr_fuel.write({"min_val": 0, "max_val": 20})
        self.attr_fuel.custom_type = "integer"
        with self.assertRaises(ValidationError):
            self.attr_fuel.validate_custom_val(25)

    def test_05_check_constraint_min_max_value(self):
        self.attr_fuel.custom_type = "integer"
        with self.assertRaises(ValidationError):
            self.attr_fuel.write({"max_val": 10, "min_val": 20})

    def test_06_onchange_attribute(self):
        with Form(
            self.attr_line_fuel.product_tmpl_id
        ).attribute_line_ids.new() as attribute_form:
            attribute_form.attribute_id = self.env.ref(
                "product_configurator.product_attribute_color"
            )
            self.assertFalse(attribute_form.value_ids, "value_ids is not False")
            attribute_form.required = True
            self.assertTrue(attribute_form.required, "required not exsits value")
            attribute_form.multi = True
            self.assertTrue(attribute_form.multi, "multi not exsits value")
            attribute_form.attribute_id = self.env.ref(
                "product_configurator.product_attribute_rims"
            )
            # Values depend on attribute.
            self.assertTrue(attribute_form.required, "required not exsits value")
            self.assertFalse(attribute_form.multi, "multi not exsits value")

    def test_07_check_default_values(self):
        with self.assertRaises(ValidationError):
            self.attr_line_fuel.default_val = self.value_218i.id

    def test_08_copy_attribute(self):
        copyAttribute = self.attr_fuel.copy()
        self.assertEqual(
            copyAttribute.name,
            "Fuel (copy)",
            "Error: If not copy attribute\
            Method: copy()",
        )

    def test_09_compute_get_value_id(self):
        attrvalline = self.env["product.attribute.value.line"].create(
            {
                "product_tmpl_id": self.cfg_tmpl.id,
                "value_id": self.value_gasoline.id,
            }
        )
        self.assertTrue(
            attrvalline.product_value_ids,
            "Error: If product_value_ids not exists\
            Method: _compute_get_value_id()",
        )

    def test_10_validate_configuration(self):
        with self.assertRaises(ValidationError):
            self.env["product.attribute.value.line"].create(
                {
                    "product_tmpl_id": self.cfg_tmpl.id,
                    "value_id": self.value_diesel.id,
                    "value_ids": [(6, 0, [self.value_218i.id])],
                }
            )

    def test_11_copy(self):
        default = {}
        productattribute = self.value_gasoline.copy(default)
        self.assertEqual(
            productattribute.name,
            self.value_gasoline.name + " (copy)",
            "Error: If not equal productattribute name\
            Method: copy()",
        )

    def test_12_onchange_values(self):
        self.ProductAttributeLine.onchange_values()
        self.assertEqual(
            self.ProductAttributeLine.default_val,
            self.ProductAttributeLine.value_ids,
            "Error: If default_val not exists\
            Method: onchange_values()",
        )
