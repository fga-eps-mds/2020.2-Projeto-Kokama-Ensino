from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods
from .forms import AddNewHistory
from .models import KokamaHistory


@require_http_methods(["GET", "POST"])
def list_history (request):
    if(request.method == 'GET'):
        history_title = KokamaHistory.objects.all()
        context = {
            'history_title': history_title,
        }
        return render(request, 'list_history.html',{'object':history_title})
    else:
        return HttpResponse('<h1>Erro interno do servidor</h1>', status=500)

@require_http_methods(["GET", "POST"])
def add_history(request):
    if(request.method == 'GET'):
        form = AddNewHistory()
        return render(request, 'add_history.html', {'form': form})
    elif(request.method == 'POST'):
        form = AddNewHistory(request.POST)

        if form.is_valid():
            history_title = request.POST.get('history_title')
            history_text = request.POST.get('history_text')
            history = KokamaHistory(history_title=history_title, history_text=history_text)
            history.save()
            return redirect('/')
        

