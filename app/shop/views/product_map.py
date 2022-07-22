import os
from django.views.decorators.http import require_POST
from django.http import HttpResponse
from pathlib import Path

# from ..models import Category, Product

@require_POST
def make_map(request):
	base_dir = Path(__file__).resolve().parent.parent.parent
	return HttpResponse(os.path.join(base_dir, 'media', 'products'))