from django.contrib import admin
from django.urls import path
from . import views, adminviews, docviews, userviews
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path("admin/", admin.site.urls),
    path("base/", views.BASE, name="base"),
    path("login/", views.LOGIN, name="login"),
    path("doLogin", views.doLogin, name="doLogin"),
    path("doLogout", views.doLogout, name="logout"),
    path("userappointment/", userviews.create_appointment, name="appointment"),

    path("payment/", userviews.PAYMENT, name="payment"),
    
    # pdf  print section
    path('pdf_view/<int:id>/', views.invoice_view, name="pdf_view"),
    
    
    # admin panel
    path("Admin/AdminHome", adminviews.ADMINHOME, name="admin_home"),
    
    # specialization management
    path("Admin/Specialization", adminviews.SPECIALIZATION, name="add_specilizations"),
    path("Admin/ManageSpecialization", adminviews.MANAGESPECIALIZATION, name="manage_specilizations",),
    path("Admin/DeleteSpecialization/<str:id>", adminviews.DELETE_SPECIALIZATION, name="delete_specilizations",),
    path("UpdateSpecialization/<str:id>", adminviews.UPDATE_SPECIALIZATION, name="update_specilizations",),
    path("UPDATE_Specialization_DETAILS", adminviews.UPDATE_SPECIALIZATION_DETAILS, name="update_specilizations_details",),
    
    
    # doctor view management
    path("Admin/DoctorList", adminviews.DoctorList, name="viewdoctorlist"),
    path("Admin/ViewDoctorDetails/<str:id>", adminviews.ViewDoctorDetails, name="viewdoctordetails",),
    path("Admin/ViewDoctorAppointmentList/<str:id>", adminviews.ViewDoctorAppointmentList, name="viewdoctorappointmentlist",),
    path("Admin/ViewPatientDetails/<str:id>", adminviews.ViewPatientDetails, name="viewpatientdetails",),
    
    # doctor crud management
    path("Admin/Doctor", adminviews.add_doctor, name="add_doctor"),
    path("Admin/ManageDoctor", adminviews.MANAGEDOCTOR, name="manage_doctors",),
    path("Admin/DeleteDoctor/<str:id>", adminviews.DELETE_DOCTOR, name="delete_doctor",),
    path("Admin/UpdateDoctor/<str:id>", adminviews.UPDATE_DOCTOR, name="update_doctor",),
    path("Admin/DoctorList/", adminviews.DOCTOR_LIST, name="doctor_list"),

    path("Admin/UPDATE_Doctor_Details/<int:sep_id>/", adminviews.UPDATE_DOCTOR_DETAILS, name="update_doctor_details"),

    # path("Admin/UPDATE_Doctor_Details", adminviews.UPDATE_DOCTOR_DETAILS, name="update_doctor_details",),
    
    
    
    # searching registered doctor
    path("SearchDoctor", adminviews.Search_Doctor, name="search_doctor"),
   
    # Website Page
    path("Website/update", adminviews.WEBSITE_UPDATE, name="website_update"),
    path(
        "UPDATE_WEBSITE_DETAILS",
        adminviews.UPDATE_WEBSITE_DETAILS,
        name="update_website_details",
    ),
    
    # This is Doctor Panel
    path("docsignup/", docviews.DOCSIGNUP, name="docsignup"),
    path("Doctor/DocHome", docviews.DOCTORHOME, name="doctor_home"),
    path("Doctor/ViewAppointment", docviews.View_Appointment, name="view_appointment"),
    path(
        "DoctorPatientAppointmentDetails/<str:id>",
        docviews.Patient_Appointment_Details,
        name="patientappointmentdetails",
    ),
    path(
        "AppointmentDetailsRemark/Update",
        docviews.Patient_Appointment_Details_Remark,
        name="patient_appointment_details_remark",
    ),
    path(
        "DoctorPatientApprovedAppointment",
        docviews.Patient_Approved_Appointment,
        name="patientapprovedappointment",
    ),
    path(
        "DoctorPatientCancelledAppointment",
        docviews.Patient_Cancelled_Appointment,
        name="patientcancelledappointment",
    ),
    path(
        "DoctorPatientNewAppointment",
        docviews.Patient_New_Appointment,
        name="patientnewappointment",
    ),
    path(
        "DoctorPatientListApprovedAppointment",
        docviews.Patient_List_Approved_Appointment,
        name="patientlistappointment",
    ),
    path(
        "DoctorAppointmentList/<str:id>",
        docviews.DoctorAppointmentList,
        name="doctorappointmentlist",
    ),
    path(
        "PatientAppointmentPrescription",
        docviews.Patient_Appointment_Prescription,
        name="patientappointmentprescription",
    ),
    path(
        "PatientAppointmentCompleted",
        docviews.Patient_Appointment_Completed,
        name="patientappointmentcompleted",
    ),
    path("SearchAppointment", docviews.Search_Appointments, name="search_appointment"),
    
    # This is User Panel
    path("userbase/", userviews.USERBASE, name="userbase"),
    path("", userviews.Index, name="index"),
    path("userappointment/", userviews.create_appointment, name="appointment"),
    path(
        "User_SearchAppointment",
        userviews.User_Search_Appointments,
        name="user_search_appointment",
    ),
    path(
        "ViewAppointmentDetails/<str:id>/",
        userviews.View_Appointment_Details,
        name="viewappointmentdetails",
    ),

    # path for printing invoice
    path("ViewInvoice", views.invoice_view,  name="ViewInvoice"),
    
    #email path
    path("sendemails", views.send_email, name="send_email"),


    # profile path
    path("Profile", views.PROFILE, name="profile"),
    path("Profile/update", views.PROFILE_UPDATE, name="profile_update"),
    path("Password", views.CHANGE_PASSWORD, name="change_password"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
