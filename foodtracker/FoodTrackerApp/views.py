from django.shortcuts import render
from django.views.generic import (DetailView,UpdateView,DeleteView,CreateView)
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse,reverse_lazy
from django.http import HttpResponseRedirect
from FoodTrackerApp.models import User,Food,Category
from django.db import IntegrityError
from FoodTrackerApp.forms import FoodForm,CategoryForm
from django import forms
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages


# Create your views here.
def IndexView(request):
    foods = Food.objects.all()

    # Show 4 food items per page
    page = request.GET.get('page', 1)
    paginator = Paginator(foods, 4)
    try:
        pages = paginator.page(page)
    except PageNotAnInteger:
        pages = paginator.page(1)
    except EmptyPage:
        pages = paginator.page(paginator.num_pages)

    return render(request, 'index.html', {
        'foods': foods,
        'pages': pages,
        'title': 'Food List'
    })


def loginView(request):
    if request.method == 'POST':

        # Attempt to sign user in
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('index'))
        else:
            return render(request, 'login.html', {
                'message': 'Invalid username and/or password.',
                # 'categories': FoodCategory.objects.all()
            })
    else:
        return render(request, 'login.html')

@login_required
def logoutView(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

def registerView(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']

        # Ensure password matches confirmation
        password = request.POST['password']
        confirmation = request.POST['confirmation']
        if password != confirmation:
            return render(request, 'register.html', {
                'message': 'Passwords must match.'
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, 'register.html', {
                'message': 'Username already taken.',
            })
        login(request, user)
        return HttpResponseRedirect(reverse('index'))
    else:
        return render(request, 'register.html')
    

 ### add food items ###
@login_required
def addFoodView(request):
    '''
    It allows the user to add a new food item
    '''
    if request.method == 'POST':
        food_form = FoodForm(request.POST, request.FILES)

        if food_form.is_valid():
            new_food = food_form.save(commit=False)
            if 'food_img' in request.FILES:
                new_food.food_img = request.FILES['food_img']

            new_food.save()

            return render(request, 'food_add.html', {
                'food_form': FoodForm(),
                'success': True
            })

        else:
            return render(request, 'food_add.html', {'food_form': FoodForm()})

    else:
        return render(request, 'food_add.html', {
            'food_form': FoodForm(),
        })


## details food items
class FoodDetailView(DetailView): 
    context_object_name = "food_detail"
    model = Food
    template_name = 'food_detail.html'

## update food item
class FoodUpdateView(UpdateView):
    template_name = 'food_update.html'
    form_class = FoodForm
    model = Food
    redirect_field_name = 'food_detail.html'

## delete food item
class FoodDeleteView(LoginRequiredMixin,DeleteView):
    template_name='food_confirm_delete.html'
    model = Food
    success_url = reverse_lazy('index')

###Create category
class CreateCategoryView(LoginRequiredMixin,CreateView):
    login_url = '/login/'
    template_name='category_form.html'
    success_url = reverse_lazy('index')
    form_class = CategoryForm
    model=Category

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Category created successfully.')  # Add success message
        return response
