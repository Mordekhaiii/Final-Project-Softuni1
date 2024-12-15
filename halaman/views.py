import profile

from django.shortcuts import render,HttpResponse, redirect
from django.contrib.auth.forms import UserCreationForm
from halaman.forms import CreateUserForm
import logging
from .forms import EditProfileForm
from .models import UserProfile
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib import messages



@login_required
def home(request):
    return render(request, 'home.html', {
        'user': request.user,
    })


logger = logging.getLogger(__name__)
# Create your views here.
def home(request):
    logger.info("Home view accessed")
    return render(request, 'home.html')

from django.shortcuts import render

def home(request):
    return render(request, 'welcome_popup.html')

# Update Profile
from .forms import UserUpdateForm, CustomPasswordChangeForm
from django.contrib.auth.forms import PasswordChangeForm

@login_required
def update_user_profile(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        password_form = CustomPasswordChangeForm(user=request.user, data=request.POST)

        if user_form.is_valid() and password_form.is_valid():
            # Simpan perubahan username dan email
            user_form.save()
            # Simpan perubahan password
            password_form.save()
            # Perbarui sesi pengguna
            update_session_auth_hash(request, password_form.user)

            messages.success(request, 'Profil berhasil diperbarui!')
            return redirect('update_profile')
        else:
            messages.error(request, 'Terjadi kesalahan. Silakan periksa form Anda.')
    else:
        user_form = UserUpdateForm(instance=request.user)
        password_form = CustomPasswordChangeForm(user=request.user)

    return render(request, 'accounts/change_password.html', {
        'user_form': user_form,
        'password_form': password_form,
    })

# Timestap setiap file
from django.utils.timezone import now

# Jika CSSnya tidak berubah saya pakai ini dibelakangnya
def contact_view(request):
    return render(request, 'contact.html', {'timestamp': now().timestamp()})

def home_view(request):
    return render(request, 'home.html', {'timestamp': now().timestamp()})


def registerPage(request):
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {form.cleaned_data["username"]}')

            return redirect('login')

    context = {'form' :form}
    return render(request, 'accounts/register.html', context)

def loginPage(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=request.POST.get('username'), password=request.POST.get('password'))

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Username or password incorrect')

    context = {}
    return render(request, 'accounts/login.html', context)

def profilePage(request):
    if not request.user.is_authenticated:
        messages.info(request, "You need to log in to view your profile.")
        return redirect('login')

    # Ambil profil pengguna yang sedang login (dari UserProfile)
    profile = UserProfile.objects.filter(user=request.user).first()

    context = {
        'user': request.user,
        'profile': profile  # Tambahkan profil pengguna ke context
    }
    return render(request, 'accounts/profile.html', context)

def logoutUser(request):
    logout(request)
    messages.success(request, "You have successfully logged out.")
    return redirect('home')


@login_required
def profile_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=request.POST.get('username'), password=request.POST.get('password'))

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Username or password incorrect')

    context = {}
    return render(request, 'home.html', context)

@login_required
def profile_view(request):
    user_profile = UserProfile.objects.get(user=request.user)
    return render(request, 'accounts/profile.html', {'user_profile': user_profile})


@login_required
def profilePage(request):
    if not request.user.is_authenticated:
        messages.info(request, "You need to log in to view your profile.")
        return redirect('login')

    # Ambil profil pengguna yang sedang login
    profile = UserProfile.objects.filter(user=request.user).first()

    # Jika nama kosong, tampilkan 'Unknown'
    first_name = request.user.first_name if request.user.first_name else "Unknown"
    last_name = request.user.last_name if request.user.last_name else ""

    context = {
        'user': request.user,
        'profile': profile,
        'full_name': f"{first_name} {last_name}".strip(),  # Gabungkan nama depan dan belakang
    }
    return render(request, 'accounts/profile.html', context)


@login_required
def edit_user_profile(request):
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        user_profile.user.first_name = request.POST.get("name")
        user_profile.phone_number = request.POST.get("phone_number")
        user_profile.address = request.POST.get("address")
        user_profile.age = request.POST.get("age")

        if 'profile_picture' in request.FILES:
            user_profile.profile_picture = request.FILES['profile_picture']

        user_profile.user.save()
        user_profile.save()

        return redirect('profile')  # Ganti 'profile' dengan nama URL untuk halaman profil

    return render(request, 'accounts/edit_profile.html', {'user_profile': user_profile})

def contact(request):
    return render(request, 'contact.html')


# Cekout



