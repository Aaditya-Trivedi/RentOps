from django.shortcuts import render, redirect
from accounts.models import Shop
from .utils import create_shop_database_and_tables
import uuid


def create_shop(request):
    if request.method == 'POST':
        shop_name = request.POST['shop_name']
        owner_name = request.POST['owner_name']
        email = request.POST['email']
        phone = request.POST['phone']

        # unique database name
        db_name = f"shop_{uuid.uuid4().hex[:8]}"

        shop = Shop.objects.create(
            shop_name=shop_name,
            owner_name=owner_name,
            email=email,
            phone=phone,
            database_name=db_name
        )

        create_shop_database_and_tables(db_name)

        return redirect('shop_success')

    return render(request, 'shops/create_shop.html')
