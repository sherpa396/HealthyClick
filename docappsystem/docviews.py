from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.decorators import login_required
from dasapp.models import DoctorReg, Specialization, CustomUser, Appointment
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from datetime import datetime
from django.core.paginator import Paginator


def DOCSIGNUP(request):
    specialization = Specialization.objects.all()
    if request.method == "POST":
        pic = request.FILES.get("pic")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        username = request.POST.get("username")
        email = request.POST.get("email")
        mobno = request.POST.get("mobno")
        specialization_id = request.POST.get("specialization_id")
        password = request.POST.get("password")

        if CustomUser.objects.filter(email=email).exists():
            messages.warning(request, "Email already exist !!")
            return redirect("docsignup")
        if CustomUser.objects.filter(username=username).exists():
            messages.warning(request, "Username already exist !!")
            return redirect("docsignup")
        else:
            user = CustomUser(
                first_name=first_name,
                last_name=last_name,
                username=username,
                email=email,
                user_type=2,
                profile_pic=pic,
            )
            user.set_password(password) # Set the user's password securely
            user.save() ## Save the user to the database
            spid = Specialization.objects.get(id=specialization_id)
            doctor = DoctorReg(
                admin=user,
                mobilenumber=mobno,
                specialization_id=spid,
            )
            doctor.save()
            messages.success(request, "Signup Successfull !!")
            return redirect("docsignup")

    context = {"specialization": specialization}

    return render(request, "doc/docreg.html", context)


@login_required(login_url="/")
def DOCTORHOME(request):
    doctor_admin = request.user
    doctor_reg = DoctorReg.objects.get(admin=doctor_admin)
    allaptcount = Appointment.objects.filter(doctor_id=doctor_reg).count
    newaptcount = Appointment.objects.filter(status="0", doctor_id=doctor_reg).count
    appaptcount = Appointment.objects.filter(
        status="Approved", doctor_id=doctor_reg
    ).count
    canaptcount = Appointment.objects.filter(
        status="Cancelled", doctor_id=doctor_reg #canaptcount = cancelled appointment count
    ).count
    comaptcount = Appointment.objects.filter(
        status="Completed", doctor_id=doctor_reg # comaptcount = completed appointment count
    ).count
    context = {
        "newaptcount": newaptcount,
        "allaptcount": allaptcount,
        "appaptcount": appaptcount,
        "canaptcount": canaptcount,
        "comaptcount": comaptcount,
    }
    return render(request, "doc/dochome.html", context)


def View_Appointment(request):
    try:
        doctor_admin = request.user
        doctor_reg = DoctorReg.objects.get(admin=doctor_admin)
        view_appointment = Appointment.objects.filter(doctor_id=doctor_reg)

        # Pagination for all appointment
        paginator = Paginator(view_appointment, 5)  # Show 5 appointments per page
        page = request.GET.get("page")
        try:
            view_appointment = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            view_appointment = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            view_appointment = paginator.page(paginator.num_pages)

        context = {"view_appointment": view_appointment}
    except Exception as e:
        # Handle exceptions, such as database errors, gracefully
        context = {"error_message": str(e)}

    return render(request, "doc/view_appointment.html", context)


def Patient_Appointment_Details(request, id):
    patientdetails = Appointment.objects.filter(id=id)
    context = {"patientdetails": patientdetails}

    return render(request, "doc/patient_appointment_details.html", context)


def Patient_Appointment_Details_Remark(request):
    if request.method == "POST":
        patient_id = request.POST.get("pat_id")
        remark = request.POST["remark"]
        status = request.POST["status"]
        patientaptdet = Appointment.objects.get(id=patient_id)
        patientaptdet.remark = remark
        patientaptdet.status = status
        patientaptdet.save()
        messages.success(request, "Status Update successfully !!")
        return redirect("view_appointment")
    return render(request, "doc/view_appointment.html", context)


def Patient_Approved_Appointment(request):
    doctor_admin = request.user
    doctor_reg = DoctorReg.objects.get(admin=doctor_admin)
    patientdetails1 = Appointment.objects.filter(status="Approved", doctor_id=doctor_reg)
    context = {"patientdetails1": patientdetails1}
    return render(request, "doc/patient_app_appointment.html", context)


def Patient_Cancelled_Appointment(request):
    doctor_admin = request.user
    doctor_reg = DoctorReg.objects.get(admin=doctor_admin)
    patientdetails1 = Appointment.objects.filter(
        status="Cancelled", doctor_id=doctor_reg
    )
    context = {"patientdetails1": patientdetails1}
    return render(request, "doc/patient_app_appointment.html", context)


def Patient_New_Appointment(request):
    doctor_admin = request.user
    doctor_reg = DoctorReg.objects.get(admin=doctor_admin)
    patientdetails1 = Appointment.objects.filter(status="0", doctor_id=doctor_reg)
    context = {"patientdetails1": patientdetails1}
    return render(request, "doc/patient_app_appointment.html", context)


def Patient_List_Approved_Appointment(request):
    doctor_admin = request.user
    doctor_reg = DoctorReg.objects.get(admin=doctor_admin)
    
    # Fetch all approved appointments for the doctor
    patientdetails1 = Appointment.objects.filter(status='Approved', doctor_id=doctor_reg)

    # Pagination logic
    paginator = Paginator(patientdetails1, 1)  # Show 10 appointments per page
    page_number = request.GET.get('page')  # Get the page number from the request
    patientdetails1_page = paginator.get_page(page_number)  # Get the appointments for the current page

    context = {
        'patientdetails1': patientdetails1_page,  # Pass the paginated appointments
        'paginator': paginator  # Pass the paginator to the template if needed
    }
    return render(request, 'doc/patient_list_app_appointment.html', context)


def DoctorAppointmentList(request, id):
    patientdetails = Appointment.objects.filter(id=id)
    context = {"patientdetails": patientdetails}

    return render(request, "doc/doctor_appointment_list_details.html", context)


def Patient_Appointment_Prescription(request):
    if request.method == "POST":
        patient_id = request.POST.get("pat_id")
        prescription = request.POST["prescription"]
        recommendedtest = request.POST["recommendedtest"]
        status = request.POST["status"]
        patientaptdet = Appointment.objects.get(id=patient_id)
        patientaptdet.prescription = prescription
        patientaptdet.recommendedtest = recommendedtest
        patientaptdet.status = status
        patientaptdet.save()
        messages.success(request, "Status Update successfully")
        return redirect("view_appointment")
    return render(request, "doc/patient_list_app_appointment.html", context)


def Patient_Appointment_Completed(request):
    try:
        # Get the logged-in user (doctor)
        doctor_admin = request.user
        doctor_reg = DoctorReg.objects.get(admin=doctor_admin)

        # Fetch completed patient appointments for this doctor
        patientdetails1 = Appointment.objects.filter(status="Completed", doctor_id=doctor_reg)

        # Pagination for completed appointments (e.g., 5 per page)
        paginator = Paginator(patientdetails1, 2)
        page = request.GET.get("page")

        try:
            # Get the requested page of appointments
            patientdetails1_paginated = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, show the first page
            patientdetails1_paginated = paginator.page(1)
        except EmptyPage:
            # If the page is out of range, show the last page
            patientdetails1_paginated = paginator.page(paginator.num_pages)

        # Add the paginated appointments to the context
        context = {"patientdetails1": patientdetails1_paginated}
    except Exception as e:
        # Handle any errors that might occur (e.g., database issues)
        context = {"error_message": str(e)}

    # Render the response with the context data
    return render(request, "doc/patient_list_app_appointment.html", context)


def Search_Appointments(request):
    doctor_admin = request.user
    doctor_reg = DoctorReg.objects.get(admin=doctor_admin)
    if request.method == "GET":
        query = request.GET.get("query", "")
        if query:
            # Filter records where fullname or Appointment Number contains the query
            patient = Appointment.objects.filter(
                fullname__icontains=query
            ) | Appointment.objects.filter(
                appointmentnumber__icontains=query
            ) & Appointment.objects.filter(
                doctor_id=doctor_reg
            )
            messages.success(request, "Search against " + query)
            return render(
                request,
                "doc/search-appointment.html",
                {"patient": patient, "query": query},
            )
        else:
            print("No Record Found")
            return render(request, "doc/search-appointment.html", {})

