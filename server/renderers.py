from django.utils import timezone
from rest_framework.renderers import JSONRenderer


class MetadataJSONRenderer(JSONRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        return super().render({
            'version': 1,
            'user': renderer_context['request'].user.username,
            'server_time': timezone.now(),
            'data': data,
        }, accepted_media_type, renderer_context)

