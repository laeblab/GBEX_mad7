from django.urls import path, re_path
from django.apps import apps
from GBEX_app.views import GBEXindex, GBEXList, ExcelExportView


urlpatterns = [
	path('', GBEXindex.as_view(), name='GBEXindex'),
] + [
	path(f'{model.__name__}/', GBEXList.as_view(model=model), name=f'list_{model.__name__}')
	for model in apps.get_app_config('GBEX_app').get_models() if hasattr(model, "GBEX_Page")
] + [
	re_path(f'{model.__name__}/exportexcel/(?P<rids>.*)$', ExcelExportView.as_view(model=model), name=f'export_{model.__name__}')
	for model in apps.get_app_config('GBEX_app').get_models() if hasattr(model, "GBEX_Page")
]
