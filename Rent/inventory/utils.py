import barcode
from barcode.writer import ImageWriter
import uuid
import os
from django.conf import settings


def generate_barcode():
    code = str(uuid.uuid4().int)[:12]  # unique numeric code

    barcode_class = barcode.get_barcode_class('code128')
    barcode_instance = barcode_class(code, writer=ImageWriter())

    barcode_dir = os.path.join(settings.MEDIA_ROOT, 'barcodes')
    os.makedirs(barcode_dir, exist_ok=True)

    file_path = barcode_instance.save(
        os.path.join(barcode_dir, code)
    )

    return code, file_path
