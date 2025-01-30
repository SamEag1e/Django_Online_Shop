from categories.trees import get_user_category_tree


def get_menu_data(request):
    categories = get_user_category_tree()
    return {"categories": categories}
