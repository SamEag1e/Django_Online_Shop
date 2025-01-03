# ---------------------------------------------------------------------
def primary_image_path(instance, filename):
    return f"products/images/{instance.sku}/{filename}"


# ---------------------------------------------------------------------
def additional_image_path(instance, filename):
    return f"products/images/{instance.product.sku}/{filename}"
