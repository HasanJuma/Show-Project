from django.shortcuts import render, get_object_or_404, redirect
from .models import Show
from .forms import RatingForm, CommentForm
from django.contrib import messages

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm


# create your views here 

def home(request):
    return render(request, 'main_app/home.html')

def show_list(request):
    shows = Show.objects.all()
    return render(request, 'main_app/show_list.html', {'shows': shows})

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Show
from .forms import RatingForm, CommentForm

def show_detail(request, show_id):
    show = get_object_or_404(Show, id=show_id)

    # احضري كل التقييمات والتعليقات
    ratings = show.ratings.all()
    comments = show.comments.order_by('-created_at')  # الأحدث أولاً

    rating_form = RatingForm()
    comment_form = CommentForm()

    if request.method == 'POST':
        # إرسال تقييم
        if 'submit_rating' in request.POST:
            if request.user.is_authenticated:
                # منع التقييم المكرر
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

        # إرسال تعليق
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
            return redirect('home')   # أو أي صفحة تبينها بعد الدخول
        else:
            messages.error(request, "Invalid username or password.")
            return redirect('login')  # ← هنا كانت المشكلة: لا تكتبي 'login_view'
    return render(request, 'main_app/login.html')

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Registration successful. Please log in.")
            return redirect('login')  # ← بدل login_view
    else:
        form = RegisterForm()
    return render(request, 'main_app/register.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('home')

