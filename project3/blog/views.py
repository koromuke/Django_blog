from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect
from django.views import generic
from .models import Post, Category, Comment
from .forms import CommentCreateForm


class IndexView(generic.ListView):
    # template_name = 'blog/post_list.html'
    model = Post
    paginate_by = 10

    def get_queryset(self):
        queryset = Post.objects.order_by('-created_at')
        keyword = self.request.GET.get('keyword')

        if keyword:
            # キーワードを含む、の検索
            queryset = queryset.filter(
             Q(title__icontains=keyword) | Q(text__icontains=keyword)
            )
        return queryset


class CategoryView(generic.ListView):
    model = Post
    paginate_by = 10

    def get_queryset(self):

        category = get_object_or_404(Category, pk=self.kwargs['pk'])
        queryset = Post.objects.order_by('-created_at').filter(category=category)

        """
        カテゴリのpkを取得後、カテゴリ自体ではなくカテゴリのプライマリキーで絞り込む方法、ForeignKey・many to manyでも同じ書き方ができる。
        category_pk = self.kwargs['pk']
        queryset = Post.objects.order_by('-created_at').filter(category__pk=category_pk)
        """

        return queryset


class DetailView(generic.DetailView):
    model = Post


class CommentView(generic.CreateView):
    model = Comment
    form_class = CommentCreateForm
    # fields = ('name', 'text')  こちらは今回は使えない。

    def form_valid(self, form):
        post_pk = self.kwargs['post_pk']
        comment = form.save(commit=False)  # インスタンスは作成されていますがコメントはDBに保存されていません
        comment.post = get_object_or_404(Post, pk=post_pk)  # インスタンスがあるのでコメントオブジェクトを操作できます。
        comment.save()  # ここでDBに保存
        return redirect('blog:detail', pk=post_pk)
