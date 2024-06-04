
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

from django.shortcuts import render
from .models import StickyNote, UserSuggestion


NUMBER_OF_NOTES_TO_DISPLAY = 3

# Create your views here.

def get_incremental_sticky_notes(start_id, count):
    sticky_notes = list(StickyNote.objects.filter(id__gte=start_id).order_by('id')[:count])
    print(f"Sticky Notes Incremental : {sticky_notes}")
    sticky_notes.reverse()
    return sticky_notes

def next_page(start_id):
    sticky_notes = StickyNote.objects.filter(id__lt=start_id).order_by('-id')[:NUMBER_OF_NOTES_TO_DISPLAY]
    print(f"Next Page: {sticky_notes}")
    return sticky_notes

def previous_page(start_id):
    sticky_notes = StickyNote.objects.filter(id__gt=start_id).order_by('id')[:NUMBER_OF_NOTES_TO_DISPLAY:-1]
    print(f"Previous Page: {sticky_notes}")
    return sticky_notes
    
def get_decremental_sticky_notes(start_id, count):
    sticky_notes = list(StickyNote.objects.filter(id__lte=start_id).order_by('-id')[:count])
    print(f"Sticky Notes Decremental : {sticky_notes}")
    sticky_notes.reverse()
    return sticky_notes



@login_required
def sticky_notes_view(request):
    if request.method == 'POST':
        direction = request.POST.get('direction')
        start_id = request.POST.get('start_id')
        count = NUMBER_OF_NOTES_TO_DISPLAY
        
        print(f"\n\ndirection : {direction} \nstart_id : {start_id} \ncount: {count}")
        
        start_id = int(request.POST.get('start_id'))

        if direction == 'up':
            sticky_notes = next_page(start_id=start_id)
        elif direction == 'down':
            sticky_notes = previous_page(start_id)
            
        else:
            return JsonResponse({'error': 'Invalid direction'}, status=400)

        isDatabaseHasData = len(sticky_notes) > NUMBER_OF_NOTES_TO_DISPLAY - 1
        notes_data = [
            {
                "nickname": note.nickname, "nickname_color": note.nickname_color, 
                "nickname_font": note.nickname_font, "content": note.content, 
                "content_color": note.content_color, "content_font": note.content_font,
                "emoji": note.emoji , 'note_id': note.id
            }
            for note in sticky_notes
        ]
        return JsonResponse(
            {
                'sticky_notes': notes_data ,
                'isDatabaseHasData' : isDatabaseHasData
            }
        )
    else:
        # If it's not a POST request, you can return an empty response or handle it accordingly
        return JsonResponse({'error': 'Invalid request method'}, status=405)


def clipboard_list_page(request):
    if request.method == "GET":
        notes = sticky_notes = StickyNote.objects.all().order_by('-id')[:NUMBER_OF_NOTES_TO_DISPLAY]
        previous_page(12)
        context = {"notes" : notes }
        return render(request , 'clipboards_screens.html' , context=context)


@csrf_exempt
def write_notes(request):
    if request.method == 'POST':
        nickname = request.POST.get('nickname')
        nickname_color = request.POST.get('nickname_color')
        nickname_font = request.POST.get('nickname_font')
        content = request.POST.get('content')
        content_color = request.POST.get('content_color')
        content_font = request.POST.get('content_font')
        emoji = request.POST.get('emoji')
        
        sticky_note = StickyNote(
            nickname=nickname, nickname_color=nickname_color, nickname_font=nickname_font,
            content=content, content_color=content_color, content_font=content_font,
            emoji=emoji
            )
        sticky_note.save()
        return JsonResponse({'message': 'User Notes saved successfully!'})
    elif request.method == 'GET':
        return render(request , 'write_notes_screens.html' )
    else:
        return JsonResponse({'error': 'Invalid request method'})


@csrf_exempt
def suggestion_page(request):
    if request.method == 'POST':
        nickname = request.POST.get('nickname')
        subject = request.POST.get('subject')
        content = request.POST.get('content')
        suggestion = UserSuggestion(nickname=nickname, subject=subject, content=content)
        suggestion.save()
        return JsonResponse({'message': 'User suggestion saved successfully!'})
    elif request.method == 'GET':
        return render(request, 'suggestions_screens.html')
    else:
        return JsonResponse({'error': 'Invalid request method'})
    
