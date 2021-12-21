from rest_framework.serializers import ModelSerializer
from ToDos.models import ToDo


class ToDoSerializer(ModelSerializer):
    class Meta:
        model= ToDo
        fields = ("id","title", "description", "is_complete")