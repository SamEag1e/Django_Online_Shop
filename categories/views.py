from django.views.generic import (
    CreateView,
    UpdateView,
    DeleteView,
    TemplateView,
)
from django.urls import reverse
from django.contrib.contenttypes.models import ContentType
from .models import Category
from .trees import get_admin_category_tree


# ---------------------------------------------------------------------
class ProductCategoryTreeView(TemplateView):
    template_name = "admin/category/category_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["category_tree"] = get_admin_category_tree()
        context["is_root"] = True
        return context


# ---------------------------------------------------------------------
class ProductCategoryCreateView(CreateView):
    model = Category
    fields = ["name", "description"]
    template_name = "admin/category/category_form.html"

    def get_initial(self):
        initial = super().get_initial()
        parent_id = self.request.GET.get("parent")
        if parent_id:
            initial["parent"] = Category.objects.get(pk=parent_id)
        return initial

    def form_valid(self, form):
        product_content_type = ContentType.objects.get(
            app_label="products", model="product"
        )
        form.instance.content_type = product_content_type
        parent_id = self.request.GET.get("parent")
        if parent_id:
            form.instance.parent = Category.objects.get(pk=parent_id)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        parent_id = self.request.GET.get("parent")
        if parent_id:
            context["parent"] = Category.objects.get(pk=parent_id)
        return context

    def get_success_url(self):
        return reverse("category_tree")


# ---------------------------------------------------------------------
class ProductCategoryUpdateView(UpdateView):
    model = Category
    fields = ["name", "description"]
    template_name = "admin/category/category_form.html"

    def form_valid(self, form):
        product_content_type = ContentType.objects.get(
            app_label="products", model="product"
        )
        form.instance.content_type = product_content_type
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("category_tree")


# ---------------------------------------------------------------------
class ProductCategoryDeleteView(DeleteView):
    model = Category
    template_name = "admin/category/category_confirm_delete.html"

    def get_success_url(self):
        return reverse("category_tree")
