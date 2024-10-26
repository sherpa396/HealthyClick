'''
The admin.py file in Django plays a crucial role in managing the administrative interface of a Django application. It is primarily used to register models with the Django admin site, allowing for easy management of data through a web interface. Here’s a detailed overview of its uses and functionalities:
#Purpose of admin.py
1. Model Registration:
- The primary function of admin.py is to register models so they can be managed through the Django admin interface. By registering a model, you allow it to be accessible for Create, Read, Update, and Delete (CRUD) operations via the admin panel.

2. Customization of Admin Interface:
- You can customize how models are displayed in the admin interface by creating a class that inherits from admin.ModelAdmin. This allows you to define fields to display, search capabilities, and filtering options.     

3. Adding Functionality:
- You can add custom actions and features to your models within the admin interface. This includes defining methods that perform specific tasks on selected records.     

4. Inline Models:
- For models that have relationships (like ForeignKey), you can use inline classes to manage related records directly within the parent model's admin form.
5. Customizing Admin Site Appearance:
- You can change the layout and appearance of the admin site by overriding templates or using CSS styles specific to your application.
'''

from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin


# Register your models here.
class UserModel(UserAdmin):
    list_display = ["username", "email", "user_type"]


admin.site.register(CustomUser, UserModel)
admin.site.register(Specialization)
admin.site.register(DoctorReg)
admin.site.register(Appointment)
admin.site.register(Page)
admin.site.register(Payment)

