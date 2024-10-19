## This project is for educational purpose only.

## Programming Language used:
1) Python
2) JS

## Database
1) SQLite

## Frontend
1) HTML
2) CSS

## Version Control
1) Git
2) Github

## creating requirement text
=> python freeze > requirements.txt

#installing requirement text
=> pip install -r requirements.txt


## Functional Description

* Secure Login Authentication (Signup and then Login).
* Emergency Registration & Online OPD Appointment.
* Medical Lab Report of Present Diagnosis
* Automatic expenses calculator for medicines prescribed in form of Invoice type (view/download).
* Admin access for proper management of the whole system.
* COVID vaccine tracking, availability and appointments.*
* Video/Normal Call and chatting facility for COVID patients surveillance.
* Medical History of the Patient*
* Feedback System for Patients.

* ## Admin

* Signup their account. Then login (Approval required by other admins, only then can Admin login).
* Can view/approve doctor (approve those doctor who applied for job in their hospital).
* Can admit/view/approve/book appointment patient.
* Can Generate/Download Invoice pdf (Generate Invoice according to medicine cost, room charge, doctor charge and other charge).
* Can view/book/approve appointment (approve those appointments which is requested by patient).



## Doctor
* Apply for job in hospital. Then login (Approval required by hospital admin, only then can the doctor login).
* Can only view their patient details (symptoms, name) assigned to that doctor.
* Can view their patient list.
* Can generate Video Calling Link with Patients.
* Can view their appointments/admit details.


## Patient
* Create account for admit in hospital. Then login (Approval required by hospital admin, only then can patientlogin).
* Can view assigned doctor's details like ( specialization, mobile, address).
* Can view their booked appointment status (pending/confirmed by admin).
* Can book appointments.(approval required by admin).
* Can view/download Invoice pdf (Only when that patient is discharged by admin).


## Problem Modules
* Module 1: Creation of Basic outline structure of the Project (Static files generation, linking with Backend,etc)
* Module 2: Almost completion of front-end part, Form Creations,etc.
* Module 3: Database linking of app & completion of left-over Backend Functionalities.
* Module 4: Testing, Deployment & Hosting on a Web Server.

## HOW TO RUN THIS PROJECT

The website has been hosted at

To run the program offline, follow the following steps:
* Install Python(3.7.6) (Don't Forget to Tick Add to Path while installing Python).
* Open Terminal and Execute Following Commands :
    ```
    pip install django
    pip install django-widget-tweaks
    pip install xhtml2pdf
    ```

* Download this project zip folder and extract it
* Move to project folder in terminal. Then run following commands :

Command for Window PC
   ```
    py manage.py makemigrations
    py manage.py migrate
    py manage.py runserver
   ```

  
* Now enter following URL in Your Browser Installed On Your Pc

    ```http://127.0.0.1:8000/  ```
 
 ## CHANGES REQUIRED
 

## Drawbacks/LoopHoles
* Date and time picker is not supported on safari browser.
* A third-party Agora application is needed to access the video calling facilities through mobile/iOS devices.
* A gmail account is needed to provide feedback, and the user needs to turn on access for less secure apps.
* An initial admin account is needed for approving all other accounts.



