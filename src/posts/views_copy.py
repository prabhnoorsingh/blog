from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render
from .forms import PostForm

from .models import Post


def post_create(request):
	form = PostForm(request.POST or None, request.FILES or None) #request.FILES bcoz od adding enctype

	if form.is_valid():
		instance = form.save(commit=False)
		print form.cleaned_data.get("title")
		instance.save()
		messages.success(request,"Successfully Created")
		return HttpResponseRedirect(instance.get_absolute_url())

	# form = PostForm()
	# if request.method=="POST":
	# 	print request.POST

	context = { "form":form}
	return render(request,"post_form.html", context)

def post_detail(request, slug=None):
	instance = get_object_or_404(Post, slug	=slug)
	context = { "title":"My User List",
				"instance":instance
		}

	return render(request,"post_detail.html", context)

def post_list(request):
	# queryset = Post.objects.all().order_by("-timestamp")
	queryset_list = Post.objects.all()
	paginator = Paginator(queryset_list, 3) # Show 5 posts per page
	page_request_var = 'page'
	page = request.GET.get(page_request_var)	
	try:
		queryset = paginator.page(page)
	except PageNotAnInteger:
		# If page is not an integer, deliver first page.
		queryset = paginator.page(1)
	except EmptyPage:
		# If page is out of range (e.g. 9999), deliver last page of results.
		queryset = paginator.page(paginator.num_pages)
	context = { "title":"My User List",
				"object_list":queryset,
				"page_request_var":page_request_var
		}

	# if request.user.is_authenticated():
	# 	context = { "title":"My User List"}
	# else:
	# 	context = { "title":"List"}
	return render(request,"post_list.html", context)

def post_update(request, slug=None):
	instance = get_object_or_404(Post, slug=slug)
	form = PostForm(request.POST or None, request.FILES or None,instance=instance) ###instance important !!
	if form.is_valid():
		instance=form.save(commit=False)
		instance.save()
		messages.success(request,"Saved",extra_tags="html_safe")
		return HttpResponseRedirect(instance.get_absolute_url())

	context = { "title":"My User List",
				"object_list":instance,
				"form": form
		}
	return render(request,"post_form.html", context)

def post_delete(request, slug=None):
	instance = get_object_or_404(Post, slug=slug)
	instance.delete()
	messages.success(request,"deleted")
	return redirect("list")

	# return HttpResponse("<h1>Delete</h1>")