from . import common


class ConfigurationCreate(common.TestProductConfiguratorCommon):
    def test_01_create(self):
        """Test configuration item does not make variations."""
        attr_test = self.ProductAttribute.create(
            {
                "name": "Test",
                "value_ids": [
                    (0, 0, {"name": "1"}),
                    (0, 0, {"name": "2"}),
                ],
            }
        )

        test_template = self.ProductTemplate.create(
            {
                "name": "Test Configuration",
                "config_ok": True,
                "type": "consu",
                "categ_id": self.product_category_5.id,
                "attribute_line_ids": [
                    (
                        0,
                        0,
                        {
                            "attribute_id": attr_test.id,
                            "value_ids": [
                                (6, 0, attr_test.value_ids.ids),
                            ],
                            "required": True,
                        },
                    ),
                ],
            }
        )

        self.assertEqual(
            len(test_template.product_variant_ids),
            0,
            "Create should not have any variants",
        )

    def test_02_previous_step_incompatible_changes(self):
        """Test changes in previous steps.

        These steps would makes values in next configuration steps invalid"""
        product_config_wizard = self.ProductConfigurator.create(
            {
                "product_tmpl_id": self.cfg_tmpl.id,
            }
        )
        product_config_wizard.action_next_step()
        product_config_wizard.write(
            {
                f"__attribute_{self.attr_fuel.id}": self.value_gasoline.id,
                f"__attribute_{self.attr_engine.id}": self.value_218i.id,
            }
        )
        product_config_wizard.action_next_step()
        product_config_wizard.write(
            {
                f"__attribute_{self.attr_color.id}": self.value_red.id,
                f"__attribute_{self.attr_rims.id}": self.value_rims_378.id,
            }
        )
        product_config_wizard.action_next_step()
        product_config_wizard.write(
            {
                "__attribute_{}".format(
                    self.attr_model_line.id
                ): self.value_sport_line.id,
            }
        )
        product_config_wizard.action_previous_step()
        product_config_wizard.action_previous_step()
        product_config_wizard.write(
            {
                f"__attribute_{self.attr_engine.id}": self.value_220i.id,
            }
        )
        product_config_wizard.action_next_step()
        product_config_wizard.action_next_step()
        product_config_wizard.write(
            {
                "__attribute_{}".format(
                    self.attr_model_line.id
                ): self.value_model_sport_line.id,
            }
        )
        product_config_wizard.action_next_step()
        product_config_wizard.write(
            {
                f"__attribute_{self.attr_tapistry.id}": self.value_tapistry.id,
            }
        )
        product_config_wizard.action_next_step()
        product_config_wizard.write(
            {
                "__attribute_{}".format(
                    self.attr_transmission.id
                ): self.value_transmission.id,
                f"__attribute_{self.attr_options.id}": [
                    [6, 0, [self.value_options_1.id, self.value_options_2.id]]
                ],
            }
        )
        product_config_wizard.action_next_step()
        value_ids = (
            self.value_gasoline
            + self.value_220i
            + self.value_red
            + self.value_rims_378
            + self.value_model_sport_line
            + self.value_tapistry
            + self.value_transmission
            + self.value_options_1
            + self.value_options_2
        )
        new_variant = self.cfg_tmpl.product_variant_ids.filtered(
            lambda variant: variant.product_template_attribute_value_ids.product_attribute_value_id
            == value_ids
        )
        self.assertNotEqual(
            new_variant.id,
            False,
            "Variant not generated at the end of the configuration process",
        )
