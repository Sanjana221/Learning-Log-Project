from django.shortcuts import render
from django.http import HttpResponseRedirect,Http404
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import Topic,Entry
from .forms import TopicForm,EntryForm

# Create your views here.
def index(request):
   """The home page for Learning Log"""
   return render(request,'Learning_logs/index.html')
@login_required
def topics(request):
   """show all topics."""
   topics=Topic.objects.filter(owner=request.user).order_by('date_added')
   context={'topics':topics}
   return render(request,'Learning_logs/topics.html',context)

@login_required
def topic(request,topic_id):
   """show a single topic and all it's entries."""
   topic = Topic.objects.get(id=topic_id)
   #make sure the topic belongs to the current user
   if topic.owner!=request.user:
      raise Http404
   entries=topic.entry_set.order_by('-date_added')
   context={'topic':topic,'entries':entries}
   return render(request,'Learning_logs/topic.html',context)

@login_required
def new_topic(request):
   """Add a new topic"""
   if request.method!='POST':
      #No data submited,create a blank form
      form = TopicForm
   else:
      #post data submited,process data
      form = TopicForm(request.POST)
      if form.is_valid():
         new_topic=form.save(commit=False)
         new_topic.owner=request.user
         new_topic.save()
         #form.save()
         return HttpResponseRedirect(reverse('Learning_logs:topics'))
   context={'form':form}
   return render(request,'Learning_logs/new_topic.html',context)

@login_required
def new_entry(request,topic_id):
   """Add a new entry for a particular topic"""
   topic=Topic.objects.get(id=topic_id)

   if request.method !='POST':
      #No data submited create a blank form
      form = EntryForm()
   else:
      #post data submited,process it.
      form = EntryForm(data=request.POST)
      if form.is_valid():
         new_entry=form.save(commit=False)
         new_entry.topic = topic
         new_entry.save()
         return HttpResponseRedirect(reverse('Learning_logs:topic',args=[topic_id]))
      
   context = {'topic':topic,'form':form}
   return render(request,'Learning_logs/new_entry.html',context)

@login_required 
def edit_entry(request,entry_id):
   """Edit an existing entry."""
   entry=Entry.objects.get(id=entry_id)
   topic=entry.topic
   if topic.owner!=request.user:
      raise Http404

   if request.method!='POST':
      #Initial request;pre fill form with the current entry.
      form = EntryForm(instance=entry)
   else:
      #post data submited;process data
      form = EntryForm(instance=entry,data=request.POST)
      if form.is_valid():
         form.save()
         return HttpResponseRedirect(reverse('Learning_logs:topic',args=[topic.id]))
   
   context={'entry':entry,'topic':topic,'form':form}
   return render(request,'Learning_logs/edit_entry.html',context)




