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

    categories = Category.objects.filter(
        parent=parent, content_type=content_type
    ).order_by("name")

    tree = []
    for category in categories:
        # Count products in this category and all its descendant categories
        total_product_count = (
            Category.objects.filter(
                content_type=content_type,
                id__in=category.get_descendants(include_self=True),
            ).aggregate(total_count=Count("products"))["total_count"]
            or 0
        )

        children = get_user_category_tree(
            parent=category, app_label=app_label, model=model
        )

        tree.append(
            {
                "name": category.name,
                "slug": category.slug,
                "product_count": total_product_count,
                "children": children,
            }
        )

    return tree


# ---------------------------------------------------------------------
def get_category_and_descendants(slugs):
    """
    Given a list of category slugs, return the selected categories
    along with their descendants.
    """
    categories = Category.objects.filter(slug__in=slugs)

    # Combine selected categories with their descendants
    all_categories = categories
    for category in categories:
        all_categories = all_categories | category.get_descendants()

    return all_categories
