from django.contrib.auth import login, logout, authenticate  
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse

from django.utils.http import urlsafe_base64_encode
from django.db.models.query_utils import Q
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.contrib.auth.forms import PasswordResetForm
from django.template.loader import render_to_string


from authentication.models import User
from . import forms, models

#Page de connexion
def login_page(request):
    form = forms.LoginForm()
    message = ''
    if request.method == 'POST':
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
            )
            if user is not None:
                login(request, user)
                return redirect('dashbord')
            else:
                message = 'Identifiants invalides.'
                print(message)
    return render(
        request, 'authentication/login.html', context={'form': form, 'message': message})

#Page de déconnexion
@login_required
def logout_user(request):
    logout(request)
    return redirect('login')

#Création d'un nouvel utilisateur
def new_user_page(request):
    form = forms.NewUserForm()
    if request.method == 'POST':
        form = forms.NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect('login')
    return render(request, 'authentication/new_user.html', context={'form': form})

#Password reset
def password_reset_request(request):
	if request.method == "POST":
		password_reset_form = PasswordResetForm(request.POST)
		if password_reset_form.is_valid():
			data = password_reset_form.cleaned_data['email']
			associated_users = User.objects.filter(Q(email=data))
			if associated_users.exists():
				for user in associated_users:
					subject = "Demande de réinitialisation du mot de passe"
					email_template_name = "authentication/password_reset_email.txt"
					c = {
					"email":user.email,
					'domain':'karrodeko.fr',
					'site_name': 'CIFPE',
					"uid": urlsafe_base64_encode(force_bytes(user.pk)),
					"user": user,
					'token': default_token_generator.make_token(user),
					'protocol': 'http',
					}
					email = render_to_string(email_template_name, c)
					try:
						send_mail(subject, email, 'alexandre.boucher92@gmail.com' , [user.email], fail_silently=False)
					except BadHeaderError:
						return HttpResponse('Invalid header found.')
					return redirect ("/password_reset/done/")
	password_reset_form = PasswordResetForm()
	return render(request=request, template_name="authentication/password_reset.html", context={"password_reset_form":password_reset_form})
