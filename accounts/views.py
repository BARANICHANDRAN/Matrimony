from django.shortcuts import render, redirect
from .forms import CustomUserForm, ProfileForm, UserEditForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .models import Profile
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404


def index(request):
    return render(request, 'index.html')


def register(request):
    if request.method == 'POST':
        user_form = CustomUserForm(request.POST)
        profile_form = ProfileForm(request.POST, request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            login(request, user)
            return redirect('profile')
    else:
        user_form = CustomUserForm()
        profile_form = ProfileForm()
    return render(request, 'register.html', {'user_form': user_form, 'profile_form': profile_form})

@login_required
def profile(request):
    profile = Profile.objects.get(user=request.user)  # Get the profile for the logged-in user
    return render(request, 'profile.html', {'profile': profile})

@login_required
def profile_edit(request):
    profile = Profile.objects.get(user=request.user)
    if request.method == 'POST':
        user_form = UserEditForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('profile')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileForm(instance=profile)
    return render(request, 'profile_edit.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })

@login_required
def profile_list(request):
    user_profile = Profile.objects.get(user=request.user)

    # Base query with gender filter
    if user_profile.gender == 'M':
        profiles = Profile.objects.filter(gender='F').exclude(user=request.user)
    else:
        profiles = Profile.objects.filter(gender='M').exclude(user=request.user)

    # Apply location filter if provided
    location = request.GET.get('location')
    if location:
        profiles = profiles.filter(location__icontains=location)

    # Apply age filters if provided
    min_age = request.GET.get('min_age')
    max_age = request.GET.get('max_age')
    
    if min_age:
        profiles = profiles.filter(age__gte=min_age)
    if max_age:
        profiles = profiles.filter(age__lte=max_age)

    return render(request, 'profile_list.html', {'profiles': profiles})

@login_required
def profile_detail(request, pk):
    profile = get_object_or_404(Profile, pk=pk)

    if profile.user == request.user:
        return redirect('profile')

    return render(request, 'profile_detail.html', {'profile': profile})


@login_required
def delete_profile(request):
    if request.method == 'POST':
        try:
            profile = Profile.objects.get(user=request.user)
            profile.delete()
        except Profile.DoesNotExist:
            pass  

        user = request.user
        user.delete()
        return redirect('index')  

    return render(request, 'confirm_delete.html')