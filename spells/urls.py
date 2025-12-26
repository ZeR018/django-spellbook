from django.urls import path

from spells.views.material_component import MaterialConponentListView

app_name = "spells"
urlpatterns = [
    path(
        "material_component/",
        MaterialConponentListView.as_view(),
        name="material_component",
    )
]
