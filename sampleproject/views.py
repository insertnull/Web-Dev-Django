from django.shortcuts import render, redirect, get_object_or_404
from sampleapp.models import Item, ActionLog, CustomUser
from django.db.models import Sum, F
from django.http import HttpResponse
import json
import csv
import sys
import datetime
sys.path.append('c:\inv\myenv\lib\site-packages')
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, authenticate, login
from django.views.decorators.cache import never_cache
from django.contrib import messages
from django.contrib.auth.models import User

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("dashboard.html")
        else:
            messages.error(request, "Invalid username or password")

    return render(request, "login.html")

def logout_view(request):
    logout(request)
    request.session.flush()
    return redirect("login")

@login_required
@never_cache
def dashboard(request):
    inventory = Item.objects.filter(is_deleted=False)
    inventory_summary = (
        inventory.values('name')
        .annotate(total_quantity=Sum('quantity'))
        .order_by('-total_quantity')
    )

    recent_added = Item.objects.filter(is_deleted=False, created_at=F('modified_at')).order_by('-created_at')[:5]
    recent_modified = Item.objects.filter(is_deleted=False).exclude(created_at=F('modified_at')).order_by('-modified_at')[:5]
    recent_deleted = Item.objects.filter(is_deleted=True).order_by('-modified_at')[:5]

    all_changes = (
        list(recent_added) +
        list(recent_modified) +
        list(recent_deleted)
    )
    sorted_changes = sorted(all_changes, key=lambda x: max(x.created_at, x.modified_at), reverse=True)[:5]

    context = {
        'inventory_summary': inventory_summary,
        'recent_changes': sorted_changes,
    }
    return render(request, 'dashboard.html', context)

def generate_report(request):

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="inventory_report.pdf"'

    pdf = canvas.Canvas(response, pagesize=letter)
    pdf.setTitle("Inventory Report")

    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(100, 750, "Inventory Report")

    least_stocked_item = Item.objects.order_by('quantity').first()
    total_unique_items = Item.objects.count()
    total_items = sum(item.quantity for item in Item.objects.all())

    pdf.setFont("Helvetica", 12)
    pdf.drawString(100, 720, f"Total unique items: {total_unique_items}")
    pdf.drawString(100, 700, f"Total items in inventory: {total_items}")
    pdf.drawString(100, 680, f"Least stocked item: {least_stocked_item.name if least_stocked_item else 'N/A'}")

    pdf.drawString(100, 630, "Items in Inventory:")
    y_position = 610
    for item in Item.objects.all():
        pdf.drawString(120, y_position, f"- {item.name} (Quantity: {item.quantity})")
        y_position -= 20
        if y_position < 50:
            pdf.showPage()
            pdf.setFont("Helvetica", 12)
            y_position = 750

    pdf.save()
    return response

@login_required
@never_cache
def backup_items(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="items_backup.csv"'

    writer = csv.writer(response)
    writer.writerow(['ID', 'Name', 'Quantity', 'Price'])
    for item in Item.objects.all():
        writer.writerow([item.id, item.name, item.quantity, item.price])

    return response

@login_required
@never_cache
def search_items(request):
    query = request.GET.get('query', '')
    items = Item.objects.filter(name__icontains=query)
    return render(request, 'homepage.html', {'items': items, 'query': query})

@login_required
@never_cache
def item_list(request):
    items = Item.objects.filter(is_deleted=False) 
    return render(request, 'homepage.html', {'items': items})

@login_required
@never_cache
def add_item(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description', '')
        quantity = request.POST.get('quantity')
        price = request.POST.get('price')

        if name and quantity and price:
            Item.objects.create(
                name=name,
                description=description,
                quantity=int(quantity),
                price=float(price)
            )
            return redirect('item_list')

    return render(request, 'add_item.html')

@login_required
@never_cache
def edit_item(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    if request.method == 'POST':
        item.name = request.POST['name']
        item.description = request.POST['description']
        item.quantity = request.POST['quantity']
        item.price = request.POST['price']
        item.save()
        return redirect('item_list')
    return render(request, 'edit_item.html', {'item': item})

@login_required
@never_cache
def notifications(request):
    notifications = Item.objects.filter(is_deleted=False, quantity__lt=10)
    return render(request, 'notifications.html', {'notifications': notifications})

@login_required
@never_cache
def delete_item(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    item.is_deleted = True
    item.save()
    return redirect('item_list')

@login_required
@never_cache
def restore_item(request, item_id):
    item = get_object_or_404(Item, id=item_id, is_deleted=True)
    item.is_deleted = False
    item.save()
    return redirect('recycle_bin')

@login_required
@never_cache
def permanently_delete_item(request, item_id):
    item = get_object_or_404(Item, id=item_id, is_deleted=True)
    item.delete()
    return redirect('recycle_bin')

@login_required
@never_cache
def restore_all_items(request):
    Item.objects.filter(is_deleted=True).update(is_deleted=False)
    return redirect('recycle_bin')

@login_required
@never_cache
def delete_all_items(request):
    Item.objects.filter(is_deleted=True).delete()
    return redirect('recycle_bin')

@login_required
@never_cache
def recycle_bin(request):
    deleted_items = Item.objects.filter(is_deleted=True)
    return render(request, 'recycle_bin.html', {'deleted_items': deleted_items})
