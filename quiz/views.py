from django.shortcuts import render, redirect
from django.http import HttpResponse
from django import forms
from django.contrib.auth.decorators import login_required

from collections import defaultdict


# Create your views here.

def index(request):
    return HttpResponse(render(request, 'quiz/index.html'))


class QuizForm(forms.Form):
    subject = forms.CharField()
    date = forms.DateField(widget=forms.SelectDateWidget)


class QuestionForm(forms.Form):
    question = forms.CharField(widget=forms.Textarea(attrs={'rows': 4, 'cols': 80}), label='question')
    option1 = forms.CharField(widget=forms.Textarea(attrs={'rows': 4, 'cols': 80}), label='option1')
    option2 = forms.CharField(widget=forms.Textarea(attrs={'rows': 4, 'cols': 80}), label='option2')
    option3 = forms.CharField(widget=forms.Textarea(attrs={'rows': 4, 'cols': 80}), label='option3')
    option4 = forms.CharField(widget=forms.Textarea(attrs={'rows': 4, 'cols': 80}), label='option4')
    correct_option = forms.ChoiceField(widget=forms.RadioSelect, choices=[(1, 1), [2, 2], [3, 3], [4, 4]])


questioins_papers = defaultdict(list)


@login_required
def create(request):
    if request.method == 'POST':
        form = QuizForm(request.POST)
        quiz_id = ''.join(
            [form.data['subject'], form.data['date_month'], form.data['date_day'], form.data['date_year']])

        if form.is_valid():
            return redirect('quiz:add', quiz_id=quiz_id)
    else:
        form = QuizForm()
        return render(request, 'quiz/create_quiz.html', {'form': form})


@login_required
def add(request, quiz_id):
    print(request)
    print(quiz_id, type(quiz_id))
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        print(form.data)
        question = {'question': form.data['question'],
                    'options': [form.data['option1'], form.data['option2'], form.data['option3'], form.data['option4']],
                    'correct_option': form.data['correct_option']}

        questioins_papers[quiz_id].append(question)

        return render(request, 'quiz/add_questions.html',
                      {'quiz_id': quiz_id, 'form': form, 'questions': questioins_papers[quiz_id]})
    else:
        form = QuestionForm()
        return render(request, 'quiz/add_questions.html',
                      {'quiz_id': quiz_id, 'form': form, 'questions': questioins_papers[quiz_id]})


def submit(request, quiz_id):
    if len(questioins_papers[quiz_id]) < 1:
        return HttpResponse('Error! you must add at least 1 question.')
    else:
        return HttpResponse('Success!')
