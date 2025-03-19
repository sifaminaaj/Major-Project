from django.shortcuts import render,redirect
from farmerapp.models import *
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# Create your views here.

def index(request):
    total_users_count = User.objects.count()
    pending_users_count = User.objects.filter(status='Pending').count()
    accepted_users_count = User.objects.filter(status='Accepted').count()
    return render(request, 'govtOfficer/index.html', {
        'total_users_count': total_users_count,
        'pending_users_count': pending_users_count,
        'accepted_users_count': accepted_users_count,
    })



def graph(request):
    feedback_data = Feedback.objects.all()
    sentiment_counts = {'5': 0, '4': 0, '3': 0, '2': 0, '1': 0}

    for feedback_entry in feedback_data:
        rating = feedback_entry.rating
        sentiment_counts[str(rating)] += 1

    return render(request, 'govtOfficer/feedback-graph.html', {'sentiment_counts': sentiment_counts})


def feedback(request):
    feedback_data = Feedback.objects.all()
    paginator = Paginator(feedback_data, 5) 
    page = request.GET.get('page')
    try:
        feedback_data = paginator.page(page)
    except PageNotAnInteger:
        feedback_data = paginator.page(1)
    except EmptyPage:
        feedback_data = paginator.page(paginator.num_pages)

    return render(request, 'govtOfficer/feedback.html', {'feedback_data': feedback_data})


def sentiment(request):
    feedback_data = Feedback.objects.all()
    sentiment_data = []

    for feedback_entry in feedback_data:
        rating = feedback_entry.rating
        if rating == 5:
            sentiment = "🌟" 
        elif rating == 4:
            sentiment = "😄"
        elif rating == 3:
            sentiment = "😊"
        elif rating == 2:
            sentiment = "😐"  
        else:
            sentiment = "😢" 

        sentiment_data.append({
            'sno': feedback_entry.feedback_id,
            'name': feedback_entry.user_name,
            'email': feedback_entry.user_email,
            'sentiment': sentiment,
        })

    paginator = Paginator(sentiment_data, 5) 

    page = request.GET.get('page')
    try:
        sentiment_data = paginator.page(page)
    except PageNotAnInteger:
        sentiment_data = paginator.page(1)
    except EmptyPage:
        sentiment_data = paginator.page(paginator.num_pages)

    return render(request, 'govtOfficer/sentiment.html', {'sentiment_data': sentiment_data})



def pending_users(request):
    user_list = User.objects.filter(status="Pending")
    paginator = Paginator(user_list, 5) 
    page = request.GET.get('page')
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)
    context = {
        'user': users,
    }
    return render(request, 'govtOfficer/pending-users.html', context)


def all_users(request):
    user_list = User.objects.filter(status="Accepted")
    paginator = Paginator(user_list, 5)
    page = request.GET.get('page')
    try:
        user = paginator.page(page)
    except PageNotAnInteger:
        user = paginator.page(1)
    except EmptyPage:
        user = paginator.page(paginator.num_pages)
    context = {
        'user': user,
    }
    return render(request, 'govtOfficer/all-users.html', context)


def accept_user(request,user_id):
    user = User.objects.get(user_id=user_id)
    user.status = 'Accepted'
    user.save()
    messages.success(request,"user is Accepted")

    return redirect('pending_users')

def reject_user(request,user_id):
    user = User.objects.get(user_id = user_id)
    user.delete()
    messages.success(request,"user is rejected")

    return redirect('pending_users')


def delete_user(request,user_id):
    user = User.objects.get(user_id = user_id)
    user.delete()
    messages.warning(request,"user is Deleted")

    return redirect('all_users')