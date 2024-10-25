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
* Automatic expenses calculator for medicines prescribed in form of Invoice type (view/download).
* Admin access for proper management of the whole system.
* Medical History of the Patient*
* Feedback System for Patients.

## Admin



## Doctor
* Can only view their patient details assigned to that doctor.
* Can view their patient list.
* Can view their appointments/admit details.


## Patient
* Can view assigned doctor's details like ( specialization).
* Can view their booked appointment status (pending/confirmed by admin).
* Can book appointments.
* Can view/download Invoice pdf (Only when that patient is discharged by admin).


## To run the program offline, follow the following steps:
* Install Python(3.7.6) (Don't Forget to Tick Add to Path while installing Python).
* Open Terminal and Execute Following Commands :
    ```
    pip install django
    pip install django-widget-tweaks
    pip install xhtml2pdf
    pip install Pillow

    ```
* Run following commands :
   ```
    py manage.py makemigrations
    py manage.py migrate
    py manage.py runserver
   ```
   
* Now enter following URL in Your Browser Installed On Your Pc

    ```http://127.0.0.1:8000/  ```
 
 ## CHANGES REQUIRED
 * Admin can assign doctor to patient.
 

## Drawbacks/LoopHoles
* An initial admin should be created using django create super user.



