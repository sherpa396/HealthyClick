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

        print('Patient Name: ', patient_name, '\nAmount: ', amount, '\nCard Numbers: ', cardnumbers, '\nExpiry Date: ', expirydate, '\nCVV: ', cvv)
    
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


import sqlite3

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

        # Check for scheduling conflicts
        conflict_message = book_appointment(date_of_appointment, time_of_appointment)
        if conflict_message:
            messages.warning(request, conflict_message)
            context = {
                # "doctorview": doctorview,
                # "page": page,
                "fullname": fullname,
                "email": email,
                "mobilenumber": mobilenumber,
                # "address": address,
                # "age": age,
                # "gender": gender,
                # "appointmenttype": appointmenttype,
                "date_of_appointment": date_of_appointment,
                "time_of_appointment": time_of_appointment,
                # "doctor_id": doctor_id,
                # "additional_msg": additional_msg,
            }
            return render(request, "appointment.html", context)

        # If no conflict, insert the new appointment
        try:
            conn = sqlite3.connect('db.sqlite3')  # Connect to your database
            cursor = conn.cursor()
            cursor.execute('''INSERT INTO dasapp_appointment
                            (appointmentnumber, fullname, email, mobilenumber, address, age, gender, appointmenttype,
                            date_of_appointment, time_of_appointment, additional_msg)
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                           (appointmentnumber, fullname, email, mobilenumber, address, age, gender, appointmenttype,
                            date_of_appointment, time_of_appointment, additional_msg))
            conn.commit()
            messages.success(request, "Your Appointment Request Has Been Sent. We Will Contact You Soon")
        except Exception as e:
            messages.error(request, f"Error in booking appointment: {str(e)}")
        finally:
            conn.close()

        return redirect("appointment")

    context = {"doctorview": doctorview, "page": page}
    return render(request, "appointment.html", context)

def book_appointment(doctor_id, appointment_date, appointment_time):
    try:
        conn = sqlite3.connect('db.sqlite3')
        cursor = conn.cursor()
        cursor.execute('''SELECT COUNT(*) FROM dasapp_appointment
                          WHERE doctor_id = ? AND date_of_appointment = ? AND time_of_appointment = ?''',
                       (doctor_id, appointment_date, appointment_time))
        conflict_exists = cursor.fetchone()[0] > 0
    except Exception as e:
        return f"Error checking appointment availability: {str(e)}"
    finally:
        conn.close()

    if conflict_exists:
        return "The doctor is already booked for this time slot. Please select another date or time."
    return None  # No conflict



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



def View_Appointment_Details(request,id):
    page = Page.objects.all()
    patientdetails=Appointment.objects.filter(id=id)
    context={'patientdetails':patientdetails,
    'page': page,
    'id': id,

    }

    return render(request,'user_appointment-details.html',context)

