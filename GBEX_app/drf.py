from django.apps import apps
from rest_framework import serializers, viewsets, permissions
from GBEX_bigfiles.drf import ResumableDRFFileField
from GBEX_bigfiles.fields import ResumableFileField


GBEX_API_ViewSets = []


for model in apps.get_app_config('GBEX_app').get_models():
	file_fields = [x.name for x in model._meta.fields if isinstance(x, ResumableFileField)]

	serial = type(f"{model.__name__}Serializer", (serializers.ModelSerializer, ), {
		**{x: ResumableDRFFileField(required=False, allow_empty_file=True, allow_null=True) for x in file_fields},
		"Meta": type(f"{model.__name__}Serializer.Meta", (), {"model": model, "fields": "__all__"})
	})
	viewset = type(f"{model.__name__}ViewSet", (viewsets.ModelViewSet,), {
		"queryset": model.objects.all(),
		"serializer_class": serial,
		"permission_classes": [permissions.IsAuthenticatedOrReadOnly],
		"filter_fields": '__all__',
	})
	GBEX_API_ViewSets.append((model.__name__, viewset))
