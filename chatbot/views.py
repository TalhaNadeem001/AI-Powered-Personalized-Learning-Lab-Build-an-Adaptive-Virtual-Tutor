from django.shortcuts import render
from django.http import JsonResponse

def chatbot_view(request):
    if request.method == "POST":
        user_message = request.POST.get('message')
        response = get_chatbot_response(user_message)
        return JsonResponse({'response': response})
    return render(request, 'chatbot/chatbot.html')

def get_chatbot_response(user_message):
    # Basic responses for demonstration
    if 'hello' in user_message.lower():
        return "Hello! How can I assist you today?"
    elif 'how are you' in user_message.lower():
        return "I'm just a bot, but I'm doing great, thank you!"
    else:
        return "Sorry, I didn't understand that."
