from django.views.generic.list import ListView
from django.views.generic import DetailView
from django.urls import reverse_lazy
from django.http import Http404
from .ownerviews import *
from django.views.decorators.http import require_POST
from .forms import *
from django.core.mail import send_mail
from django.shortcuts import render
from .forms import EmailForm
from django.views.generic import ListView
from django.shortcuts import get_object_or_404
from taggit.models import Tag
from .models import BlogPost


class BlogListView(ListView):
    model = BlogPost
    paginate_by = 5
    queryset = BlogPost.published_objects.all()


class MyPostsListView(ListView):
    model = BlogPost
    paginate_by = 5
    queryset = BlogPost.objects.all()

    def get_queryset(self):
        return super().get_queryset().filter(owner=self.request.user)


class BlogDetailView(DetailView):
    model = BlogPost

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["comment_form"] = CommentForm()
        return context

    def get_object(self, queryset=None):
        pk = self.kwargs.get("pk")

        year = self.kwargs.get("year")
        month = self.kwargs.get("month")
        day = self.kwargs.get("day")
        slug_id = self.kwargs.get("slug_id")

        if pk:
            return get_object_or_404(self.model, pk=pk)
        elif slug_id:
            return get_object_or_404(self.model, created_at__year=year, created_at__month=month, created_at__day=day,
                                     slug=slug_id)
        else:
            raise Http404("No object found matching the provided criteria.")


class BlogDeleteView(OwnerDeleteView):
    model = BlogPost
    success_url = reverse_lazy("blog_app:posts")


class BlogPostCreateView(OwnerCreateView):
    model = BlogPost
    fields = ["title", "text", "tags", "status"]
    success_url = reverse_lazy("blog_app:posts")

    def form_valid(self, form):
        # Призначаємо власника поточного користувача
        form.instance.owner = self.request.user

        # Зберігаємо форму через батьківський метод
        response = super().form_valid(form)

        # Отримуємо теги та статус з POST-запиту
        tags = self.request.POST.get("tags", "")
        status = self.request.POST.get("status", "")

        # Встановлюємо статус, якщо він наданий
        if status:
            form.instance.status = status  # Встановлюємо статус як атрибут моделі

        # Якщо є теги, розділяємо їх і додаємо до моделі
        if tags:
            tag_list = [tag.strip() for tag in tags.split(",") if tag.strip()]
            form.instance.tags.add(*tag_list)  # Додаємо теги

        # Зберігаємо інстанс моделі
        form.instance.save()

        return response


class BlogUpdateView(OwnerUpdateView):
    model = BlogPost
    success_url = reverse_lazy("blog_app:posts")
    fields = ["title", "text", "status"]


@require_POST
def post_comment(request, post_id):
    post = get_object_or_404(BlogPost, id=post_id)
    comment = None

    form = CommentForm(data=request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.save()

    return render(request,
                  'blog_app/comment.html',
                  {
                      'blogpost': post,
                      'form': form,
                      'comment': comment
                  }
                  )


class TaggedPostsView(ListView):
    template_name = 'blog_app/tagged_posts.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        tag_slug = self.kwargs['tag_slug'].lstrip('#')  # Видаляємо '#'
        print(f"Looking for tag with slug: {tag_slug}")  # Виводимо значення slug
        self.tag = get_object_or_404(Tag, slug=tag_slug)  # Отримуємо тег по slug
        print(f"Found tag: {self.tag}")  # Перевіряємо, чи тег знайдений
        return BlogPost.objects.filter(tags__slug=self.tag.slug)  # Фільтруємо пости за тегом

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tag'] = self.tag
        return context


def send_email_view(request):
    if request.method == 'POST':
        form = EmailForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            from_email = form.cleaned_data['from_email']
            to_email = form.cleaned_data['to_email']

            send_mail(subject, message, from_email, [to_email], fail_silently=False)

            return render(request, 'blog_app/email_sent.html')
    else:
        form = EmailForm()

    return render(request, 'blog_app/send_email.html', {'form': form})