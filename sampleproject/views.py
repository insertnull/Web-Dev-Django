from django.shortcuts import render, redirect, get_object_or_404
from sampleapp.models import Item
from django.http import HttpResponse
import json
import csv

def backup_items(request):
    # Create the HTTP response object with CSV headers
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="items_backup.csv"'

    # Write CSV data
    writer = csv.writer(response)
    writer.writerow(['ID', 'Name', 'Quantity', 'Price'])  # Adjust headers as needed
    for item in Item.objects.all():
        writer.writerow([item.id, item.name, item.quantity, item.price])  # Match your model fields

    return response

def item_list(request):
    # Fetch all items or filter based on the search query
    query = request.GET.get('search', '')
    items = Item.objects.filter(name__icontains=query) if query else Item.objects.all()

    # Identify low-stock items
    low_stock_items = items.filter(quantity__lte=10)

    # Serialize low-stock items into JSON
    low_stock_items_json = json.dumps([
        {"name": item.name, "quantity": item.quantity} for item in low_stock_items
    ])

    return render(request, 'homepage.html', {
        'items': items,
        'low_stock_items': low_stock_items,  # For template rendering
        'low_stock_items_json': low_stock_items_json,  # For dynamic rendering
    })

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

def edit_item(request, item_id):
    item = get_object_or_404(Item, id=item_id)  # Use item_id to fetch the item
    if request.method == 'POST':
        # Update item logic
        item.name = request.POST['name']
        item.description = request.POST['description']
        item.quantity = request.POST['quantity']
        item.price = request.POST['price']
        item.save()
        return redirect('item_list')
    return render(request, 'edit_item.html', {'item': item})

