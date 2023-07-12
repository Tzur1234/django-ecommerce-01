# snippets/serializers
from rest_framework import serializers
from django_ecommerce_01.snippets.models import Snippet, LANGUAGE_CHOICES, STYLE_CHOICES


class SnippetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Snippet
        fields = (
            "id",
            "title",
            "code",
            "linenos",
            "language",
            "style",
        )