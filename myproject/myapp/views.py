import logging
from django.conf import settings
from twilio.base.exceptions import TwilioRestException
from twilio.rest import Client
from django.http import HttpResponse
from django.http import HttpResponseBadRequest
from django.views.decorators.http import require_http_methods
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from .models import Student
from django.core.files.storage import FileSystemStorage
import pandas as pd
from  .forms import StudentForm,RollNumberForm
def home(request):
    return render(request, 'myapp/home.html')

def upload_student_file(request):
    if request.method == 'POST' and request.FILES['file']:
        uploaded_file = request.FILES['file']

        # Read the Excel file using pandas
        try:
            df = pd.read_excel(uploaded_file, engine='openpyxl')

            # Iterate through rows and save data to the database
            for index, row in df.iterrows():
                Student.objects.create(
                    name=row['Name'],
                    roll_number=row['Roll Number'],
                    grade=row['Grade'],
                    phno=row['Phone Number'] 

                    # Add other fields as needed
                )

            return redirect('success')  # Redirect to a success page or any other page

        except Exception as e:
            error_message = f"Error processing the Excel file: {str(e)}"
            return render(request, 'myapp/error.html', {'error_message': error_message})

    return render(request, 'myapp/upload_student_file.html')
def view_student_data(request):
    students = Student.objects.all()
    return render(request, 'myapp/view_student_data.html', {'students': students})
def manual_student_entry(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('success')  # Redirect to a success page or any other page
    else:
        form = StudentForm()

    return render(request, 'myapp/manual_student_entry.html', {'form': form})
def success(request):
    return render(request, 'myapp/success.html')
def get_student_by_roll_number(request):
    if request.method == 'POST':
        form = RollNumberForm(request.POST)
        if form.is_valid():
            roll_number = form.cleaned_data['roll_number']
            try:
                student = Student.objects.get(roll_number=roll_number)
                return render(request, 'myapp/student_details.html', {'student': student})
            except Student.DoesNotExist:
                error_message = 'Student with roll number {} not found.'.format(roll_number)
                return render(request, 'myapp/error.html', {'error_message': error_message})
    else:
        form = RollNumberForm()

    return render(request, 'myapp/get_student_by_roll_number.html', {'form': form})
import logging
from django.http import JsonResponse

logger = logging.getLogger(__name__)
def edit_student(request, student_id):
    try:
        student = get_object_or_404(Student, id=student_id)

        if request.method == 'POST':
            form = StudentForm(request.POST, instance=student)

            
            # Replace 'default_phno_value' with the actual default value

            if form.is_valid():
                form.save()  # Save the updated student data

                # Return a success response with JSON content type
                return JsonResponse({'success': True}, content_type='application/json')
            else:
                # If the form is not valid, return an error response
                return JsonResponse({'success': False, 'errors': form.errors}, content_type='application/json')

    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, content_type='application/json')
def send_sms(request):
    if request.method == 'POST':
        phone_number = request.POST.get('phone_number', '')

        # Validate phone number (you may need a more robust validation based on your requirements)
        if not phone_number.isdigit() or len(phone_number) != 10:
            return HttpResponseBadRequest("Invalid phone number. Please enter a 10-digit number.")

        # Your Twilio code...
        account_sid = settings.TWILIO_ACCOUNT_SID
        auth_token = settings.TWILIO_AUTH_TOKEN
        twilio_phone_number = settings.TWILIO_PHONE_NUMBER

        client = Client(account_sid, auth_token)

        try:
            message = client.messages.create(
                body='Hello from your Django app!',
                from_=twilio_phone_number,
                to=phone_number
            )
            return HttpResponse(f"SMS sent successfully to {phone_number}. SID: {message.sid}")
        except TwilioRestException as e:
            return HttpResponse(f"Failed to send SMS. Twilio error: {e}")
        except Exception as e:
            return HttpResponse(f"Failed to send SMS. Error: {str(e)}")

    return render(request, 'myapp/send_sms.html')
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.shortcuts import get_object_or_404
from .models import Student

@require_http_methods(["DELETE"])
def delete_student(request):
    student_id = request.GET.get('id')
    student = get_object_or_404(Student, id=student_id)
    student.delete()
    return JsonResponse({'success': True})
