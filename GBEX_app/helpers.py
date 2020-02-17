from datetime import datetime
from django.utils import timezone


def field_to_string(model_instance, column: str) -> str:
	"""
		Convert a field to string
		:param model_instance: a specif model instance
		:param column: the name of the field
		:return: string version of field
	"""
	if column in model_instance.col_display_func_dict:
		return model_instance.col_display_func_dict[column](model_instance)
	else:
		field = getattr(model_instance, column)
		if hasattr(field, f'get_{column}_display'):
			display_version = getattr(field, f'get_{column}_display')()
		else:
			display_version = field
		if type(display_version) in [str, int, float]:
			return display_version
		elif isinstance(display_version, datetime):
			return str(timezone.localtime(display_version))
		elif display_version is not None:
			return str(display_version)
		else:
			return ""


def model_to_list_list(query_set):
	data = []
	fkeys = []
	m2ms = []

	# figure out which fields are relational for pre-fetching
	for field in query_set.model._meta.get_fields():
		if not field.auto_created:
			if field.is_relation:
				if field.many_to_many:
					m2ms.append(field.name)
				else:
					fkeys.append(field.name)
	# prefetch related fields and convert model instance to strings
	for row_obj in query_set.select_related(*fkeys).prefetch_related(*m2ms):
		row = []
		for column in query_set.model.order:
			row.append(field_to_string(row_obj, column))
		data.append(row)

	return data


def get_upload_path(instance, filename):
	return f"{instance._meta.model.__name__}/{instance.name}/{filename}"


def return_stripped(s):
	"""
		Attempt to clean values from excel sheets.

		:param s: value read from excel sheet via openpyxl
		:return: a value suitable for a django model field
	"""

	if type(s) == str:  # only strings can be stripped
		return s.strip()
	elif isinstance(s, (type(None),)):
		return ""
	else:  # return everything else as is
		return s
