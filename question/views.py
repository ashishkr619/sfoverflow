from django.shortcuts import render
from django.conf import settings
import requests
import json
from datetime import date
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.views.decorators.cache import never_cache
from ratelimit.decorators import ratelimit

from question.api.serializers import QuestionSerializer
from question.forms import QuestionForm
from question.models import Question, Tag, Owner
# Create your views here.


@ratelimit(key='get:q', rate='100/d', block=True)
@ratelimit(key='get:q', rate='5/m', block=True)
def question(request):
    query = None
    results = []
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1
    page = request.GET.get('page')
    user = None
    tag = None

    if 'query' in request.GET and 'user' is None and 'tag' is None:
        print('only query there')
        form = QuestionForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            previous_searches = Question.objects.filter(
                search_term__icontains=query).values_list('search_term', flat=True)
            if query in previous_searches:
                print('true it is there')
                results = Question.objects.filter(Q(title__icontains=query))
            else:
                r = requests.get(
                    'https://api.stackexchange.com/2.2/search/advanced?order=desc&sort=activity&q='+query+'&site=stackoverflow')
                answers = r.json()
                for i in range(len(answers['items'])):

                    is_answered = answers['items'][i]['is_answered']
                    view_count = answers['items'][i]['view_count']
                    # closed_date=date.fromtimestamp(answers['items'][i]['closed_date'])
                    answer_count = answers['items'][i]['answer_count']
                    score = answers['items'][i]['score']
                    last_activity_date = date.fromtimestamp(
                        answers['items'][i]['last_activity_date'])
                    creation_date = date.fromtimestamp(
                        answers['items'][i]['creation_date'])
                    question_id = answers['items'][i]['question_id']
                    link = answers['items'][i]['link']
                    # closed_reason=answers['items'][i]['closed_reason']
                    display_name = answers['items'][i]['owner']['user_id']
                    title = answers['items'][i]['title']
                    search_term = query
                    question = Question.objects.create(is_answered=is_answered, view_count=view_count, link=link, answer_count=answer_count, score=score,
                                                       last_activity_date=last_activity_date, creation_date=creation_date, question_id=question_id, title=title, display_name=display_name, search_term=search_term)
                    results.append(answers['items'][i])

            paginator = Paginator(results, 5)
            # page = request.GET.get('page')
            try:
                results = paginator.page(page)
            except PageNotAnInteger:
                # If page is not an integer deliver the first page
                results = paginator.page(1)
            except EmptyPage:
                # If page is out of range deliver last page of results
                results = paginator.page(paginator.num_pages)

            return render(request, 'questionapp/questions.html', {'form': form, 'results': results, 'query': query, 'page': page, 'num_visits': num_visits})

    elif 'query' in request.GET and 'user' in request.GET and 'tag' in request.GET:
        print('user query')
        form = QuestionForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            user = form.cleaned_data['user']
            tag = form.cleaned_data['tag']
            previous_searches = Question.objects.filter(
                search_term__icontains=query).values_list('search_term', flat=True)
            if query in previous_searches:
                print('true it is there')
                results = Question.objects.filter(Q(title__icontains=query) | Q(display_name__icontains=query) | Q(
                    search_term__icontains=query) | Q(search_term__icontains=user)).distinct()
            else:
                r = requests.get('https://api.stackexchange.com/2.2/search/advanced?order=desc&sort=activity&q=' +
                                 query+'&site=stackoverflow'+'&user='+user+'&tagged='+tag)
                answers = r.json()

                for i in range(len(answers['items'])):

                    is_answered = answers['items'][i]['is_answered']
                    view_count = answers['items'][i]['view_count']
                    # closed_date=date.fromtimestamp(answers['items'][i]['closed_date'])
                    answer_count = answers['items'][i]['answer_count']
                    score = answers['items'][i]['score']
                    last_activity_date = date.fromtimestamp(
                        answers['items'][i]['last_activity_date'])
                    creation_date = date.fromtimestamp(
                        answers['items'][i]['creation_date'])
                    question_id = answers['items'][i]['question_id']
                    link = answers['items'][i]['link']
                    # closed_reason=answers['items'][i]['closed_reason']
                    display_name = answers['items'][i]['owner']['user_id']
                    title = answers['items'][i]['title']
                    for answer in answers['items']:
                        for tag in answer['tags']:
                            for tag_length in range(len(answer['tags'])):
                                # print(answers['items']['tags'])
                                print('tag wale babu zara gaana chala do')
                                tags_present_already = Tag.objects.filter(
                                    word=tag)
                                if not tags_present_already:
                                    tag_created = Tag.objects.create(word=tag)
                                    print(tag_created)

                    search_term = query
                    question = Question.objects.create(is_answered=is_answered, view_count=view_count, link=link, answer_count=answer_count, score=score,
                                                       last_activity_date=last_activity_date, creation_date=creation_date, question_id=question_id, title=title, display_name=display_name, search_term=search_term)
                    question.tags.add(tag_created)
                    results.append(answers['items'][i])

            paginator = Paginator(results, 5)
            # page = request.GET.get('page')
            try:
                results = paginator.page(page)
            except PageNotAnInteger:
                # If page is not an integer deliver the first page
                results = paginator.page(1)
            except EmptyPage:
                # If page is out of range deliver last page of results
                results = paginator.page(paginator.num_pages)

            return render(request, 'questionapp/questions.html', {'tag': tag, 'user': user, 'form': form, 'results': results, 'query': query, 'page': page, 'num_visits': num_visits})

    elif 'query' is None and 'user' in request.GET and 'tag' is None:
        print('user none query there')
        form = QuestionForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['user']
            previous_searches = Question.objects.filter(
                search_term__icontains=query).values_list('search_term', flat=True)
            if query in previous_searches:
                print('true it is there')
                results = Question.objects.filter(
                    Q(title__icontains=query) | Q(display_name=query)).distinct()
            else:
                r = requests.get(
                    'https://api.stackexchange.com/2.2/search/advanced?order=desc&sort=activity&user='+query+'&site=stackoverflow')
                answers = r.json()
                for i in range(len(answers['items'])):

                    is_answered = answers['items'][i]['is_answered']
                    view_count = answers['items'][i]['view_count']
                    # closed_date=date.fromtimestamp(answers['items'][i]['closed_date'])
                    answer_count = answers['items'][i]['answer_count']
                    score = answers['items'][i]['score']
                    last_activity_date = date.fromtimestamp(
                        answers['items'][i]['last_activity_date'])
                    creation_date = date.fromtimestamp(
                        answers['items'][i]['creation_date'])
                    question_id = answers['items'][i]['question_id']
                    link = answers['items'][i]['link']
                    # closed_reason=answers['items'][i]['closed_reason']
                    display_name = answers['items'][i]['owner']['user_id']
                    title = answers['items'][i]['title']
                    search_term = query
                    question = Question.objects.create(is_answered=is_answered, view_count=view_count, link=link, answer_count=answer_count, score=score,
                                                       last_activity_date=last_activity_date, creation_date=creation_date, question_id=question_id, title=title, display_name=display_name, search_term=search_term)
                    results.append(answers['items'][i])

            paginator = Paginator(results, 5)
            # page = request.GET.get('page')
            try:
                results = paginator.page(page)
            except PageNotAnInteger:
                # If page is not an integer deliver the first page
                results = paginator.page(1)
            except EmptyPage:
                # If page is out of range deliver last page of results
                results = paginator.page(paginator.num_pages)

            return render(request, 'questionapp/questions.html', {'form': form, 'results': results, 'query': query, 'page': page, 'num_visits': num_visits})

    else:
        form = QuestionForm()
        return render(request, 'questionapp/questions.html', {'form': form, 'num_visits': num_visits, 'results': results, })

# def active(request):
#     form = QuestionForm()
#     query = None
#     results = []

#     if 'query' in request.GET:
#         form = QuestionForm(request.GET)
#         if form.is_valid():
#             query = form.cleaned_data['query']
#             print(query)
#             r = requests.get('https://api.stackexchange.com/2.2/search/advanced?order=desc&sort=activity&closed=False&title='+query+'&site=stackoverflow')
#             answers = r.json()
#             print(answers)
#             for i in range(len(answers['items'])):
#                 results.append(answers['items'][i])
#                 print(results)


#     return render(request, 'questionapp/questions.html', {'form': form, 'results': results,'query':query,})
