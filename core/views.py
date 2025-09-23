from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.db.models import Count

import random
from django.utils.timezone import now, timedelta
from django.core.mail import send_mail
from django.urls import reverse
from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.hashers import make_password
from django.shortcuts import render, get_object_or_404, redirect


from .forms import ItemForm
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Item, Reservation


# Step 1: Send reset code
import random
from django.core.mail import send_mail
from django.contrib import messages
from django.shortcuts import render, redirect

def forgot_password(request):
    # Generate a 6-digit reset code
    reset_code = str(random.randint(100000, 999999))
    request.session['reset_code'] = reset_code  # save code in session

    # Send email
    try:
        send_mail(
            'Password Reset Code',
            f'Your password reset code is: {reset_code}',
            'sumariamariahshannen@gmail.com',  # from
            ['sumariamariahshannen@gmail.com'],  # to
            fail_silently=False,
        )
        print("DEBUG: Reset code sent:", reset_code)
        messages.success(request, 'A reset code has been sent to your email!')
    except Exception as e:
        print("DEBUG: Email failed:", e)
        messages.error(request, f'Failed to send reset code: {e}')

    # Redirect to verify code page
    return redirect('verify_reset_code')




# Step 2: Verify the reset code
def verify_reset_code(request):
    if request.method == 'POST':
        entered_code = request.POST.get('code')
        if entered_code == request.session.get('reset_code'):
            messages.success(request, 'Code verified. You can reset your password now.')
            return redirect('reset_password')
        else:
            messages.error(request, 'Invalid code. Please try again.')

    return render(request, 'verify_reset_code.html')


# Step 3: Reset password
def reset_password(request):
    if request.method == 'POST':
        new_password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if new_password != confirm_password:
            messages.error(request, 'Passwords do not match.')
        else:
            try:
                admin_user = User.objects.get(email='sumariamariahshannen@gmail.com')
                admin_user.set_password(new_password)
                admin_user.save()
                messages.success(request, 'Password reset successful.')
                # clear session code
                if 'reset_code' in request.session:
                    del request.session['reset_code']
                return redirect('login')
            except User.DoesNotExist:
                messages.error(request, 'Admin user not found.')

    return render(request, 'reset_password.html')


def admin_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("dashboard")  # make sure you have this URL in urls.py
        else:
            messages.error(request, "Invalid username or password")

    return render(request, "login.html")


from django.shortcuts import render

def dashboard(request):
    context = {
        'total_users': 15,
        'total_items': 120,
        'total_categories': 4,
        'total_borrowed': 35,
        'category_series': [40, 25, 20, 15],
        'category_labels': ['Sports Equipment', 'Chairs', 'Sound System', 'Others'],
        'borrowed_series': [30, 25, 18, 12, 10],
        'borrowed_labels': ['Basketball', 'Projector', 'Chairs', 'Speakers', 'Tables'],
        'available_percent': 71  # (total_items - total_borrowed)/total_items*100
    }
    return render(request, 'dashboard.html', context)



def inventory(request):
    # Get filters
    q = request.GET.get('q', '')
    category = request.GET.get('category', '')
    sort = request.GET.get('sort', 'newest')

    items = Item.objects.all()

    if q:
        items = items.filter(name__icontains=q)

    if category:
        items = items.filter(category=category)

    if sort == 'newest':
        items = items.order_by('-id')
    else:
        items = items.order_by('id')

    total_items = items.count()

    return render(request, 'inventory.html', {
        'items': items,
        'q': q,
        'category': category,
        'sort': sort,
        'total_items': total_items,
    })




def inventory_createitem(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        qty = request.POST.get('qty')
        category = request.POST.get('category')
        image = request.FILES.get('image')

        Item.objects.create(
            name=name,
            description=description,
            qty=qty,
            category=category,
            image=image
        )
        # after saving, redirect to inventory list
        return redirect('inventory') 

    return render(request, 'inventory_createitem.html')




def inventory_edit(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, 'Item updated successfully.')
            return redirect('inventory_list')
    else:
        form = ItemForm(instance=item)
    
    context = {'form': form, 'item': item}
    return render(request, 'inventory_edit.html', context)


# 3️⃣ Delete item
def inventory_delete(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    if request.method == 'POST':
        item.delete()
        messages.success(request, 'Item deleted successfully.')
        return redirect('inventory_list')
    # Optional: confirm deletion if GET request
    return render(request, 'inventory_confirm_delete.html', {'item': item})

def inventory_detail(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    return render(request, 'inventory_detail.html', {'item': item})

@csrf_exempt
def block_date(request, item_id):
    if request.method == "POST":
        item = Item.objects.get(id=item_id)
        data = json.loads(request.body)
        date_str = data.get("date")

        # Example: create a reservation/block for this date
        Reservation.objects.create(item=item, date=date_str, blocked=True)

        return JsonResponse({"status": "success"})
    return JsonResponse({"status": "error"}, status=400)


def verification(request):
    return render(request, 'verification.html')

def history_log(request):
    return render(request, 'history.html')

def damage_report(request):
    return render(request, 'damage.html')

def statistics(request):
    return render(request, 'statistics.html')

def change_pass(request):
    return render(request, 'change-password.html')

def list_of_users(request):
    return render(request, 'list_of_users.html')

def logout(request):
    return render(request, 'logout.html')