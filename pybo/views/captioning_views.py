from django.shortcuts import render,get_object_or_404, redirect
from django.http import HttpResponse

from django.utils import timezone
from ..forms import QuestionForm, AnswerForm, CommentForm
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from ..models import Question, Answer, Comment


@login_required(login_url="common:login")
def image_captioning(request):
    question = get_object_or_404(Question)

    if request.method == 'POST':
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.author = request.user
            answer.create_date = timezone.now()
            answer.question = question
            answer.save()
            return redirect('pybo:detail', question_id=question.id)
    else:
        form = AnswerForm()
    context = {'question': question, 'form': form}
    return render(request, 'pybo/question_detail.html', context)