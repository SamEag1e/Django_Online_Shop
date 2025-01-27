from django.urls import reverse
from django.db.models import Count
from django.contrib.contenttypes.models import ContentType
from .models import Category


# ---------------------------------------------------------------------
def get_admin_category_tree(
    parent=None, app_label="products", model="product"
):
    content_type = ContentType.objects.get(app_label=app_label, model=model)

    categories = Category.objects.filter(
        parent=parent, content_type=content_type
    ).order_by("name")

    tree = []
    for category in categories:
        tree.append(
            {
                "category": category,
                "children": get_admin_category_tree(
                    parent=category, app_label=app_label, model=model
                ),
                "create_this_level_url": reverse("category_create")
                + f"?parent={category.id}",
                "update_url": reverse("category_update", args=[category.id]),
                "delete_url": reverse("category_delete", args=[category.id]),
            }
        )
    return tree


# ---------------------------------------------------------------------
def get_user_category_tree(parent=None, app_label="products", model="product"):
    content_type = ContentType.objects.get(app_label=app_label, model=model)

    categories = (
        Category.objects.filter(parent=parent, content_type=content_type)
        .annotate(product_count=Count("products"))
        .order_by("name")
    )

    tree = []
    for category in categories:
        tree.append(
            {
                "name": category.name,
                "slug": category.slug,
                "product_count": category.product_count,
                "children": get_user_category_tree(
                    parent=category, app_label=app_label, model=model
                ),
            }
        )

    return tree
