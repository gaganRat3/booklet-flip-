from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from .models import FlipBook, BookView


def get_client_ip(request):
    """Get client IP address"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def login_view(request):
    """User login view"""
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome back, {username}!")
                return redirect('home')
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    
    return render(request, 'books/login.html', {'form': form})


def logout_view(request):
    """User logout view"""
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect('login')


@login_required
def home_view(request):
    """Home page - list all flipbooks"""
    books = FlipBook.objects.filter(is_published=True)
    return render(request, 'books/home.html', {'books': books})


@login_required
def flipbook_view(request, book_id):
    """View individual flipbook"""
    book = get_object_or_404(FlipBook, id=book_id, is_published=True)
    
    # Track view
    BookView.objects.create(
        book=book,
        user=request.user if request.user.is_authenticated else None,
        ip_address=get_client_ip(request)
    )
    
    # Get all page URLs
    pages = book.get_pages()
    
    context = {
        'book': book,
        'pages': pages,
        'total_pages': book.total_pages,
    }
    
    return render(request, 'books/flipbook.html', context)
