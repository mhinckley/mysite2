from django.shortcuts import render, redirect, render, get_object_or_404
from django.utils import timezone
from .models import Post, Proof, Comment, Follow, Tag, PostTag
from .forms import PostForm, EmailUserCreationForm
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import View, CreateView
from django.core.urlresolvers import reverse
from libs import google_sheet_accessor 
from django.utils.decorators import method_decorator
from jsonview.decorators import json_view
from django.contrib.auth.models import User


try:
    from django.utils import simplejson as json
except ImportError:
    import json


def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
    tag_name = request.GET.get('tag')
    if tag_name:
        posts = posts.filter(posttag__tag__text=tag_name)
    liked_posts = Post.objects.filter(likes=request.user.pk)
    paginator = Paginator(posts, 10)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        posts = paginator.page(paginator.num_pages)

    return render(request, 'board/post_list.html', {'posts': posts, 'liked_posts': liked_posts})


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    liked_posts = Post.objects.filter(likes=request.user.pk)
    daily_post = len(post.follow_set.filter(user=request.user.pk, frequency=Follow.DAILY)) #TRUE (1) OR FALSE (0) if following daily
    weekly_post = len(post.follow_set.filter(user=request.user.pk, frequency=Follow.WEEKLY)) #TRUE (1) OR FALSE (0) if following weekly
    monthly_post = len(post.follow_set.filter(user=request.user.pk, frequency=Follow.MONTHLY)) #TRUE (1) OR FALSE (0) if following monthly
    return render(request, 'board/post_detail.html', {'post': post, 'liked_posts': liked_posts, 
        'daily_post': daily_post, 'weekly_post': weekly_post, 'monthly_post': monthly_post})


def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'board/post_edit.html', {'form': form})

def clazz_posts(request, clazz):
    posts = Post.objects.filter(clazz=clazz).order_by('-published_date')
    return render(request, 'board/post_list.html', {'posts': posts})

#def genre_posts(request, content_type):
#    posts = Post.objects.filter(content_type=content_type).order_by('-published_date')
#    return render(request, 'board/post_list.html', {'posts': posts})

#def remember_posts(request, when):
#    posts = Post.objects.filter(when=when).order_by('-published_date')
#    return render(request, 'board/post_list.html', {'posts': posts})

def user_posts(request, author):
    posts = Post.objects.filter(author__username=author).order_by('-published_date')
    return render(request, 'board/post_list.html', {'posts': posts})

def to_posts(request, to_field):
    posts = Post.objects.filter(to_field=to_field).order_by('-published_date')
    return render(request, 'board/post_list.html', {'posts': posts})

def my_toolkit(request):
    user = request.user
    if user.is_authenticated():
        liked_posts = Post.objects.filter(likes=request.user.pk)
        my_posts = Post.objects.filter(author=request.user.pk).order_by('-published_date')

        daily_follows = user.follow_set.filter(frequency=1)
        daily_post_ids = daily_follows.values_list('post')
        daily_posts = Post.objects.filter(id__in=daily_post_ids)
        
        weekly_follows = user.follow_set.filter(frequency=3)
        weekly_post_ids = weekly_follows.values_list('post')
        weekly_posts = Post.objects.filter(id__in=weekly_post_ids)

        monthly_follows = user.follow_set.filter(frequency=6)
        monthly_post_ids = monthly_follows.values_list('post')
        monthly_posts = Post.objects.filter(id__in=monthly_post_ids)

        # Get all remaining posts that user has saved
        all_follow_posts_ids = daily_post_ids | weekly_post_ids | monthly_post_ids # Combining Query Sets
        saved_for_later_posts = liked_posts.exclude(id__in=all_follow_posts_ids)
        saved_for_later_post_ids = saved_for_later_posts.values_list('id')

        # Get all remaining posts that user has created
        my_remainder_posts = my_posts.exclude(id__in=saved_for_later_post_ids).exclude(id__in=all_follow_posts_ids)
        
        # to debug you can put "print liked_posts" into a view or "print anything"    
        return render(request, 'board/mytoolkit.html', {'liked_posts': liked_posts,
            'daily_posts': daily_posts, 'weekly_posts': weekly_posts, 'monthly_posts': monthly_posts,
            'saved_for_later_posts': saved_for_later_posts, 'my_remainder_posts': my_remainder_posts})

    else:
        return redirect('../login/')


#Parameters in the def are recieved from the url
#Second argument in return defines which template
#Third argument in return function defines what object will be available in the templates


def person_posts(request, person_or_proof):
    person_from_posts = Post.objects.filter(person__iexact=person_or_proof)
    person_from_proofs = Post.objects.filter(proof__person__iexact=person_or_proof)
    posts = person_from_posts | person_from_proofs 
    return render(request, 'board/post_list.html', {'posts': posts})


def register(request):
    if request.method == 'POST':
        form = EmailUserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            new_user = authenticate(username=form.cleaned_data['username'],
                                    email=form.cleaned_data['email'],
                                    password=form.cleaned_data['password1'],
                                    )
            login(request, new_user)
            return HttpResponseRedirect('/')

    else:
        form = EmailUserCreationForm()
    return render(request, "registration/register.html", {
        'form': form,
    })


def user_login(request):
    # If the request is a HTTP POST, try to pull out the relevant information.
    if request.method == 'POST':
        # Gather the username and password provided by the user.
        # This information is obtained from the login form.
        username = request.POST['username']
        password = request.POST['password']

        # Use Django's machinery to attempt to see if the username/password
        # combination is valid - a User object is returned if it is.
        user = authenticate(username=username, password=password)

        # If we have a User object, the details are correct.
        # If None (Python's way of representing the absence of a value), no user
        # with matching credentials was found.
        if user:
            # Is the account active? It could have been disabled.
            if user.is_active:
                # If the account is valid and active, we can log the user in.
                # We'll send the user back to the homepage.
                login(request, user)
                return HttpResponseRedirect('post_list.html')
            else:
                # An inactive account was used - no logging in!
                return HttpResponse("Your account is disabled.")
        else:
            # Bad login details were provided. So we can't log the user in.
            print "Invalid login details: {0}, {1}".format(username, password)
            return HttpResponse("Invalid login details supplied.")

    # The request is not a HTTP POST, so display the login form.
    # This scenario would most likely be a HTTP GET.
    else:
        # No context variables to pass to the template system, hence the
        # blank dictionary object...
        return render(request, 'registration/login.html', {})


class ProofCreate(CreateView):
    model = Proof
    fields = ['person', 'caption', 'source_url']

    def get_success_url(self):
        return reverse("post_detail", kwargs = {"pk": self.kwargs["post"]})

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post = Post.objects.get(pk=self.kwargs["post"])
        return super(ProofCreate, self).form_valid(form)


class CommentCreate(CreateView):
    model = Comment
    fields = ['entry']

    def get_success_url(self):
        return reverse("post_detail", kwargs = {"pk": self.kwargs["post"]})

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post = Post.objects.get(pk=self.kwargs["post"])
        return super(CommentCreate, self).form_valid(form)


@login_required(login_url='/user')
def like_button(request):
    if request.method == 'POST':
        user = request.user
        id = request.POST.get('pk', None)
        post = get_object_or_404(Post, pk=id)

        if post.likes.filter(id=user.id).exists():
            post.likes.remove(user)
        else:
            post.likes.add(user)

    context = {'likes_count': post.total_likes}
    return JsonResponse(context)


@login_required(login_url='/user')
def follow_button(request):
    context = {}
    if request.method == 'POST':
        user = request.user
        id = request.POST.get('pk')
        post = get_object_or_404(Post, pk=id)

        frequency = int(request.POST.get('frequency'))
        follows = Follow.objects.filter(user=user, post=post)

        if follows.exists():
            if follows.first().frequency == frequency:
                follows.delete()
            else:
                follows.update(frequency=frequency)
        else:
            Follow.objects.create(user=user, post=post, frequency=frequency)

        context = {
            'total_daily': post.total_daily,
            'total_weekly': post.total_weekly,
            'total_monthly': post.total_monthly,
            'total_all': post.total_all_follows
        }
    return JsonResponse(context)


def home(request):
    return render(request, 'board/home.html')

'''
class GoogleDataView(View):
    @method_decorator(json_view)
    def dispatch(self, *args, **kwargs):
        return super(GoogleDataView, self).dispatch(*args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        # Get relevant info from headers
        resource_id = request.META['X-Goog-Resource-ID']
        print(resource_id)
        # Call library function to retrieve new data
        data = google_sheet_accessor.get_post_from_google(resource_id)

        post = Post()
        # Map google data fields to Post object
        post.to_field = data['to_field_sheet']
        post.do_field = data['do_field_sheet']
        post.person = data['person_sheet']
        post.summary = data['summary_sheet']
        post.source_url = data['source_url_sheet']
        email_address = data['author_sheet']        
        post.author = User.objects.filter(email=email_address).first()
        post.save()
        return reverse("post_detail", kwargs = {"pk": self.kwargs["post"]})
'''


