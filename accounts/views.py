from django.shortcuts import render, redirect
from django.contrib.auth.models import User, Group
from .forms import UserForm, GroupForm
from django.contrib.auth import login, authenticate
from .forms import CustomAuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt
from .authorization import Authorization

@login_required
@csrf_exempt
def user_list(request):
    users = User.objects.all().order_by('username')
    
    # Pagination
    paginator = Paginator(users, 20)  # Show 10 items per page
    page_number = request.GET.get('page')  # Get the current page number
    page_obj = paginator.get_page(page_number)  # Get the page object for the current page

    context = {
        'title' : 'List of Users',
        'page_obj' : page_obj
    }

    return render(request, 'accounts/user_list.html', context=context)


@login_required
def user_create(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            form.save_m2m()
            return redirect('user-list')
    else:
        form = UserForm()
    return render(request, 'accounts/user_form.html', {'form': form})



@login_required
@csrf_exempt
def group_list(request):

    # groups = Group.objects.all().values_list()
    groups = Group.objects.all().order_by('name')

    # Pagination
    paginator = Paginator(groups, 20)  # Show 10 items per page
    page_number = request.GET.get('page')  # Get the current page number
    page_obj = paginator.get_page(page_number)  # Get the page object for the current page

    # prepare the date to be rendered on HTML page
    context = {
        'title' : 'List of Groups',
        'page_obj' : page_obj
    }

    return render(request, 'accounts/group_list.html', context=context)



@login_required
def group_create(request):
    if request.method == 'POST':
        form = GroupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('group-list')
    else:
        form = GroupForm()
    return render(request, 'accounts/group_form.html', {'form': form})




@csrf_exempt
def login_view(request):

    if request.session.get('_auth_user_id'):
        return redirect('dashboard') 

    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)

                # if logged in successfully, fetch authorized menu and store it to sesssion
                try:
                    user_groups = user.groups.all()
                    menu_list = Authorization.objects.filter(groups__in=user_groups).values_list('menu', flat=True)
                    request.session['menu_list'] = list(menu_list)
                except Authorization.DoesNotExist:
                    request.session['menu_list'] = []

                return redirect('dashboard')  # Redirect to dashboard
    else:
        form = CustomAuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})



@login_required
@csrf_exempt
def dashboard_view(request):
    context = {
        'heading' : 'USDA Dashboard',
        'message' : 'Welcome to USDA Dashboard'
    }

    return render(request, 'common/dashboard.html', context=context)


def logout_view(request):
    logout(request)
    return redirect('login')