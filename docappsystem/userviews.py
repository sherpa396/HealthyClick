from django.shortcuts import render, redirect, HttpResponse
from dasapp.models import *
import random
from datetime import datetime
from django.contrib import messages
from django.core.exceptions import ValidationError


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
        # Collect form data
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

        # Check if email or mobile number is already registered for the same doctor
        doc_instance = DoctorReg.objects.get(id=doctor_id)
        email_exists = Appointment.objects.filter(email=email, doctor_id=doc_instance).exists()
        mobile_exists = Appointment.objects.filter(mobilenumber=mobilenumber, doctor_id=doc_instance).exists()

        if email_exists:
            messages.error(request, "You have already registered with this doctor using this email.")
        if mobile_exists:
            messages.error(request, "You have already registered with this doctor using this mobile number.")

        # If there are error messages (for email or mobile), stop further processing
        if email_exists or mobile_exists:
            context = {
                "doctorview": doctorview,
                "page": page,
                "fullname": fullname,
                "email": email,
                "mobilenumber": mobilenumber,
                "address": address,
                "age": age,
                "gender": gender,
                "appointmenttype": appointmenttype,
                "date_of_appointment": date_of_appointment,
                "time_of_appointment": time_of_appointment,
                "doctor_id": doctor_id,
                "additional_msg": additional_msg,
            }
            return render(request, "appointment.html", context)

        # Validate the date
        try:
            appointment_date = datetime.strptime(date_of_appointment, "%Y-%m-%d").date()
            today_date = datetime.now().date()

            # Only show error if the selected date is in the past
            if appointment_date <= today_date:
                messages.error(request, "Please select a date in the future for your appointment")
                context = {
                    "doctorview": doctorview,
                    "page": page,
                    "fullname": fullname,
                    "email": email,
                    "mobilenumber": mobilenumber,
                    "address": address,
                    "age": age,
                    "gender": gender,
                    "appointmenttype": appointmenttype,
                    "date_of_appointment": date_of_appointment,
                    "time_of_appointment": time_of_appointment,
                    "doctor_id": doctor_id,
                    "additional_msg": additional_msg,
                }
                return render(request, "appointment.html", context)
        except ValueError:
            messages.error(request, "Invalid date format")
            context = {
                "doctorview": doctorview,
                "page": page,
                "fullname": fullname,
                "email": email,
                "mobilenumber": mobilenumber,
                "address": address,
                "age": age,
                "gender": gender,
                "appointmenttype": appointmenttype,
                "date_of_appointment": date_of_appointment,
                "time_of_appointment": time_of_appointment,
                "doctor_id": doctor_id,
                "additional_msg": additional_msg,
            }
            return render(request, "appointment.html", context)

        # Apply scheduling check using book_appointment function
        conflict_message = book_appointment(doctor_id, date_of_appointment, time_of_appointment)
        if conflict_message:  # If there's a scheduling conflict
            messages.warning(request, conflict_message)  # Show warning instead of redirecting
            context = {
                "doctorview": doctorview,
                "page": page,
                "fullname": fullname,
                "email": email,
                "mobilenumber": mobilenumber,
                "address": address,
                "age": age,
                "gender": gender,
                "appointmenttype": appointmenttype,
                "date_of_appointment": date_of_appointment,
                "time_of_appointment": time_of_appointment,
                "doctor_id": doctor_id,
                "additional_msg": additional_msg,
            }
            return render(request, "appointment.html", context)

        # If date is valid, create the new Appointment
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



def book_appointment(doctor_id, appointment_date, appointment_time):
    # Check if the doctor is available at the selected date and time
    if Appointment.objects.filter(doctor_id=doctor_id, date_of_appointment=appointment_date, time_of_appointment=appointment_time).exists():
        return "The doctor is already booked for this time slot. Please select another date or time."
    return None  # No conflict



def User_Search_Appointments(request):
    page = Page.objects.all()
    
    if request.method == "GET":
        query = request.GET.get('query', '')
        if query:
            # Filter records where fullname or Appointment Number contains the query
            patient = Appointment.objects.filter(fullname__icontains=query) | Appointment.objects.filter(appointmentnumber__icontains=query)
            messages.info(request, "Search against " + query)
            context = {'patient': patient, 'query': query, 'page': page}
            return render(request, 'search-appointment.html', context)
        else:
            print("No Record Found")
            context = {'page': page}
            return render(request, 'search-appointment.html', context)
    
    # If the request method is not GET
    context = {'page': page}
    return render(request, 'search-appointment.html', context)
def View_Appointment_Details(request,id):
    page = Page.objects.all()
    patientdetails=Appointment.objects.filter(id=id)
    context={'patientdetails':patientdetails,
    'page': page

    }

    return render(request,'user_appointment-details.html',context)
