from django.shortcuts import render, redirect, HttpResponse
from dasapp.models import *
import random
import re
from datetime import datetime
from django.contrib import messages
from django.core.exceptions import ValidationError



def USERBASE(request):
    return render(request, "userbase.html", context)

def PAYMENT(request):
    if request.method == "POST":
        patient_name = request.POST.get('patientname')
        amount = request.POST.get('amount')
        cardnumbers = request.POST.get('cardnumber')
        expirydate = request.POST.get('expirydate')
        cvv = request.POST.get('cvv')

        print('Patient Name: ', patient_name, '\nAmount: ', amount,
            '\nCard Numbers: ', cardnumbers, '\nExpiry Date: ', expirydate, '\nCVV: ', cvv)
    
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


# In-memory list to store appointment slots for quick conflict checks
appointments = []

def load_prebooked_appointments():
    # Load existing appointments into the in-memory list
    global appointments
    appointments = list(Appointment.objects.values("doctor_id", "date_of_appointment", "time_of_appointment"))

# Load appointments at startup
load_prebooked_appointments()

def book_appointment(doctor_id, appointment_date, appointment_time):
    # Check for conflicts in the in-memory list
    for appointment in appointments:
        if (appointment["doctor_id"] == doctor_id and
            appointment["date_of_appointment"] == appointment_date and
            appointment["time_of_appointment"] == appointment_time):
            return "The doctor is already booked for this time slot. Please select another date or time."

    # No conflict; add the appointment details to the in-memory list
    appointments.append({
        "doctor_id": doctor_id,
        "date_of_appointment": appointment_date,
        "time_of_appointment": appointment_time
    })
    return None



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
        
        
        # Check if a valid doctor is selected
        if doctor_id == "Choose Doctor" or not doctor_id.isdigit():
            messages.error(request, "Please select a valid doctor.")
            context = {
                "doctorview": doctorview,
                "page": page,
                "fullname": fullname,
                "email": email,
                "mobilenumber": mobilenumber,
                "date_of_appointment": date_of_appointment,
                "time_of_appointment": time_of_appointment,
            }
            return render(request, "appointment.html", context)

        # Convert doctor_id to integer after validation
        doctor_id = int(doctor_id)

        # Check if a user with the same email and phone number already has an appointment on the same date and doctor
        existing_appointments = Appointment.objects.filter(
            email=email,
            mobilenumber=mobilenumber,
            date_of_appointment=date_of_appointment,
            doctor_id=doctor_id
        )
        
        
        
        # Validate that date_of_appointment is greater than today's date
        try:
            appointment_date = datetime.strptime(date_of_appointment, '%Y-%m-%d').date()
            today_date = datetime.now().date()

            if appointment_date <= today_date:
                # If the appointment date is not in the future, display an error message
                messages.error(request, "Please select a date in the future for your appointment")
                return redirect('appointment')  # Redirect back to the appointment page
        except ValueError:
            # Handle invalid date format error
            messages.error(request, "Invalid date format")
            return redirect('appointment')  # Redirect back to the appointment page

        if existing_appointments.exists():
            messages.warning(request, "An appointment already exists for this email and phone number on the same date with the same doctor.")
            context = {
                "doctorview": doctorview,
                "page": page,
                "fullname": fullname,
                "email": email,
                "mobilenumber": mobilenumber,
                "date_of_appointment": date_of_appointment,
                "time_of_appointment": time_of_appointment,
            }
            return render(request, "appointment.html", context)

        # Check for scheduling conflicts
        conflict_message = book_appointment(doctor_id, date_of_appointment, time_of_appointment)
        if conflict_message:
            messages.warning(request, conflict_message)
            context = {
                "doctorview": doctorview,
                "page": page,
                "fullname": fullname,
                "email": email,
                "mobilenumber": mobilenumber,
                "date_of_appointment": date_of_appointment,
                "time_of_appointment": time_of_appointment,
            }
            return render(request, "appointment.html", context)

        # No conflict; create new appointment in the database
        try:
            new_appointment = Appointment.objects.create(
                appointmentnumber=appointmentnumber,
                fullname=fullname,
                email=email,
                mobilenumber=mobilenumber,
                address=address,
                age=age,
                gender=gender,
                appointmenttype=appointmenttype,
                date_of_appointment=date_of_appointment,
                time_of_appointment=time_of_appointment,
                doctor_id_id=doctor_id,
                additional_msg=additional_msg,
            )
            new_appointment.save()
            messages.success(request, "Your appointment request has been sent. We will contact you soon !!")

            # Update in-memory list with the new appointment
            appointments.append({
                "doctor_id": doctor_id,
                "date_of_appointment": date_of_appointment,
                "time_of_appointment": time_of_appointment
            })

        except Exception as e:
            messages.error(request, f"Error in booking appointment: {str(e)}")

        return redirect("appointment")

    context = {"doctorview": doctorview, "page": page}
    return render(request, "appointment.html", context)










def User_Search_Appointments(request):
    page = Page.objects.all()
    
    if request.method == "GET":
        query = request.GET.get('query', '')
        
        if query:
            # Check if the query is a valid email or 10-digit phone number
            email_pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'  # Regex for validating an email
            phone_pattern = r'^\d{10}$'  # Regex for exactly 10 digits
            
            # Validate email or phone number
            if re.match(email_pattern, query):  # If it's a valid email
                patient = Appointment.objects.filter(email=query)
                messages.info(request, "Search results for email: " + query)
            elif re.match(phone_pattern, query):  # If it's a valid 10-digit phone number
                patient = Appointment.objects.filter(mobilenumber=query)
                messages.info(request, "Search results for phone number: " + query)
            else:
                # If it doesn't match any pattern
                patient = None
                messages.error(request, "Please enter a valid email or 10-digit phone number.")
            
            context = {'patient': patient, 'query': query, 'page': page}
            return render(request, 'search-appointment.html', context)
        
        else:
            messages.error(request, "No query entered. Please provide an email or phone number.")
            context = {'page': page}
            return render(request, 'search-appointment.html', context)
    
    # If the request method is not GET
    context = {'page': page}
    return render(request, 'search-appointment.html', context)



def View_Appointment_Details(request, id):
    page = Page.objects.all()
    specialization = Specialization.objects.all()
    patientdetails = Appointment.objects.filter(id=id).select_related('doctor_id')  # Use select_related for optimization
    context = {
        'patientdetails': patientdetails,
        'page': page,
        'id': id,
    }

    return render(request, 'user_appointment-details.html', context)
