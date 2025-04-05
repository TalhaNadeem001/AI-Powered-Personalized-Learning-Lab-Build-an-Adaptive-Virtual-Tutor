import anthropic
from django.shortcuts import render
from django.http import JsonResponse
from django.conf import settings

# Declare the client as a global variable
client = None

def chatbot_view(request):
    if request.method == "POST":
        user_message = request.POST.get('message')
        response = get_claude_response(user_message)
        return JsonResponse({'response': response})
    return render(request, 'chatbot/chatbot.html')

def get_claude_response(user_message):
    try:
        # Get the existing or new client instance
        client = get_claude_client()
        
        response = client.messages.create(
            model="claude-3-7-sonnet-20250219",
            max_tokens=1000,
            messages=[{"role": "user", "content": f"{user_message}"}]
        )
        return response.content[0].text
        
    except Exception as e:
        return f"Error: {str(e)}"

def get_claude_client():
    global client
    if client is None:
        try:
            client = anthropic.Anthropic(api_key=settings.ANTHROPIC_API_KEY)
        except Exception as e:
            print(f"Error initializing client: {e}")
            raise
    return client