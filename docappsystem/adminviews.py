from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.decorators import login_required
from dasapp.models import Specialization, DoctorReg, Appointment, Page
from django.contrib import messages
from datetime import datetime


@login_required(login_url="/")
def ADMINHOME(request):
    doctor_count = DoctorReg.objects.all().count
    specialization_count = Specialization.objects.all().count
    context = {"doctor_count": doctor_count,"specialization_count": specialization_count,}
    return render(request, "admin/adminhome.html", context)

#for specialization
@login_required(login_url="/")
def SPECIALIZATION(request):
    if request.method == "POST":
        specializationname = request.POST.get("specializationname")
        
        # Check if the specialization already exists
        if Specialization.objects.filter(sname=specializationname).exists():
            messages.error(request, "Specialization already exists !")
            return redirect("add_specilizations")  # Redirect back to the form

        # If it doesn't exist, create and save the new specialization
        specialization = Specialization(sname=specializationname)
        specialization.save()
        messages.success(request, "Specialization added successfully!")
        return redirect("add_specilizations")

    return render(request, "admin/specialization.html")

@login_required(login_url="/")
def MANAGESPECIALIZATION(request):
    specialization = Specialization.objects.all()
    context = {"specialization": specialization,}
    return render(request, "admin/manage_specialization.html", context)


def DELETE_SPECIALIZATION(request, id):
    specialization = Specialization.objects.get(id=id)
    specialization.delete()
    messages.success(request, "Record Delete Succeesfully!!!")
    return redirect("manage_specilizations")

login_required(login_url="/")


def UPDATE_SPECIALIZATION(request, id):
    specialization = Specialization.objects.get(id=id)
    context = {"specialization": specialization,}
    return render(request, "admin/update_specialization.html", context)


login_required(login_url="/")


def UPDATE_SPECIALIZATION_DETAILS(request):
    if request.method == "POST":
        sep_id = request.POST.get("sep_id")
        sname = request.POST.get("sname")
        sepcialization = Specialization.objects.get(id=sep_id)
        sepcialization.sname = sname
        sepcialization.save()
        messages.success(request, "Your specialization detail has been updated successfully")
        return redirect("manage_specilizations")
    return render(request, "admin/update_specialization.html")


#for doctors
@login_required(login_url="/")
def DOCTOR(request):
    if request.method == "POST":
        doctorname = request.POST.get("doctorname")
        
        # Check if the doctor already exists
        if Doctor.objects.filter(dname=doctorname).exists():
            messages.error(request, "Doctor already exists !")
            return redirect("add_doctors")  # Redirect back to the form

        # If it doesn't exist, create and save the new specialization
        doctor = Doctor(dname=doctorname)
        doctor.save()
        messages.success(request, "Doctor added successfully!")
        return redirect("add_doctors")

    return render(request, "admin/doctor.html")

# @login_required(login_url="/")
# def MANAGEDOCTOR(request):
#     doctor = Doctor.objects.all()
#     context = {"doctor": doctor,}
#     return render(request, "admin/manage_doctor.html", context)


# def DELETE_DOCTOR(request, id):
#     doctor = Doctor.objectsdoctor.delete()
#     messages.success(request, "Record Delete Succeesfully!!!")
#     return redirect("manage_doctors")


def UPDATE_DOCTOR(request, id):
    doctor = Doctor.objects.get(id=id)
    context = {"doctor": doctor,}
    return render(request, "admin/update_doctor.html", context)


login_required(login_url="/")


def UPDATE_DOCTOR_DETAILS(request):
    if request.method == "POST":
        sep_id = request.POST.get("sep_id")
        dname = request.POST.get("dname")
        doctor = Doctor.objects.get(id=sep_id)
        doctor.dname = dname
        doctor.save()
        messages.success(request, "Your doctor detail has been updated successfully")
        return redirect("manage_doctors")
    return render(request, "admin/update_doctor.html")
# #end doctor


@login_required(login_url="/")
def DoctorList(request):
    doctorlist = DoctorReg.objects.all()
    context = {"doctorlist": doctorlist,}
    return render(request, "admin/doctor_list.html", context)


def ViewDoctorDetails(request, id):
    doctorlist1 = DoctorReg.objects.filter(id=id)
    context = {"doctorlist1": doctorlist1}
    return render(request, "admin/doctor-details.html", context)


def ViewDoctorAppointmentList(request, id):
    patientdetails = Appointment.objects.filter(doctor_id=id)
    context = {"patientdetails": patientdetails}
    return render(request, "admin/doctor_appointment_list.html", context)


def ViewPatientDetails(request, id):
    patientdetails = Appointment.objects.filter(id=id)
    context = {"patientdetails": patientdetails}
    return render(request, "admin/patient_appointment_details.html", context)


def Search_Doctor(request):
    if request.method == "GET":
        query = request.GET.get("query", "")
        if query:
            # Filter records where email or mobilenumber contains the query
            searchdoc = (
                DoctorReg.objects.filter(mobilenumber__icontains=query)
                | DoctorReg.objects.filter(admin__first_name__icontains=query)
                | DoctorReg.objects.filter(admin__last_name__icontains=query)
            )
            messages.info(request, "Search against " + query)
            return render(
                request,
                "admin/search-doctor.html",
                {"searchdoc": searchdoc, "query": query},
            )
        else:
            print("No Record Found")
            return render(request, "admin/search-doctor.html", {})


@login_required(login_url="/")
def WEBSITE_UPDATE(request):
    page = Page.objects.all()
    context = {
        "page": page,
    }
    return render(request, "admin/website.html", context)


@login_required(login_url="/")
def UPDATE_WEBSITE_DETAILS(request):
    if request.method == "POST":
        web_id = request.POST.get("web_id")
        pagetitle = request.POST["pagetitle"]
        address = request.POST["address"]
        aboutus = request.POST["aboutus"]
        email = request.POST["email"]
        mobilenumber = request.POST["mobilenumber"]
        page = Page.objects.get(id=web_id)
        page.pagetitle = pagetitle
        page.address = address
        page.aboutus = aboutus
        page.email = email
        page.mobilenumber = mobilenumber
        page.save()
        messages.success(request, "Your website detail has been updated successfully")
        return redirect("website_update")
    return render(request, "admin/website.html")
