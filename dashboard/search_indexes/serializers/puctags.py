import json

from rest_framework import serializers

class TagSerializer(serializers.Serializer):
    """Helper serializer for the PUCTag field of the Product document."""

    title = serializers.CharField()

    class Meta(object):
        """Meta options."""

        fields = ('name','slug')
        read_only_fields = ('name','slug')