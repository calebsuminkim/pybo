from django.shortcuts import render,get_object_or_404, redirect
from django.http import HttpResponse

from django.utils import timezone
from ..forms import QuestionForm, AnswerForm, CommentForm
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from ..models import Question, Answer, Comment

@login_required(login_url='common:login')
def comment_create_question(request, question_id):

    form = CommentForm() # forms.py에서 클래스 만들어질 필요
    context = {'form':form}
    return render(request, 'pybo/comment_form.html', context) # 새로 html파일이 만들어질 필요

@login_required(login_url='common:login')
def comment_modify_question(request, comment_id):
    """
    pybo 질문 댓글 수정
    """
    comment = get_object_or_404(Answer, pk=comment_id)
    if request.user != comment.author:
        messages.error(request, '댓글수정 권한이 없습니다.')
        return redirect('pybo:detail', question_id=comment.question.id)

    if request.method == 'POST':
        form = AnswerForm(request.POST, instance=comment)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.modify_date = timezone.now()
            comment.save()
            return redirect('pybo:detail', question_id=comment.question.id)
    else:
        form = CommentForm(instance=comment)
    context = {'form':form}
    return render(request, 'pybo/comment_form.html', context)

@login_required(login_url='common:login')
def comment_delete_question(request, answer_id):
    """
    pybo 질문 댓글 삭제
    """
    comment = get_object_or_404(Answer, pk=answer_id)
    if request.user != comment.author:
        messages.error(request, '댓글삭제 권한이 없습니다.')
        return redirect('pybo:detail', question_id=comment.answer.question.id)
    else:
        comment.delete()
    return redirect('pybo:detail', question_id=comment.answer.question.id)


@login_required(login_url='common:login')
def comment_create_answer(request, answer_id):
    """
    pybo 답변 댓글 등록
    """
    answer = get_object_or_404(Answer, pk=answer_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.create_date = timezone.now()
            comment.answer = answer
            comment.save()
            return redirect('pybo:detail', question_id=comment.answer.question.id)
    else:
        form = CommentForm()
    context = {'form':form}
    return render(request, 'pybo/comment_form.html', context)

@login_required(login_url='common:login')
def comment_modify_answer(request, comment_id):
    """
    pybo 답변 댓글 수정
    """
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.user != comment.author:
        messages.error(request, '댓글수정 권한이 없습니다.')
        return redirect('pybo:detail', question_id=comment.question.id)

    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.create_date = timezone.now()
            comment.save()
            return redirect('pybo:detail', question_id=comment.answer.question.id)
    else:
        form = CommentForm(instance=comment)
    context = {'form':form}
    return render(request, 'pybo/comment_form.html', context)

@login_required(login_url='common:login')
def comment_delete_answer(request, comment_id):
    """
    pybo 답글 댓글 삭제
    """
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.user != comment.author:
        messages.error(request, '댓글삭제 권한이 없습니다.')
        return redirect('pybo:detail', question_id=comment.answer.question.id)
    else:
        comment.delete()
    return redirect('pybo:detail', question_id=comment.answer.question.id)