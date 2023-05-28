from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from django.core.cache import cache




class Author(models.Model):
    authorUser = models.OneToOneField(User, on_delete=models.CASCADE)
    authorRating = models.SmallIntegerField("рейтинг автора", default=0)

    def update_rating(self):
        postRat = self.post_set.aggregate(postRating=Sum('rating'))
        pRat = 0
        pRat += postRat.get('postRating')

        commentRat = self.authorUser.comment_set.aggregate(commentRating=Sum('rating'))
        cRat = 0
        cRat += commentRat.get('commentRating')

        self.authorRating = pRat * 3 + cRat
        self.save()

    def __str__(self):
        return f'{self.authorUser.username}'


class Category(models.Model):
    categoryName = models.CharField('Выберите категорию публикаций для подписки:', max_length=64, unique=True)
    subscribers = models.ManyToManyField(User, related_name='categories', blank=True, null= True)
    
    def __str__(self):
        return f'{self.categoryName}'


class Post(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)

    NEWS = 'Новость'
    ARTICLE = 'Статья'
    CATEGORIES = [
        (NEWS, 'Новость'),
        (ARTICLE, 'Статья')
    ]
    categoryType = models.CharField(max_length=10,
                                     choices=CATEGORIES,
                                     default=ARTICLE)
    
    category = models.ManyToManyField(Category, through='PostCategory')

    publicationDate = models.DateTimeField('Publication date ', auto_now_add=True)
    postTitle = models.CharField('Title ', max_length=128)
    postContent = models.TextField('Content')
    rating = models.SmallIntegerField("рейтинг статьи/новости", default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        return f'{self.postContent[:124]} ...'

    def __str__(self):
        return f'{self.postTitle}. {self.postContent[:124]} ...'

    def get_absolute_url(self):
        return f'http://127.0.0.1:8000/portal/{self.id}'
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        cache.delete(f'Post-{self.pk}')

    def message_subscriber(self):
        return f'Новая статья - "{self.postTitle}" в разделе "{self.category.first()}" '


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.post}. {self.category}'


class Comment(models.Model):
    commentPost = models.ForeignKey(Post, on_delete=models.CASCADE)
    commentUser = models.ForeignKey(User, on_delete=models.CASCADE)
    commentText = models.CharField('текст комментария', max_length=200)
    publicationDate = models.DateTimeField('дата и время публикации комментария', auto_now_add=True)
    rating = models.SmallIntegerField("рейтинг комментария", default=0)

    def __str__(self):
        return f'{self.commentUser.username}'

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def postComment(self):
        return f'Комментарий к статье:\n Дата: {self.publicationDate}\nПользователь: {self.commentUser}\n Рейтинг: {self.rating}\n Коментарий: {self.commentText}'
