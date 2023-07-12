from django.contrib.auth import get_user_model
from rest_framework import serializers
from django_ecommerce_01.snippets.models import Snippet

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):

    snippets = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Snippet.objects.all()
    )

    class Meta:
        model = User
        fields = ["name", "url", "snippets"]

        extra_kwargs = {
            "url": {"view_name": "api:user-detail", "lookup_field": "pk"},
        }
