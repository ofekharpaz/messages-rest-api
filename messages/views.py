import json
from django.http import JsonResponse
from .models import Message
from django.views.decorators.http import require_GET
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404

@csrf_exempt
def write_message(request):
    if request.method == 'POST':
        try:
            # Decode the JSON data from the request body
            data = json.loads(request.body)
            # Extract message data from request
            sender = data.get('sender')
            receiver = data.get('receiver')
            message = data.get('message')
            subject = data.get('subject')
            is_read = data.get('is_read')
            # Create a new message object and save it to the database
            message_obj = Message.objects.create(sender=sender, receiver=receiver, message=message, subject=subject, is_read=is_read)
            
            # Return a JSON response indicating success
            res = JsonResponse({'message': 'Message written successfully'})
        except json.JSONDecodeError:
            res = JsonResponse({'error': 'Invalid JSON format'}, status=400)
    else:
        # Return a JSON response with an error message for other request methods
        res = JsonResponse({'error': 'Only POST requests are allowed'}, status=405)
    print(res)
    return res

@require_GET
def get_user_messages(request, username):
    # Query the database to retrieve all messages for the specified user
    user_messages = Message.objects.filter(receiver=username)
    
    # Serialize the queryset to JSON
    messages_data = list(user_messages.values())
    
    # Return the JSON response containing the messages data
    return JsonResponse(messages_data, safe=False)

@require_GET
def get_unread_messages(request, username):
    # Query the database to retrieve unread messages for the specified user
    unread_messages = Message.objects.filter(receiver=username, is_read=False)

    # Serialize the unread messages into JSON format
    serialized_messages = [
        {
            'sender': message.sender,
            'message': message.message,
            'subject': message.subject,
            'creation_date': message.creation_date.strftime('%Y-%m-%d %H:%M:%S'),  # Convert to string format
        }
        for message in unread_messages
    ]

    # Return a JSON response containing the unread messages
    return JsonResponse({'unread_messages': serialized_messages})

@require_GET
def read_message(request, username):
    # Retrieve an unread message (e.g., the latest one)
    message = Message.objects.filter(receiver=username, is_read=False).order_by('creation_date').first()
    if not message:
        return JsonResponse({'message': 'No unread messages'}, status=404)
    # Update the message status to "read"
    message.is_read = True
    message.save()
    
    # Prepare the response data
    response_data = {
        'id': message.id,
        'sender': message.sender,
        'receiver': message.receiver,
        'message': message.message,
        'subject': message.subject,
        'creation_date': message.creation_date,
        'is_read': message.is_read
    }
    
    # Return the JSON response
    return JsonResponse(response_data)

@csrf_exempt
def delete_message(request, username, subject):
    # Get the message to be deleted
    if request.method != 'DELETE':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
    message = get_object_or_404(Message, subject=subject)
    
    # Check if the user is the owner or the receiver of the message
    if message.sender == username or message.receiver == username:
        # Delete the message
        message.delete()
        return JsonResponse({'message': 'Message deleted successfully'})
    else:
        # Return a 403 Forbidden response if the user is neither the owner nor the receiver
        return JsonResponse({'error': 'You are not authorized to delete this message'}, status=403)