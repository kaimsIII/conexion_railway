# views.py
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
import os

@login_required
def download_db(request):
    db_path = os.getenv('DATABASE_PATH', '/login_app/data/db.sqlite3')
    with open(db_path, 'rb') as f:
        response = HttpResponse(f.read(), content_type='application/x-sqlite3')
        response['Content-Disposition'] = 'attachment; filename=db.sqlite3'
        return response