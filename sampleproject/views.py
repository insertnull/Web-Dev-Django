from django.shortcuts import render, redirect, get_object_or_404
from sampleapp.models import Item, RecycleBin, ActionLog
from django.db.models import Sum
from django.http import HttpResponse
import json
import csv
import sys
import datetime
sys.path.append('c:\inv\myenv\lib\site-packages')
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def dashboard(request):
    # Data for the pie chart
    inventory = Item.objects.all()
    inventory_summary = (
        inventory.values('name')
        .annotate(total_quantity=Sum('quantity'))
        .order_by('-total_quantity')
    )

    # Recent changes (latest 10 entries)
    recent_changes = ActionLog.objects.order_by('-action_date')[:10]

    context = {
        'inventory_summary': inventory_summary,
        'recent_changes': recent_changes,
    }
    return render(request, 'dashboard.html', context)

def generate_report(request):
    # Create the HTTP response object with PDF headers
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="inventory_report.pdf"'

    # Create a PDF canvas
    pdf = canvas.Canvas(response, pagesize=letter)
    pdf.setTitle("Inventory Report")

    # Add title
    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(100, 750, "Inventory Report")

    # Compute metrics
    least_stocked_item = Item.objects.order_by('quantity').first()
    total_unique_items = Item.objects.count()
    total_items = sum(item.quantity for item in Item.objects.all())

    # Add summary metrics
    pdf.setFont("Helvetica", 12)
    pdf.drawString(100, 720, f"Total unique items: {total_unique_items}")
    pdf.drawString(100, 700, f"Total items in inventory: {total_items}")
    pdf.drawString(100, 680, f"Least stocked item: {least_stocked_item.name if least_stocked_item else 'N/A'}")

    # Add inventory details
    pdf.drawString(100, 630, "Items in Inventory:")
    y_position = 610
    for item in Item.objects.all():
        pdf.drawString(120, y_position, f"- {item.name} (Quantity: {item.quantity})")
        y_position -= 20
        if y_position < 50:  # Create a new page if content overflows
            pdf.showPage()
            pdf.setFont("Helvetica", 12)
            y_position = 750

    # Finalize the PDF
    pdf.save()
    return response

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
    items = Item.objects.filter(is_deleted=False)  # Exclude soft-deleted items
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

def notifications(request):
    notifications = Item.objects.filter(is_deleted=False, quantity__lt=10)  # Low stock, not deleted
    return render(request, 'notifications.html', {'notifications': notifications})

def delete_item(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    item.is_deleted = True
    item.save()
    return redirect('item_list')  # Replace with the name of your homepage URL

def restore_item(request, item_id):
    item = get_object_or_404(Item, id=item_id, is_deleted=True)
    item.is_deleted = False
    item.save()
    return redirect('recycle_bin')

def permanently_delete_item(request, item_id):
    item = get_object_or_404(Item, id=item_id, is_deleted=True)
    item.delete()
    return redirect('recycle_bin')

def recycle_bin(request):
    deleted_items = Item.objects.filter(is_deleted=True)
    return render(request, 'recycle_bin.html', {'deleted_items': deleted_items})
