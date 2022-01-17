from django.shortcuts import render


# Create your views here.

def Diary(request):
    return render(request, 'Diary.html')


def main(request):
    return render(request, 'main.html')
