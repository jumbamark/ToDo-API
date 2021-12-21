from django.urls import path
from ToDos.views import ToDosAPIView, ToDoDetailAPIView

urlpatterns = [
    # path("create/", CreateToDoAPIView.as_view(), name="create_to_do"),
    # path("list/", ToDoListAPIView.as_view(), name="list_to_dos"),
    path("", ToDosAPIView.as_view(), name="to-dos"),
    path("<int:id>/",ToDoDetailAPIView.as_view(), name="to-do")
]