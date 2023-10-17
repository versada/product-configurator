def post_init_hook(cr, registry):
    """Transfer existing weight values to weight_dummy after installation.

    Weight field is computed.
    """
    cr.execute("UPDATE product_product SET weight_dummy = weight")
