from django.contrib.auth.models import User
from django.db import models
from GBEX_bigfiles.fields import ResumableFileField
from GBEX_app.helpers import get_upload_path


default_order = ['id', 'name', 'responsible']


class GBEXModelBase(models.Model):
	name = models.TextField(unique=True)
	responsible = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True)
	created = models.DateTimeField(auto_now_add=True)
	edited = models.DateTimeField(auto_now=True)

	order = default_order
	symbol = ""
	col_display_func_dict = {}
	widgets = {}
	GBEX_Page = True

	def __str__(self):
		return self.name

	class Meta:
		abstract = True
		ordering = ['id']


OligoType = [
	('gRNA', 'gRNA'),
	('PCR primer', 'PCR primer'),
]


class Oligo(GBEXModelBase):
	Usage = models.TextField()
	OligoType = models.CharField(choices=OligoType, max_length=10)
	Sequence = models.TextField()

	order = [*default_order, 'Usage', 'OligoType', 'Sequence']
	menu_label = "Oligos"


class Plasmid(GBEXModelBase):
	Usage = models.TextField()
	GenbankFile = ResumableFileField(blank=True, null=True, upload_to=get_upload_path, max_length=500)

	menu_label = "Plasmids"
	order = [*default_order, 'Usage', 'GenbankFile']


ResultType = [
	('NGS', 'NGS'),
]


class RawResult(GBEXModelBase):
	Description = models.TextField()
	ResultType = models.CharField(choices=ResultType, max_length=10)
	DataFile = ResumableFileField(blank=True, null=True, upload_to=get_upload_path, max_length=500)

	menu_label = "Raw Results"
	order = [*default_order, "Description", "ResultType", 'DataFile']


class Experiment(GBEXModelBase):
	Description = models.TextField()
	Oligos = models.ManyToManyField(Oligo, blank=True)
	Plasmids = models.ManyToManyField(Plasmid, blank=True)
	Results = models.ManyToManyField(RawResult, blank=True)

	menu_label = "Experiments"
	order = [*default_order, "Description", "Oligos", "Plasmids", "Results"]

	col_display_func_dict = {
		'Oligos': lambda item: ", ".join(ab.name for ab in item.Oligos.all()) if item.Oligos.all() else "",
		'Plasmids': lambda item: ", ".join(ab.name for ab in item.Plasmids.all()) if item.Plasmids.all() else "",
		'Results': lambda item: ", ".join(ab.name for ab in item.Results.all()) if item.Results.all() else "",
	}