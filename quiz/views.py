import django.forms
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django import forms
from django.contrib.auth.decorators import login_required

from collections import defaultdict
import json
from quiz.models import QuestionPaper


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
ids = {}


@login_required
def create(request):
    if request.method == 'POST':
        form = QuizForm(request.POST)
        id = [form.data['subject'], form.data['date_month'], form.data['date_day'], form.data['date_year']]
        quiz_id = ''.join(id)
        ids[quiz_id] = id

        if form.is_valid():
            return redirect('quiz:add', quiz_id=quiz_id)
    else:
        form = QuizForm()
        return render(request, 'quiz/create_quiz.html', {'form': form})


@login_required
def add(request, quiz_id):
    if request.method == 'POST':
        form = QuestionForm(request.POST)

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

        quiz_js = json.dumps(questioins_papers[quiz_id])
        subject, month, day, year = ids[quiz_id]
        date = '-'.join([year, month, day])
        paper = QuestionPaper(subject=subject, date=date, paper=quiz_js)
        paper.save()

        return HttpResponse('Success!')


all_quizes = QuestionPaper.objects.all()
list_quiz = [(x.subject, x.date) for x in all_quizes]


class SelectQuiz(forms.Form):
    quiz = forms.ChoiceField(choices=[(i, str(x)) for i, x in enumerate(list_quiz)])


paper = None
score = None


def participate(request):
    global all_quizes, list_quiz, score
    score = 0
    all_quizes = QuestionPaper.objects.all()
    list_quiz = [(x.subject, x.date) for x in all_quizes]
    if request.method == 'POST':
        selected_quiz = SelectQuiz(request.POST)

        quiz_index = int(selected_quiz.data['quiz'])
        global paper
        paper = json.loads(all_quizes[quiz_index].paper)
        print(paper)
        return redirect('quiz:givequiz', question_number=1)

    return render(request, 'quiz/participate.html', {'form': SelectQuiz()})


def qive_quiz(request, question_number):
    global score
    question = paper[question_number - 1]
    result = None
    if request.method == 'POST':
        print(request.POST)
        selected_option = request.POST['selected_answer']
        print(selected_option)
        correct_option = question['correct_option']
        result = int(correct_option) == int(selected_option)
        if result:
            score += 1

    return render(request, 'quiz/give_quiz.html', {'question': question['question'],
                                                   'options': [(i + 1, question['options'][i]) for i in
                                                               range(len(question['options']))],
                                                   'result': result,
                                                   'question_number': question_number,
                                                   'number_of_questions': len(paper)})


def finish(request):
    global score,paper
    this_score = score
    score = None
    paper=None
    return render(request, 'quiz/finish.html', {'score': this_score, 'max_score': len(paper)})
