# views.py
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from django.contrib.auth import login
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import LoginForm, userProfileForm



from django.contrib.auth import authenticate, login
from django.contrib import messages

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            
            try:
                profile = UserProfile.objects.get(user=user)
                # אם קיימים שם פרטי שם משפחה ואימייל
                if profile.first_name and profile.last_name and profile.email:
                    return redirect('home')  # יש פרופיל -> לדף הבית
                else:
                    return redirect('user_profile')  # חסרים פרטים -> לדף השלמת פרטים
            except UserProfile.DoesNotExist:
                # אין בכלל פרופיל => שולחים לדף השלמת פרטים
                return redirect('user_profile')
        else:
            messages.error(request, 'שם משתמש או סיסמה לא נכונים')

    return render(request, 'main/login.html')
from django.contrib import messages
from .models import UserProfile

@login_required(login_url='login')
def user_profile_view(request):
    user = request.user
    profile, created = UserProfile.objects.get_or_create(user=user)

    if request.method == 'POST':
        form = userProfileForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            profile.first_name = data['first_name']
            profile.last_name = data['last_name']
            profile.email = data['email']
            profile.phone_number = data.get('phone_number')
            profile.building_number = data.get('building_number')
            profile.apartment_number = data.get('apartment_number')
            profile.floor_number = data.get('floor_number')
            profile.city = data.get('city')
            profile.street = data.get('street')
            profile.postal_code = data.get('postal_code')
            profile.save()  # <--- פה נשמר לדאטהבייס
            messages.success(request, 'פרופיל המשתמש עודכן בהצלחה.')
            return redirect('home')
    else:
        form = userProfileForm(initial={
            'first_name': profile.first_name,
            'last_name': profile.last_name,
            'email': profile.email,
            'phone_number': profile.phone_number,
            'building_number': profile.building_number,
            'apartment_number': profile.apartment_number,
            'floor_number': profile.floor_number,
            'city': profile.city,
            'street': profile.street,
            'postal_code': profile.postal_code,
        })

    return render(request, 'main/user_profile.html', {'form': form})



from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import BookingForm, ContactForm
from .models import AvailableMeeting, BookedMeeting
from datetime import date
from datetime import date
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

import json
from datetime import date
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .models import PurchasedApartment
@login_required(login_url='login')
def home_view(request):
    if request.method == 'POST':
        if 'send_message' in request.POST:
            contact_form = ContactForm(request.POST)
            booking_form = BookingForm()
            if contact_form.is_valid():
                contact_form.save()
                return redirect('home')
    else:
        booking_form = BookingForm()
        contact_form = ContactForm()

    available_meetings = AvailableMeeting.objects.filter(is_booked=False, date__gte=date.today())

    meetings = []
    for m in available_meetings:
        if m.date.weekday() != 5:  # לא שבת
            meetings.append({
                'id': m.id,
                'date': m.date.isoformat(),
                'time': m.time.strftime('%H:%M'),
                'title': f"פגישה באתר {m.location} בשעה {m.time.strftime('%H:%M')}",
                'location': m.location,  # ⬅️ הוספה קריטית
                'color': '#ffc107'
            })

    existing_meeting = BookedMeeting.objects.filter(user=request.user).select_related('meeting').first()
    user_meeting_data = None
    if existing_meeting:
        m = existing_meeting.meeting
        user_meeting_data = {
            'id': m.id,
            'date': m.date.isoformat(),
            'time': m.time.strftime('%H:%M'),
            'title': f"✨ הפגישה שלך באתר {m.location} בשעה {m.time.strftime('%H:%M')}",
            'location': m.location,
            'color': '#ffa07a'
        }
    apartment = PurchasedApartment.objects.filter(user=request.user).first()
    try:
        user_profile = UserProfile.objects.get(user=request.user)
        full_name = f"{user_profile.first_name} {user_profile.last_name}".strip()
    except UserProfile.DoesNotExist:
        full_name = request.user.usernam
    if not full_name:
        full_name = request.user.username  # fallback אם לא הוגדר שם פרטי/משפחה
    meeting_info_html = None
    if existing_meeting:
        meeting_info_html = {
            'date': m.date.strftime('%d/%m/%Y'),
            'time': m.time.strftime('%H:%M'),
            'location': m.location
        }

    context = {
        'booking_form': booking_form,
        'meeting_info': meeting_info_html,
        'contact_form': contact_form,
        'meetings_json': json.dumps(meetings),
        'user_meeting_json': json.dumps(user_meeting_data) if user_meeting_data else 'null' ,
        'full_name': full_name,
        'apartment_location': f"{apartment.city}, {apartment.street} {apartment.building_number}, דירה {apartment.apartment_number}" if apartment else "לא נמצא מיקום" # 👈 JSON תקין ל-JS
    }
    return render(request, 'main/home.html', context)
from django.contrib.auth import get_user_model
# views.py
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
@csrf_exempt
def book_meeting_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        meeting_id = data.get('meeting_id')

        # בדיקה אם המשתמש כבר קבע פגישה
        if BookedMeeting.objects.filter(user=request.user).exists():
            return JsonResponse({'error': 'כבר קבעת פגישה. לא ניתן לקבוע פגישה נוספת.'}, status=400)

        try:
            meeting = AvailableMeeting.objects.get(id=meeting_id)

            if not meeting.is_booked:
                meeting.is_booked = True
                meeting.save()
                BookedMeeting.objects.create(user=request.user, meeting=meeting)
                return JsonResponse({
                    'status': 'success',
                    'date': meeting.date.isoformat(),
                    'time': meeting.time.strftime('%H:%M')
                })
            else:
                return JsonResponse({'error': 'פגישה זו כבר נתפסה.'}, status=400)

        except AvailableMeeting.DoesNotExist:
            return JsonResponse({'error': 'הפגישה אינה קיימת.'}, status=404)




from django.contrib.auth.decorators import login_required
from .forms import userProfileForm
from .models import UserProfile

@login_required
def edit_profile_view(request):
    user = request.user
    profile, created = UserProfile.objects.get_or_create(user=user)

    if request.method == 'POST':
        form = userProfileForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            profile.first_name = data['first_name']
            profile.last_name = data['last_name']
            profile.email = data['email']
            profile.phone_number = data.get('phone_number')
            profile.building_number = data.get('building_number')
            profile.apartment_number = data.get('apartment_number')
            profile.floor_number = data.get('floor_number')
            profile.city = data.get('city')
            profile.street = data.get('street')
            profile.postal_code = data.get('postal_code')
            profile.save()
            messages.success(request, 'הפרופיל עודכן בהצלחה!')
            return redirect('home')  # חוזר לבית אחרי עדכון
    else:
        form = userProfileForm(initial={
            'first_name': profile.first_name,
            'last_name': profile.last_name,
            'email': profile.email,
            'phone_number': profile.phone_number,
            'building_number': profile.building_number,
            'apartment_number': profile.apartment_number,
            'floor_number': profile.floor_number,
            'city': profile.city,
            'street': profile.street,
            'postal_code': profile.postal_code,
        })

    return render(request, 'main/edit_profile.html', {'form': form})


from django.utils.timezone import now
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages
from django.contrib.auth.models import User
from .models import BookedMeeting, AvailableMeeting,PurchasedApartment
from .forms import AvailableMeetingForm, CreateUserForm,CreateUserWithApartmentForm
  # ודא שהם קיימים!

@user_passes_test(lambda u: u.is_superuser)  # ⛔ כניסה רק למנהלים
def admin_dashboard_view(request):
    users = User.objects.all()
    future_bookings = BookedMeeting.objects.filter(meeting__date__gte=now().date()).order_by('meeting__date', 'meeting__time')
    available_meeting_form = AvailableMeetingForm()
    create_user_form = CreateUserWithApartmentForm()
    open_meetings = AvailableMeeting.objects.filter(is_booked=False, date__gte=now().date())
    user_selections = UserSelection.objects.all() 
    if request.method == 'POST':
        form_type = request.POST.get('form_type')

        if form_type == 'create_meeting':
            available_meeting_form = AvailableMeetingForm(request.POST)
            if available_meeting_form.is_valid():
                available_meeting_form.save()
                messages.success(request, "הפגישה החדשה נוספה בהצלחה.")
                return redirect('admin_dashboard')

        if form_type == 'create_user':
            create_user_form = CreateUserWithApartmentForm(request.POST)
            if create_user_form.is_valid():
                user = User.objects.create_user(
                    username=create_user_form.cleaned_data['username'],
                    password=create_user_form.cleaned_data['password'],
                )
                PurchasedApartment.objects.create(
                    user=user,
                    city=create_user_form.cleaned_data['city'],
                    street=create_user_form.cleaned_data['street'],
                    building_number=create_user_form.cleaned_data['building_number'],
                    floor_number=create_user_form.cleaned_data.get('floor_number'),
                    apartment_number=create_user_form.cleaned_data['apartment_number'],
                )
                messages.success(request, "המשתמש החדש נוסף בהצלחה עם דירה.")
                return redirect('admin_dashboard')



        elif form_type == 'delete_user':
            user_id = request.POST.get('user_id')
            User.objects.filter(id=user_id).delete()
            messages.success(request, "המשתמש נמחק בהצלחה.")
            return redirect('admin_dashboard')

        elif form_type == 'delete_meeting':
            meeting_id = request.POST.get('meeting_id')
            AvailableMeeting.objects.filter(id=meeting_id, is_booked=False).delete()
            messages.success(request, "הפגישה הפנויה נמחקה בהצלחה.")
            return redirect('admin_dashboard')
    context = {
        'users': users,
        'future_bookings': future_bookings,
        'available_meeting_form': available_meeting_form,
        'create_user_form': create_user_form,
        'open_meetings': open_meetings,
        'user_selections': user_selections,
    }
    return render(request, 'main/admin_dashboard.html', context)


from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import ProductCategory, ProductOption, UserSelection
from django.contrib import messages

# views.py
import os, csv
from django.conf import settings
from django.db import transaction, IntegrityError
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import ProductCategory, ProductOption, UserSelection


def _seed_products_from_csv_if_needed():
    """
    ממלא את הטבלאות ProductCategory/ProductOption מתוך main/data/selection.csv
    רק אם אין עדיין קטגוריות ב־DB. רץ אוטומטית בבקשה הראשונה לעמוד.
    """
    if ProductCategory.objects.exists():
        return  # כבר יש נתונים

    # נתיב לקובץ בתוך הפרויקט
    csv_path = os.path.join(settings.BASE_DIR, "main", "data", "products.csv")
    if not os.path.exists(csv_path):
        # אין קובץ – פשוט לא נזרעים נתונים, העמוד יישאר ריק
        return

    try:
        with open(csv_path, newline="", encoding="utf-8") as f, transaction.atomic():
            reader = csv.DictReader(f)
            if not reader.fieldnames:
                return

            # העמודה הראשונה 'לקוחות' לא רלוונטית לקטגוריות
            id_col = "לקוחות"
            category_cols = [c for c in reader.fieldnames if c and c.strip() != id_col]

            # צור קטגוריות
            cats = {
                col: ProductCategory.objects.get_or_create(name=col.strip())[0]
                for col in category_cols
            }

            # אסוף ערכים ייחודיים לכל קטגוריה
            values_by_cat = {col: set() for col in category_cols}
            for row in reader:
                for col in category_cols:
                    val = (row.get(col) or "").strip()
                    if val and val != "-":
                        values_by_cat[col].add(val)

            # צור אופציות
            for col, values in values_by_cat.items():
                cat = cats[col]
                for val in values:
                    ProductOption.objects.get_or_create(category=cat, name=val)

    except Exception as e:
        # לא מפילים את העמוד אם יש תקלה; פשוט לא ייטען כלום
        # אפשר לרשום ל-log אם יש לכם לוגר
        pass


@login_required
def product_selection_view(request):
    # זורעים נתונים פעם ראשונה אם צריך
    _seed_products_from_csv_if_needed()

    categories = ProductCategory.objects.prefetch_related('options').all()
    user_selection, created = UserSelection.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        selected_option_ids = []
        for category in categories:
            option_id = request.POST.get(f'category_{category.id}')
            if option_id:
                selected_option_ids.append(int(option_id))

        user_selection.selected_options.set(selected_option_ids)
        user_selection.save()
        messages.success(request, "הבחירות נשמרו בהצלחה!")
        return redirect('contract_preview_view')

    selected_ids = user_selection.selected_options.values_list('id', flat=True)

    return render(request, 'main/product_selection.html', {
        'categories': categories,
        'selected_ids': selected_ids,
    })


@login_required
def contract_preview_view(request):
    apartment = PurchasedApartment.objects.filter(user=request.user).first()
    user_selection = UserSelection.objects.get(user=request.user)
    selected_options = user_selection.selected_options.all()
    user_profile = UserProfile.objects.filter(user=request.user).first()

    context = {
        'selections': selected_options,
        'apartment_location': f"{apartment.city}, {apartment.street} {apartment.building_number}, דירה {apartment.apartment_number}" if apartment else "לא נמצא מיקום",
        'current_date': date.today().strftime('%d/%m/%y'),
        'user_profile': user_profile,
    }
    return render(request, 'main/contract.html', context)

