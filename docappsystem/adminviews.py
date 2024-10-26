from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.decorators import login_required
from dasapp.models import Specialization, DoctorReg, Appointment, Page, CustomUser
from django.contrib import messages
from datetime import datetime
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.shortcuts import render, redirect, get_object_or_404
from django.shortcuts import get_object_or_404, redirect, render


@login_required(login_url="/")
def ADMINHOME(request):
    doctor_count = DoctorReg.objects.all().count
    specialization_count = Specialization.objects.all().count
    context = {"doctor_count": doctor_count,"specialization_count": specialization_count,}
    return render(request, "admin/adminhome.html", context)

#for adding  new specialization

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

@login_required(login_url="/")

def UPDATE_SPECIALIZATION(request, id):
    specialization = Specialization.objects.get(id=id)
    context = {"specialization": specialization,}
    return render(request, "admin/update_specialization.html", context)


@login_required(login_url="/")
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



#adding new doctor
@login_required(login_url="/")
def add_doctor(request):
    if request.method == "POST":
        # Collect form data
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        username = request.POST.get("username")
        mobilenumber = request.POST.get("mobno")
        specialization_id = request.POST.get("specialization_id")
        password = request.POST.get("password")
        profile_pic = request.FILES.get("pic")

        # Check if user with this username or email already exists
        if CustomUser.objects.filter(username=username).exists() or CustomUser.objects.filter(email=email).exists():
            messages.error(request, "User with this username or email already exists!")
            return redirect("add_doctor")

        # Get specialization from the database
        try:
            specialization = Specialization.objects.get(id=specialization_id)
        except Specialization.DoesNotExist:
            messages.error(request, "Selected specialization does not exist!")
            return redirect("add_doctors")

        # Create the CustomUser and DoctorReg instances
        user = CustomUser.objects.create(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email,
            user_type="2",  # Set to "doc" type
            profile_pic=profile_pic,
            password=make_password(password)  # Encrypt the password
        )

        # Create the DoctorReg instance and link it to the CustomUser
        doctor = DoctorReg.objects.create(
            admin=user,
            mobilenumber=mobilenumber,
            specialization_id=specialization,
        )

        messages.success(request, "Doctor added successfully!")
        return redirect("add_doctor")

    # Fetch all specializations for the dropdown
    specialization = Specialization.objects.all()
    return render(request, "admin/doctor.html", {"specialization": specialization})


@login_required(login_url="/")
def MANAGEDOCTOR(request):
    doctor = DoctorReg.objects.all()
    context = {"doctor": doctor,}
    return render(request, "admin/manage_doctor.html", context)

@login_required(login_url="/")
def DELETE_DOCTOR(request, id):
    doctor = get_object_or_404(DoctorReg, id=id)  # Correctly fetch the doctor record

    if request.method == "GET":
        doctor.delete()  # Delete the doctor
        messages.success(request, "Doctor deleted successfully.")  # Success message
        # return redirect("admin/doctor_list.html")
        return redirect('doctor_list')


# @login_required(login_url="/")
# def DOCTOR_LIST(request):
#     doctors = DoctorReg.objects.all()  # Retrieve all doctors
#     return render(request, "admin/doctor_list.html", {"doctors": doctors})


@login_required(login_url="/")
def DOCTOR_LIST(request):
    doctorlist = DoctorReg.objects.all()
    context = {"doctorlist": doctorlist,}
    return render(request, "admin/doctor_list.html", context)


@login_required(login_url="/")
def UPDATE_DOCTOR(request, id):
    doctor = DoctorReg.objects.get(id=id)
    context = {"doctor": doctor,}
    return render(request, "admin/update_doctor.html", context)



@login_required(login_url="/")
def UPDATE_DOCTOR_DETAILS(request, sep_id):
    # Retrieve the doctor record from the database
    doctor = get_object_or_404(DoctorReg, id=sep_id)

    # Check if the form is submitted
    if request.method == "POST":
        # Get updated data from the form
        profile_pic = request.FILES.get("profile_pic")
        username = request.POST.get("username")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        password = request.POST.get("password")
        mobilenumber = request.POST.get("mobilenumber")
        print(f"Mobilenumber from form: {mobilenumber}")

        # Validate that mobilenumber is provided and not just whitespace
        if not mobilenumber or mobilenumber.strip() == "":
            messages.error(request, "Mobile number is required.")
            return render(request, "admin/update_doctor.html", {"doctor": doctor})


        # Update the doctor's details without modifying the specialization
        doctor.username = username
        doctor.first_name = first_name
        doctor.last_name = last_name
        doctor.email = email
        if profile_pic:
            doctor.profile_pic = profile_pic
        doctor.password = password  # Consider hashing this before saving!
        doctor.mobilenumber = mobilenumber

        # Save the updates to the database
        doctor.save()

        # Show a success message
        messages.success(request, "Doctor details updated successfully")
        
        # Redirect to the manage doctors page
        return redirect("doctor_list")
    
    # Render the form with the current doctor data
    return render(request, "admin/update_doctor.html", {
        "doctor": doctor,
    })


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
