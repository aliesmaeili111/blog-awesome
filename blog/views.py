from django.shortcuts import render,get_object_or_404
from . models import Article,Category
from django.core.paginator import Paginator
from django.views.generic import ListView,DetailView
from django.db.models import Q
from account.models import User
from account.mixins import AuthorAccessMixin


class ArticleList(ListView):

    # model = Article
    queryset = Article.objects.published()
    paginate_by = 6
    
# def home(request,page=1):
#     article_list =  Article.objects.published()
#     paginator = Paginator(article_slist,6)
#     articles = paginator.get_page(page)
#     context = {
#         "articles":articles,
#     }
#     return render(request,'blog/home.html',context)

class ArticleDetailView(DetailView):
    def get_object(self):
        slug = self.kwargs.get('slug')
        article =  get_object_or_404(Article.objects.published(),slug=slug)

        ip_address = self.request.user.ip_address
        if ip_address not in article.hits.all():
            article.hits.add(ip_address)
        
        return article

# def detail(request,slug):
    
#     context = {
#         "article":get_object_or_404(Article.objects.published(),slug=slug)
#     }
#     return render(request,'blog/detail.html',context) 


class CategoryList(ListView):
    paginate_by = 5
    template_name = 'blog/category_list.html'
    
    def get_queryset(self):
        global category
        slug = self.kwargs.get('slug')
        category = get_object_or_404(Category.objects.active(),slug=slug)
        return category.articles.published() 
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = category
        return context
    
# def category(request,slug,page=1):
#     category = get_object_or_404(Category,slug=slug,status=True)
#     article_list = category.articles.published()
#     paginator = Paginator(article_list,6)
#     articles = paginator.get_page(page)
    
#     context = {
#         "category":category,
#         'articles':articles,
#     }
#     return render(request,'blog/category.html',context)


class AuthorList(ListView):
    paginate_by = 5
    template_name = 'blog/author_list.html'
    
    def get_queryset(self):
        global author
        username = self.kwargs.get('username')
        author = get_object_or_404(User,username=username)
        return author.articles.published() 
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['author'] = author
        return context
    
    
class ArticlePreview(AuthorAccessMixin,DetailView):
    def get_object(self):
        pk = self.kwargs.get('pk')
        return get_object_or_404(Article,pk=pk)
    
def page_not_found_view(request, exception):
    return render(request, 'blog/404.html', status=404)


class SearchList(ListView):
    paginate_by = 5
    template_name = 'blog/search_list.html'
    
    def get_queryset(self):
        global search
        search = self.request.GET.get('q')
        return Article.objects.filter(Q(description__icontains = search) | Q(title__icontains = search))
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search'] = search
        return context