from django.http import JsonResponse
from .models import Message
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def write_message(request):
    if request.method == 'POST':
        # Extract message data from request
        sender = request.POST.get('sender')
        receiver = request.POST.get('receiver')
        message = request.POST.get('message')
        subject = request.POST.get('subject')
        # Create a new message object and save it to the database
        message_obj = Message.objects.create(sender=sender, receiver=receiver, message=message, subject=subject)
        
        # Return a JSON response indicating success
        res = JsonResponse({'message': 'Message written successfully'})
    else:
        # Return a JSON response with an error message for other request methods
        res = JsonResponse({'error': 'Only POST requests are allowed'}, status=405)
    print(res)
    return res

# Define other views for getting messages, marking as read, deleting messages, etc.