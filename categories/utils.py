from django.utils.text import slugify


# ---------------------------------------------------------------------
def get_slug(instance):
    if not instance.id:
        if instance.parent:
            # Create the slug from the parent category
            # and the current category's name
            ancestors = [
                ancestor.name
                for ancestor in instance.parent.get_ancestors(
                    include_self=True
                )
            ]
            return slugify(
                "-".join(ancestors + [instance.name]), allow_unicode=True
            )
        return slugify(instance.name, allow_unicode=True)

    # If the instance has an ID, generate the slug based on
    # the updated name entered by the user
    ancestors = [
        ancestor.name
        for ancestor in instance.get_ancestors(include_self=False)
    ]
    return slugify("-".join(ancestors + [instance.name]), allow_unicode=True)
