import anthropic
from django.shortcuts import render
from django.http import JsonResponse
from django.conf import settings
from django.contrib.auth.decorators import login_required

# Declare the client as a global variable
client = None
@login_required
def chatbot_view(request):
    if request.method == "POST":
        user_message = request.POST.get('message')
        response = get_claude_response(user_message)
        return JsonResponse({'response': response})
    return render(request, 'chatbot/chatbot.html')

def get_claude_response(user_message):
    try:
        client = get_claude_client()

        system_prompt = """
            You are an intelligent, conversational AI designed to act as a virtual teacher and tutor for students. Your purpose is to help students learn and understand concepts clearly through engaging, supportive, and informative conversation.

            You must:

            - Provide detailed, accurate answers tailored to the student's level of understanding.
            - Offer hints, analogies, examples, or step-by-step explanations when appropriate.
            - Encourage critical thinking and guide students without immediately giving away answers (especially for practice questions).
            - Be patient and approachable, and respond in a friendly, conversational tone.
            - Handle follow-up questions naturally, maintaining topic continuity and context throughout the interaction.
            - Ask clarifying questions if needed to better understand the student's request or level.

            Your role is not just to give answers, but to teach, clarify, and encourage curiosity.
        """

        response = client.messages.create(
            model="claude-3-7-sonnet-20250219",
            max_tokens=1000,
            system=system_prompt,
            messages=[
                {"role": "user", "content": user_message}
            ]
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