# views.py
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
import os
import logging

logger = logging.getLogger(__name__)

@login_required
def download_db(request):
    db_path = os.getenv('DATABASE_PATH', '/login_app/data/db.sqlite3')
    logger.info(f"Descargando base de datos desde: {db_path}")
    try:
        with open(db_path, 'rb') as f:
            response = HttpResponse(f.read(), content_type='application/x-sqlite3')
            response['Content-Disposition'] = 'attachment; filename=db.sqlite3'
            return response
    except FileNotFoundError:
        logger.error(f"Archivo no encontrado: {db_path}")
        return HttpResponse("Archivo de base de datos no encontrado", status=404)