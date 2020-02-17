from django.http import HttpResponse
from .files import ResumableFile, get_storage


def resumable_upload(request):
	storage = get_storage(request)
	if request.method == 'POST':
		chunk = request.FILES.get('file')
		r = ResumableFile(storage, request.POST)
		if not r.chunk_exists:
			r.process_chunk(chunk)
		if r.is_complete:
			actual_filename = storage.save(r.filename, r.file)
			r.delete_chunks()
			return HttpResponse(storage.url(actual_filename), status=201)
		return HttpResponse('chunk uploaded')
	elif request.method == 'GET':
		r = ResumableFile(storage, request.GET)
		if not r.chunk_exists:
			return HttpResponse('chunk not found', status=404)
		if r.is_complete:
			actual_filename = storage.save(r.filename, r.file)
			r.delete_chunks()
			return HttpResponse(storage.url(actual_filename), status=201)
		return HttpResponse('chunk exists', status=200)
