
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from django.shortcuts import render
from .models import StickyNote, UserSuggestion

from html.parser import HTMLParser


NUMBER_OF_NOTES_TO_DISPLAY = 20
BAD_WORDS = (
    'puta', 'pota', 'tangina', 'gago' , 'bobo' , 'bubo' , 'bubu' , 'bobu' , 'gaga', 'patay', 'matay', 'natay', 'amp', 'nigga', 'yawa',
    'pisot' , 'bayag', 'buto', 'totoy', 'boto', 'letche', 'itot', 'lolo' , 'salsal', 'jabol', 'pusli', 'shabu', 'whana', 'bilat', 'belat',
    'puke', 'sex' , 'porn', 'dudu', 'dede', 'putay', 'kupal', 'kopal', 'bolbol', 'kantu', 'kasta', 'torjack', 'pisti', 'peste' , 'piste', 'pesti',
    'kant', 'yatis', 'ngina','shuta','nigger','negro','pampam','whore','slut','gagi','shole','hoe','shit','fuck','bitch','ock','uss',
    'cunt','shat','shite','jaku','kanor','jako',
)


class MyHTMLParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.contains_html = False

    def handle_starttag(self, tag, attrs):
        self.contains_html = True
        
def willMakeAHTMLObject(text: str) -> bool:
    parser = MyHTMLParser()
    parser.feed(text)
    print(parser.contains_html)
    return parser.contains_html

def isBadWords(sentence : str, word : str) -> bool:
    hasBadWord = sentence.lower().find(word)
    return True if hasBadWord > -1 else False

def updateSentence(sentence, start , end) -> str:
    for i in range(start , end + 1):
        sentence[i] = '*'
    return sentence

def hasBadWord(sentence : str) -> bool:
    for word in BAD_WORDS:
        if isBadWords(sentence , word):
            return True
    return False

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
    print(isBadWords("Hello ako po ito is max" , 'mox'))
    
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
        
        nicknameHasBadWord = hasBadWord(nickname)
        contentHasBadWord = hasBadWord(content)
        nicknameCanbeHTML = willMakeAHTMLObject(nickname)
        contentCanbeHTML = willMakeAHTMLObject(content)
        
        hasOwnerNickname = True if (nickname.find('Makietech') > -1) else False
                
        
        if not nicknameHasBadWord and not contentHasBadWord and not hasOwnerNickname and not nicknameCanbeHTML and not contentCanbeHTML:
            #nickname = 'Makietech' if hasOwnerNickname else nickname
            sticky_note = StickyNote(
                nickname=nickname, nickname_color=nickname_color, nickname_font=nickname_font,
                content=content, content_color=content_color, content_font=content_font,
                emoji=emoji
                )
            sticky_note.save()
            
        return JsonResponse(
            {
                'message': 'User Notes saved successfully!',
                'hasBadWord' : nicknameHasBadWord or contentHasBadWord or hasOwnerNickname or nicknameCanbeHTML or contentCanbeHTML,
            }
        )
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
    
