from django.shortcuts import render, redirect, HttpResponse
from dasapp.models import *
import random
from datetime import datetime
from django.contrib import messages
# from .utils import send_email_to_client
# from .models import Payment
from django.core.exceptions import ValidationError
from datetime import datetime


# def send_email(request):
#     send_email_to_client()
#     return redirect('/')


# def PAYMENT(request):
#     return render(request, "payment.html")

def USERBASE(request):
    return render(request, "userbase.html", context)

def PAYMENT(request):
    if request.method == "POST":
        patient_name = request.POST.get('patientname')
        amount = request.POST.get('amount')
        cardnumbers = request.POST.get('cardnumbers')
        expirydate = request.POST.get('expirydate')
        cvv = request.POST.get('cvv')
    
    # Save data to db and display a success message
        payment_details = Payment(
                patient_name=patient_name,
                amount=amount,
                cardnumbers=cardnumbers,
                expirydate=expirydate,
                cvv=cvv,
            )
        payment_details.save()
        
        messages.success(request, "Payment Successful !!")
        return redirect("appointment")

        
def Index(request):
    doctorview = DoctorReg.objects.all()
    page = Page.objects.all()

    context = {
        "doctorview": doctorview,
        "page": page,
    }
    return render(request, "index.html", context)


def create_appointment(request):
    doctorview = DoctorReg.objects.all()
    page = Page.objects.all()

    if request.method == "POST":
        appointmentnumber = random.randint(100000000, 999999999)
        fullname = request.POST.get("fullname")
        email = request.POST.get("email")
        mobilenumber = request.POST.get("mobilenumber")
        address = request.POST.get("address")
        age = request.POST.get("age")
        gender = request.POST.get("gender")
        appointmenttype = request.POST.get("appointmenttype")
        date_of_appointment = request.POST.get("date_of_appointment")
        time_of_appointment = request.POST.get("time_of_appointment")
        doctor_id = request.POST.get("doctor_id")
        additional_msg = request.POST.get("additional_msg")
        
        # Check if email or mobile number is already in use
        email_exists = Appointment.objects.filter(email=email).exists()
        mobile_exists = Appointment.objects.filter(mobilenumber=mobilenumber).exists()

        if email_exists:
            messages.error(request, "This email is already registered.")
        if mobile_exists:
            messages.error(request, "This mobile number is already registered.")
        
        # If there are error messages (for email or mobile), stop further processing
        if email_exists or mobile_exists:
            return redirect("appointment")

        # Validate the date
        try:
            appointment_date = datetime.strptime(date_of_appointment, "%Y-%m-%d").date()
            today_date = datetime.now().date()

            # Only show error if the selected date is in the past
            if appointment_date <= today_date:
                messages.error(request, "Please select a date in the future for your appointment")
                return redirect("appointment")
        except ValueError:
            messages.error(request, "Invalid date format")
            return redirect("appointment")

        # If date is valid, create the new Appointment
        doc_instance = DoctorReg.objects.get(id=doctor_id)
        appointmentdetails = Appointment.objects.create(
            appointmentnumber=appointmentnumber,
            fullname=fullname,
            email=email,
            address=address,
            age=age,
            gender=gender,
            appointmenttype=appointmenttype,
            mobilenumber=mobilenumber,
            date_of_appointment=date_of_appointment,
            time_of_appointment=time_of_appointment,
            doctor_id=doc_instance,
            additional_msg=additional_msg,
        )

        messages.success(request, "Your Appointment Request Has Been Sent. We Will Contact You Soon")
        return redirect("appointment")

    context = {"doctorview": doctorview, "page": page}
    return render(request, "appointment.html", context)


def User_Search_Appointments(request):
    page = Page.objects.all()

    if request.method == "GET":
        query = request.GET.get("query", "")
        if query:
            # Filter records where fullname or Appointment Number contains the query
            patient = Appointment.objects.filter(
                fullname__icontains=query
            ) | Appointment.objects.filter(appointmentnumber__icontains=query)
            messages.info(request, "Search against " + query)
            context = {"patient": patient, "query": query, "page": page}
            return render(request, "search-appointment.html", context)
        else:
            print("No Record Found")
            context = {"page": page}
            return render(request, "search-appointment.html", context)

    # If the request method is not GET
    context = {"page": page}
    return render(request, "search-appointment.html", context)


def View_Appointment_Details(request, id):
    page = Page.objects.all()
    patientdetails = Appointment.objects.filter(id=id)
    context = {"patientdetails": patientdetails, "page": page}

    return render(request, "user_appointment-details.html", context)


def invoice_view(request, id):
    # Fetch patient details based on the provided patient_id
    patient_details = Appointment.objects.get(id=id)
    
    context = {
        'doctor_remarks': patient_details.remark,
        'prescribed_medicine': patient_details.prescription,  # Adjust based on your model
        'recommended_test': patient_details.recommendedtest,  # Adjust based on your model
        'doctor_name': patient_details.fullname,  # Adjust based on your model
    }
    
    return render(request, 'pdf_template.html', context)