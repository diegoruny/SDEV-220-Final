from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login


# Create your views here.
# def register(request):
#     """New user registration"""
#     if request.method == 'POST':
#         form = UserCreationForm()
#     else:
#         form = UserCreationForm(request.POST)
#         if form.is_valid():
#             new_user = form.save()
#             #Log the user in and redirect to product_list page
#             login(request, new_user)
#             return redirect('shop:product_list')
    
#     #Blank/error form
#     context = {'form': form}
#     return render(request, 'registration/register.html', context)

def register(request):
    form = UserCreationForm()
    """New user registration"""
    if request.method == 'POST':
        
    
        form = UserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            #Log the user in and redirect to product_list page
            login(request, new_user)
            return redirect('shop:product_list')
    
    #Blank/error form
    context = {'form': form}
    return render(request, 'registration/register.html', context)
