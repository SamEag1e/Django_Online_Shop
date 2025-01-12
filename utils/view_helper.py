from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy


class DynamicCRUDViewGenerator:
    def __init__(
        self, model, success_url_name, templates, context_object_name, fields
    ):
        """
        :param model: The model class for the views.
        :param success_url_name: The name of the URL to redirect to on success.
        :param templates: A dictionary with template names for each CRUD operation.
                          Example: {"list": "list.html", "create": "create.html", ...}
        :param context_object_name: The context object name for the ListView (optional).
        :param fields: The fields to display in the CreateView and UpdateView (optional).
        """
        self.model = model
        self.success_url_name = success_url_name
        self.templates = templates
        self.context_object_name = context_object_name
        self.fields = fields

    def list_view(self):
        class DynamicListView(ListView):
            model = self.model
            template_name = self.templates.get("list")
            context_object_name = self.context_object_name

        return DynamicListView

    def create_view(self):
        class DynamicCreateView(CreateView):
            model = self.model
            template_name = self.templates.get("create")
            fields = self.fields

            def get_success_url(inner_self):
                return reverse_lazy(self.success_url_name)

        return DynamicCreateView

    def update_view(self):
        class DynamicUpdateView(UpdateView):
            model = self.model
            template_name = self.templates.get("update")
            fields = self.fields

            def get_success_url(inner_self):
                return reverse_lazy(self.success_url_name)

        return DynamicUpdateView

    def delete_view(self):
        class DynamicDeleteView(DeleteView):
            model = self.model
            template_name = self.templates.get("delete")

            def get_success_url(inner_self):
                return reverse_lazy(self.success_url_name)

        return DynamicDeleteView
