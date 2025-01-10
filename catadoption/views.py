from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required

from datetime import date

from .forms import RegistrationForm, LoginForm, AdoptionProfileForm
from .models import Cat, AdoptionProfile, AdoptionRequest


# homepage
def index(request):
    return render (request, 'index.html', {'user': request.user})

# registration
def register(request):
    # prevent registered users from accessing
    if request.user.is_authenticated:
        messages.error (request, "You are already registered!")
        # redirect to homepage
        return redirect('/')
    # submitting registration from
    if request.method == 'POST':
        # the form also involves file upload
        form = RegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            # create new user from form data
            user = form.save()
            # log in user after registering
            login(request, user)
            return redirect('create_profile')
        else:
            return render(request, 'register.html', {'form': form})
    # return blank form if simply accessing the page
    else:
        form = RegistrationForm()
        return render(request, 'register.html', {'form': form})

# login
def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
                # get form data
                username = form.cleaned_data['username']
                password = form.cleaned_data['password']
                # attempt to authenticate the user with the data
                user = authenticate(request, username=username, password=password)
                if user is not None:
                    # if the user exists, log them in
                    login(request, user)
                    return redirect('/')
                # otherwise give error and reload the page for new input
                else:
                    messages.error(request, "Invalid Username or Password")
                    return render(request, 'login.html', {'form': form})
    else:
        form = LoginForm()
        return render(request, 'login.html', {'form': form})

# logout
@login_required
def user_logout(request):
    # log out user and display success message
    logout(request)
    messages.success(request, "You have successfully logged out.")
    return redirect('/')

# create profile
@login_required
def create_profile(request):
    try:
        # if the user already has a profile filled out, redirect them to view profile
        profile = request.user.adoption_profile
        messages.error(request, "Profile already exists!")
        return redirect('view_or_edit_profile')
    # otherwise generate adoption profile form and attempt to save upon completion
    except AdoptionProfile.DoesNotExist:
        if request.method == 'POST':
            form = AdoptionProfileForm(request.POST)
            if form.is_valid():
                # save form
                adoption_profile = form.save(commit=False)
                # assign to user
                adoption_profile.user = request.user
                # save to user
                adoption_profile.save()
                # redirect to view profile upon success
                messages.success(request,"Profile created!")
                return redirect('view_or_edit_profile')
            else:
                return render(request, 'create_profile.html', {'form': form})
        else:
            form = AdoptionProfileForm()
            return render(request, 'create_profile.html', {'form': form})

# view/edit profile
@login_required
def view_or_edit_profile(request):
    try:
        user = request.user
        profile = request.user.adoption_profile
    # if the user doesn't have a profile filled out redirect them to create one
    except AdoptionProfile.DoesNotExist:
        messages.error(request, "User profile has not been filled out.")
        return redirect('create_profile')
    # upon pressing submit:
    if request.method == 'POST':
        # fill in the user's existing profile with the new data
        form = AdoptionProfileForm(request.POST, instance=profile)
        if form.is_valid():
            # save form and reload the page with a success message
            form.save()
            messages.success(request, "Form saved")
            return redirect('view_or_edit_profile')
    else:
        # otherwise just get the user's profile form and display
        form = AdoptionProfileForm(instance=profile)
    return render(request, 'view_or_edit_profile.html', {'form':form, 'user': user})

# view cats (along with filtering search)
def view_cats(request):
    # fields that won't be used as filters (has_special_needs is a special case)
    to_exclude = ['name','photo', 'has_special_needs', 'id']
    field_list = {}
    # using the existing fields from the cat model
    for filter_field in Cat._meta.fields:
        if filter_field.name not in to_exclude:
            # create a dictionary from all non excluded fields and their choices
            field_list[filter_field.name] = {
                'verbose_name': filter_field.verbose_name,
                'choices': dict(filter_field.choices)
            }
    # if the user has applied filters
    if request.GET:
        selected_filters = {}
        for filter_field in field_list:
            # get the values for a particular filter field from the query
            values = request.GET.getlist(filter_field)
            # if values exist for that field
            if values:
                # create a dictionary for the selected filter and its values
                    selected_filters[filter_field + '__in'] = values
        # handle has_special_needs separately as it is a boolean
        has_special_needs = request.GET.get('has_special_needs')
        if has_special_needs is not None:
            # one extra step to get the value as a boolean
            selected_filters['has_special_needs'] = has_special_needs == 'True'
            # apply all filters to the list of cats
        cats = Cat.objects.filter(**selected_filters)
        if not cats:
            messages.error(request, "There are no cats meeting this criteria.")
    else:
        cats = Cat.objects.all()
        if not cats:
            messages.error(request, "There are currently no cats in the system.")
    # the filtered list of cats is passed to the template
    return render (request, 'cats.html', {'cats': cats, 'user': request.user, 'fields': field_list})

# create adoption request
@login_required
def create_adoption_request(request, cat_id):
    cats = Cat.objects.all()
    # error handling for if the cat being requested doesn't exist
    if cat_id not in [cat.id for cat in cats]:
        messages.error(request, "Cat does not exist!")
        redirect('view_cats')
    # otherwise get the cat with the provided id
    cat_to_adopt = Cat.objects.get(id=cat_id)
    # prevent the user from adopting a cat they have already requested for
    if AdoptionRequest.objects.filter(cat=cat_to_adopt, user = request.user).exists():
        messages.error(request, "You have already requested to adopt " + cat_to_adopt.name +"!")
        return redirect('cats')
    try:
        profile = request.user.adoption_profile
    except AdoptionProfile.DoesNotExist:
        # prevent user from adopting without a profile filled out
        messages.error(request, "You must fill out an adoption profile.")
        return redirect('create_profile')
    if request.method == 'POST':
        # create adoption request and display confirmation page
        adoption_request = AdoptionRequest.objects.create(cat=cat_to_adopt, user=request.user, status='Pending', date=date.today())
        return render (request, 'adoption_confirmation.html', {'cat': cat_to_adopt, 'adoption_request': adoption_request})
    else:
        return render (request, 'adopt.html',{'cat': cat_to_adopt})

# view adoption requests
@login_required
def view_adoption_requests(request):
    user = request.user
    adoption_requests = user.adoption_request.all()
    # display all adoption requests for the user, if there are none the html will display a message accordingly
    return render (request, 'adoption_requests.html', {'adoption_requests': adoption_requests})

# delete adoption requests
@login_required
def delete_adoption_request(request, adoption_request_id):
    # test if valid adoption request
    try:
        adoption_request = AdoptionRequest.objects.get(id=adoption_request_id)
    except AdoptionRequest.DoesNotExist:
        messages.error(request, "Request does not exist.")
        return redirect('adoption_requests')
    # prevent finalized adoption requests from being able to be deleted
    if adoption_request.status == 'Decision Made':
        messages.error(request, "This request is already finalized and cannot be cancelled.")
        return redirect('adoption_requests')
    if request.method == 'POST':
        # delete adoption request with success message, redirect to adoption_requests page
        adoption_request.delete()
        messages.success(request, "Request cancelled.")
        return redirect('adoption_requests')
    else:
        return render(request,'cancel_adoption.html', {'adoption_request': adoption_request})