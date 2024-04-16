from django.contrib.auth.views import LoginView, PasswordResetView
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import SignupForm, DefaultersForm
from django.contrib.auth import login, authenticate
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.http import JsonResponse
import json
from .models import Defaulters

# Create your views here.
class CustomLoginView(LoginView):
    def form_valid(self, form):
        # Call the parent class's form_valid method
        super().form_valid(form)

        # Redirect to library dashboard
        return redirect('staff_home')
    
@login_required
def staff_home_view(request):    
    return render(request, 'staff_home.html')

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('staff_home')  
    else:
        form = SignupForm()
    return render(request, 'registration/signup.html', {'form': form})

class CustomPasswordResetView(PasswordResetView):
    email_template_name = 'registration/password_reset_email.html'    
    template_name = 'registration/password_reset_form.html'
    success_url = reverse_lazy('password_reset_done')

    def form_valid(self, form):        
        email = form.cleaned_data['email']
        if not User.objects.filter(email=email).exists():
            # Email doesn't exist in the database
            #error(self.request, 'This email is not registered.')
            return self.render_to_response(
                self.get_context_data(form=form, unregistered_email=True)
            )
        return super().form_valid(form)

@login_required
def newdefaulter(request):
    if request.method == 'POST':
        form = DefaultersForm(request.POST)
        if form.is_valid():
            form.save() 
            return JsonResponse({'success': True})
        else:
            # Form is not valid, return 'false'
            return JsonResponse({'success': False})
    else:
        form = DefaultersForm()

    return render(request, 'newdefaulter.html', {'form': form})

@login_required
def search_defaulter(request):
    return render(request, 'searchdefaulter.html')

@login_required
def search_for_defaulter(request):
    if request.method == 'POST':
        # Get the data from the request body
        data = json.loads(request.body.decode("utf-8"))
        search_query = data.get('q', '')
        search_field = data.get('field', 'name')

        # Determine the field to search based on the selected option
        if search_field == 'name':
            search_results = Defaulters.objects.filter(name__icontains=search_query)
        elif search_field == 'email':
            search_results = Defaulters.objects.filter(email__icontains=search_query)
        elif search_field == 'defaulter_id':
            search_results = Defaulters.objects.filter(defaulter_id__icontains=search_query)
        else:
            # If the selected field is not recognized, return an empty queryset
            search_results = Defaulters.objects.none()

        # Serialize the search results
        serialized_results = [{'id': defaulter.id, 'name': defaulter.name, 'email': defaulter.email,
                                'defaulter_id': defaulter.defaulter_id, 'location': defaulter.location,
                                'phone': defaulter.phone, 'outstanding_debt': defaulter.outstanding_debt,
                                } for defaulter in search_results]

        return JsonResponse({'results': serialized_results})
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)

@login_required
def edit_defaulter(request, defaulter_id):
    defaulter = get_object_or_404(Defaulters, pk=defaulter_id)
    
    if request.method == 'POST':
        form = DefaultersForm(request.POST, instance=defaulter)
        if form.is_valid():
            form.save()
            # Redirect to a success page or do something else
    else:
        form = DefaultersForm(instance=defaulter)
    
    return render(request, 'editdefaulter.html', {'form': form})

@login_required
def delete_defaulter(request, defaulter_id):
    # Get the book object
    defaulter = get_object_or_404(Defaulters, pk=defaulter_id)
    
    # Delete the book
    defaulter.delete()
    
    # Return a success response
    return JsonResponse({'success': True})

@login_required
def send_reminder_emails(request):
    defaulters = Defaulters.objects.filter(outstanding_debt__gt=0)  # Filter defaulters with outstanding debt
    for defaulter in defaulters:
        subject = f"Reminder: Outstanding Debt"
        message = f"Hello {defaulter.name},\n\nThis is a reminder that you have an outstanding debt of Ksh.{defaulter.outstanding_debt}.\n\nPlease make the payment at your earliest convenience.\n\nBest regards,\nKeysian Auctioneers"

        # Instead of sending actual emails, output to the console
        print("Sending email to:", defaulter.email)
        print("Subject:", subject)
        print("Message:", message)
        print("Email sent successfully\n")

    return render(request, 'emails_sent.html')  # Render a template indicating emails were sent

@login_required
def chatbot(request):
    return render(request, 'chat.html')