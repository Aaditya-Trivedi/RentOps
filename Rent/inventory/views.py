from django.shortcuts import render, redirect
from .models import Cloth, ClothBarcode
from .utils import generate_barcode
from django.http import FileResponse
import os
from django.conf import settings

def add_cloth(request):
    if request.method == 'POST':
        cloth = Cloth.objects.create(
            name=request.POST['name'],
            category_id=request.POST['category'],
            sub_category_id=request.POST['sub_category'],
            size=request.POST['size'],
            color=request.POST['color'],
            rent_price=request.POST['rent_price']
        )

        code, path = generate_barcode()

        ClothBarcode.objects.create(
            cloth=cloth,
            barcode=code
        )

        return redirect('cloth_list')

    return render(request, 'inventory/add_cloth.html')


def download_barcode(request, code):
    file_path = os.path.join(settings.MEDIA_ROOT, 'barcodes', f"{code}.png")
    return FileResponse(open(file_path, 'rb'), as_attachment=True)