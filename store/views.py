from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from django.contrib.auth import login, logout
from django.views.generic.list import ListView
from django.views.generic.edit import FormView
from django.views.generic.detail import DetailView
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth.decorators import login_required

from .models import Product, Category


def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def register(request):
    return render(request, 'register.html')

class ProductList(ListView):
    model = Product
    template_name = 'home.html'
    context_object_name = 'products'

class LoginUserView(LoginView):
    template_name = 'login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('home')

@login_required
def logout_user(request):
    logout(request)
    return redirect('home')

class RegisterUser(FormView):
    template_name = 'register.html'
    form_class = UserCreationForm
    redirect_authenticate_user = True
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(RegisterUser, self).form_valid(form)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('home')
        return super(RegisterUser, self).get(*args, **kwargs)
    
class ProductDetailView(DetailView):
    model = Product
    template_name = 'product_detail.html'
    context_object_name = 'product'

def category_view(request, name):
    category = Category.objects.get(name=name)
    products = Product.objects.filter(category=category)
    return render(request, 'category.html', {'category': category, 'products': products})

