from django.shortcuts import render, redirect, get_object_or_404
from sampleapp.models import Item

def item_list(request):
    items = Item.objects.all()
    return render(request, 'homepage.html', {'items': items})

def add_item(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description', '')
        quantity = request.POST.get('quantity')
        price = request.POST.get('price')

        if name and quantity and price:  # Basic validation
            Item.objects.create(
                name=name,
                description=description,
                quantity=int(quantity),
                price=float(price)
            )
            return redirect('item_list')

    return render(request, 'add_item.html')

def delete_item(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    item.delete()
    return redirect('item_list')
