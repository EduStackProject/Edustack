from django.urls import path
from .views import home,manual_student_entry, upload_student_file, view_student_data,success,get_student_by_roll_number,edit_student,send_sms,delete_student


urlpatterns = [
   path('', home, name='home'),
    path('manual_student_entry/', manual_student_entry, name='manual_student_entry'),
    path('upload_student_file/', upload_student_file, name='upload_student_file'),
    path('view_student_data/', view_student_data, name='view_student_data'),
    path('success/', success, name='success'),
    path('get_student_by_roll_number/', get_student_by_roll_number, name='get_student_by_roll_number'),
    path('edit_student/<uuid:student_id>/', edit_student, name='edit_student'),
    path('send_sms/', send_sms, name='send_sms'),
    path('delete_student/',delete_student,name='delete_student'),
    # ... other patterns
]
