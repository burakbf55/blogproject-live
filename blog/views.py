from django.urls.base import reverse_lazy
from django.views.generic.detail import DetailView
from blog.models import Post
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from .models import Post, Comment
from .forms import CommentForm
from django.views.generic import ListView,CreateView
from django.views.generic.edit import DeleteView, UpdateView

# Create your views here.

class BlogListView(ListView):
    model = Post
    template_name = 'home.html'

class BlogDetailView(DetailView):
    model = Post
    template_name = "post_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs["pk"]

        form = CommentForm()
        post = get_object_or_404(Post, pk=pk,)
        comments = post.comment_set.all()

        context['post'] = post
        context['comments'] = comments
        context['form'] = form
        return context

    def post(self, request, *args, **kwargs):
        form = CommentForm(request.POST)
        self.object = self.get_object()
        context = super().get_context_data(**kwargs)

        post = Post.objects.filter(id=self.kwargs['pk'])[0]
        comments = post.comment_set.all()

        context['post'] = post
        context['comments'] = comments
        context['form'] = form

        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            content = form.cleaned_data['content']

            comment = Comment.objects.create(
                name=name, email=email, content=content, post=post
            )

            form = CommentForm()
            context['form'] = form
            return self.render_to_response(context=context)

        return self.render_to_response(context=context)

class BlogCreateView(CreateView):
    model = Post
    template_name = 'post_yeni.html'
    fields = '__all__'

class BlogUpdateView(UpdateView):
    model = Post
    template_name ="post_edit.html"
    fields = ['title', 'body']

class BlogDeleteView(DeleteView):
    model = Post
    template_name = "post_silme.html"
    success_url = reverse_lazy("home")