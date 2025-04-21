# ---------------------------------------------------------------------
def primary_image_path(instance, filename):
    return f"products/images/{instance.sku}/{filename}"


# ---------------------------------------------------------------------
def additional_image_path(instance, filename):
    return f"products/images/{instance.product.sku}/{filename}"


# ---------------------------------------------------------------------
def get_sorting_field(order):
    if order == "most_recent":
        return "-created_at"
    if order == "most_recently_updated":
        return "-updated_at"
    if order == "price_asc":
        return "discounted_price"
    if order == "price_desc":
        return "-discounted_price"
    if order == "top_selling":
        return "-sales"
    return "-created_at"
