from .models import Post, Category, Response, User
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.decorators import login_required
from .forms import PostForm, ResponseForm


from django.shortcuts import get_object_or_404, render, redirect
# Create your views here.

class PostsList(ListView):
    model = Post
    ordering = '-created_date'
    template_name = 'posts.html'
    context_object_name = 'posts'
    paginate_by = 10


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['posts_count'] = Post.objects.filter(post_author = self.request.user).count
            context['responses_count'] = Response.objects.filter(response_author = self.request.user).count
            posts = Post.objects.filter(post_author = self.request.user)
            context['responses_to_posts_count'] = Response.objects.filter(response_post__in = posts).count

            return context
        return context


class PostDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['owner'] = self.get_object().post_author.id
        response = Response.objects.filter(response_post=self.get_object())
        context['response'] = response
        context['is_subscribed'] = Category.objects.filter(subscribers=self.request.user.id)
        if self.request.user.is_authenticated:
            context['response_form'] = ResponseForm(instance = self.request.user)
        return context

    def post(self, request, *args, **kwargs):
        _response_content = request.POST.get('response_content')
        _response_author = self.request.user
        _response_post = self.get_object()

        responsed = Response(response_content=_response_content, response_author=_response_author, response_post=_response_post)
        responsed.save()
        return redirect('posts_list') 
        

class PostCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('app.add_post')
    form_class = PostForm
    model = Post
    template_name = 'postedit.html'
    success_url = reverse_lazy('posts_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post_category'] = Category.objects.all
        return context
    
    def form_valid(self, form):
        form.instance.post_author = self.request.user
        return super().form_valid(form)

class PostUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = ('app.change_post')
    form_class = PostForm
    model = Post
    template_name = 'postedit.html'
    success_url = reverse_lazy('posts_list')

class PostDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('app.delete_post')
    model = Post
    template_name = 'postdelete.html'
    success_url = reverse_lazy('posts_list')


class MyPostsList(PermissionRequiredMixin, ListView):
    permission_required = ('app.change_post', 'app.change_response')
    model = Post
    ordering = '-created_date'
    template_name = 'myposts.html'
    context_object_name = 'myposts'
    paginate_by = 10

 
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        if self.request.user.is_authenticated:
            context['my_posts'] = Post.objects.filter(post_author = self.request.user)
            context['responses'] = Response.objects.filter(response_post__in=Post.objects.filter(post_author = self.request.user))
        return context

def response_accept(request, *args, **kwargs):
    # response = Response.objects.get(pk=int(kwargs['pk'])).is_accepted = '1'
    response = Response.objects.get(pk=int(kwargs['pk']))
    if response:
        response.is_accepted = True
        response.save()
    return redirect('myposts_list')

def response_delete(request, *args, **kwargs):
    response = Response.objects.get(pk=int(kwargs['pk']))
    if response:
        response.delete()
    return redirect('myposts_list')

@login_required
def subscribe(request, *args, **kwargs):
    Category.objects.get(pk=int(kwargs['pk'])).subscribers.add(request.user.id)
    
    return redirect('/')

@login_required
def unsubscribe(request, *args, **kwargs):
    Category.objects.get(pk=int(kwargs['pk'])).subscribers.remove(request.user.id)
    return redirect('/')