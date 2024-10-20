from django.shortcuts import render, redirect, HttpResponse
from dasapp.EmailBackEnd import EmailBackEnd
from django.contrib.auth import logout, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from dasapp.models import CustomUser
from django.contrib.auth import get_user_model
# from .utils import send_email_to_client

# from django.http import JsonResponse
# from .models import Appointment


# def send_email(request):
#     send_email_to_client()
#     return redirect('/')

User = get_user_model()


def BASE(request):
    return render(request, "base.html")


def LOGIN(request):
    return render(request, "login.html")

def PAYMENT(request):
    return render(request, "payment.html")


def doLogout(request):
    logout(request)
    return redirect("login")


def doLogin(request):
    if request.method == "POST":
        user = EmailBackEnd.authenticate(
            request,
            username=request.POST.get("email"),
            password=request.POST.get("password"),
        )
        if user != None:
            login(request, user)
            user_type = user.user_type
            if user_type == "1":
                return redirect("admin_home")
            elif user_type == "2":
                return redirect("doctor_home")
            elif user_type == "3":
                return HttpResponse("This is User panel")

        else:
            messages.error(request, "Email or Password is not valid")
            return redirect("login")
    else:
        messages.error(request, "Email or Password is not valid")
        return redirect("login")


login_required(login_url="/")


def PROFILE(request):
    user = CustomUser.objects.get(id=request.user.id)
    context = {
        "user": user,
    }
    return render(request, "profile.html", context)


@login_required(login_url="/")
def PROFILE_UPDATE(request):
    if request.method == "POST":
        profile_pic = request.FILES.get("profile_pic")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        username = request.POST.get("username")
        print(profile_pic)

        try:
            customuser = CustomUser.objects.get(id=request.user.id)
            customuser.first_name = first_name
            customuser.last_name = last_name

            if profile_pic != None and profile_pic != "":
                customuser.profile_pic = profile_pic
            customuser.save()
            messages.success(request, "Your profile has been updated successfully")
            return redirect("profile")

        except:
            messages.error(request, "Your profile updation has been failed")
    return render(request, "profile.html")


def CHANGE_PASSWORD(request):
    context = {}
    ch = User.objects.filter(id=request.user.id)

    if len(ch) > 0:
        data = User.objects.get(id=request.user.id)
        context["data"]: data
    if request.method == "POST":
        current = request.POST["cpwd"]
        new_pas = request.POST["npwd"]
        user = User.objects.get(id=request.user.id)
        un = user.username
        check = user.check_password(current)
        if check == True:
            user.set_password(new_pas)
            user.save()
            messages.success(request, "Password Change  Succeesfully!!!")
            user = User.objects.get(username=un)
            login(request, user)
        else:
            messages.success(request, "Current Password wrong!!!")
            return redirect("change_password")
    return render(request, "change-password.html")



# def check_availability(request):
#     date = request.GET.get('date')
#     time_slot = request.GET.get('time_slot')
    
#     if Appointment.objects.filter(date=date, time_slot=time_slot).exists():
#         return JsonResponse({'available': False})
    
#     return JsonResponse({'available': True})


from django.shortcuts import render
from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from django.views import View
from xhtml2pdf import pisa

def render_to_pdf(template_src, context_dict={}):
	template = get_template(template_src)
	html  = template.render(context_dict)
	result = BytesIO()
	pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
	if not pdf.err:
		return HttpResponse(result.getvalue(), content_type='application/pdf')
	return None


data = {
	# "website": "HealthyClick - A web based doctor appointment system",
	"address": "Bouddha - 06, Kathmandu, Nepal",
	"phone": "+977-9841123463",
	"email": "healthyclickinfo@email.com",
	}

#Opens up page as PDF
class ViewPDF(View):
	def get(self, request, *args, **kwargs):

		pdf = render_to_pdf('pdf_template.html', data)
		return HttpResponse(pdf, content_type='application/pdf')


#Automaticly downloads to PDF file
class DownloadPDF(View):
	def get(self, request, *args, **kwargs):
		
		pdf = render_to_pdf('pdf_template.html', data)

		response = HttpResponse(pdf, content_type='application/pdf')
		filename = "Invoice_%s.pdf" %("12341231")
		content = "attachment; filename='%s'" %(filename)
		response['Content-Disposition'] = content
		return response

def index(request):
	context = {}
	return render(request, 'index.html', context)