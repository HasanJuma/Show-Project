from django.shortcuts import render, get_object_or_404, redirect
from .models import Show , Profile
from .forms import RatingForm, CommentForm , ProfileForm
from django.contrib import messages

from django.contrib.auth import authenticate, login, logout , update_session_auth_hash
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm

# import 

from django.contrib.auth.forms import PasswordChangeForm

# create your views here 

def home(request):
    return render(request, 'main_app/home.html')

def show_list(request):
    shows = Show.objects.all()
    return render(request, 'main_app/show_list.html', {'shows': shows})


def show_detail(request, show_id):
    show = get_object_or_404(Show, id=show_id)

    # to get all comments & ratings
    ratings = show.ratings.all()
    comments = show.comments.order_by('-created_at')  # New first

    rating_form = RatingForm()
    comment_form = CommentForm()

    if request.method == 'POST':
        # to send rating 
        if 'submit_rating' in request.POST:
            if request.user.is_authenticated:
                # prevent rating again 
                existing = show.ratings.filter(user_name=request.user.username).first()
                if existing:
                    messages.warning(request, "You have already rated this show.")
                    return redirect('show_detail', show_id=show_id)

                rating_form = RatingForm(request.POST)
                if rating_form.is_valid():
                    rating = rating_form.save(commit=False)
                    rating.show = show
                    rating.user_name = request.user.username
                    rating.save()
                    messages.success(request, "Your rating has been added successfully.")
                    return redirect('show_detail', show_id=show_id)
                else:
                    messages.error(request, "Please provide a valid rating (1–5).")
            else:
                messages.warning(request, "You must be logged in to submit a rating.")
                return redirect('login')

        # Submit a cooment 
        elif 'submit_comment' in request.POST:
            if request.user.is_authenticated:
                comment_form = CommentForm(request.POST)
                if comment_form.is_valid():
                    comment = comment_form.save(commit=False)
                    comment.show = show
                    comment.user_name = request.user.username
                    comment.save()
                    messages.success(request, "Your comment has been posted.")
                    return redirect('show_detail', show_id=show_id)
                else:
                    messages.error(request, "Please write a valid comment.")
            else:
                messages.warning(request, "You must be logged in to comment.")
                return redirect('login')

    context = {
        'show': show,
        'ratings': ratings,
        'comments': comments,
        'rating_form': rating_form,
        'comment_form': comment_form,
    }
    return render(request, 'main_app/show_detail.html', context)


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')   
        else:
            messages.error(request, "Invalid username or password.")
            return redirect('login')  
    return render(request, 'main_app/login.html')

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Registration successful. Please log in.")
            return redirect('login')  
    else:
        form = RegisterForm()
    return render(request, 'main_app/register.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('home')


@login_required
def profile_view(request):
    profile, _ = Profile.objects.get_or_create(user=request.user)
    return render(request, 'main_app/profile.html', {
        'profile': profile
    })

# update profile & change password
@login_required
def profile_edit(request):
    profile, _ = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully.")
            return redirect('profile')  # profile display page after update
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = ProfileForm(instance=profile, user=request.user)

    return render(request, 'main_app/profile_edit.html', {'form': form})



@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()  # to save new passwrod
            update_session_auth_hash(request, user)  # stay login information
            messages.success(request, "Your password has been updated.")
            return redirect('home')  # OR redirect('change_password')
        else:
            messages.error(request, "Please fix the errors below.")
    else:
        form = PasswordChangeForm(request.user)

    return render(request, 'main_app/change_password.html', {'form': form})



