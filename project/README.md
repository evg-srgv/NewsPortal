# News

# 0. Запуск shell, импорт моделей

    python manage.py shell
    from portal.models import *

# 1. Создать двух пользователей (с помощью метода User.objects.create_user).

    user1 = User.objects.create_user(username='Sam')
    user2 = User.objects.create_user(username='Den')

# 2. Создать два объекта модели Author, связанные с пользователями.

    Author.objects.create(authorUser = user1)
    Author.objects.create(authorUser = user2)
    
# 3. Добавить 4 категории в модель Category.

    Category.objects.create(categoryName = 'IT')
    Category.objects.create(categoryName = 'AI')
    Category.objects.create(categoryName = 'Dew')
    Category.objects.create(categoryName = 'Computer science')
    Category.objects.create(categoryName = 'Data science')
    Category.objects.create(categoryName = 'Python')


    

# 4. Добавить 2 статьи и 1 новость.

    author = Author.objects.get(id=1)
    

    Post.objects.create(
    author = author, 
    categoryType = 'Статья', 
    postTitle = 'Inside the machine', 
    postContent = 'CPU - ?'
    )
    
    Post.objects.create(
    author = author, 
    categoryType = 'Новость', 
    postTitle = 'New book', 
    postContent = 'Machine Learning'
    )

# 5. Присвоить им категории (как минимум в одной статье/новости должно быть не меньше 2 категорий).

    Post.objects.get(id=1).category.add(Category.objects.get(id=1))
    
    Post.objects.get(id=1).category.add(Category.objects.get(id=4))

# 6. Создать как минимум 4 комментария к разным объектам модели Post (в каждом объекте должен быть как минимум один комментарий).
 
    Comment.objects.create(
    commentPost=Post.objects.get(id=1),
    commentUser=Author.objects.get(id=1).authorUser, 
    commentText='Very interesting book'
    )

    Comment.objects.create(
                          commentPost=Post.objects.get(id=2), 
                          commentUser = Author.objects.get(id=1).authorUser,
                          commentText='It is interesting'
                          )

    Comment.objects.create(
                          commentPost = Post.objects.get(id=3), 
                          commentUser = Author.objects.get(id=2).authorUser, 
                          commentText="Wow, that's awesome"
                          )

    Comment.objects.create(
                          commentPost=Post.objects.get(id=4), 
                          commentUser = Author.objects.get(id=2).authorUser, 
                          commentText='It is okay'
                          )

# 7. Применяя функции like() и dislike() к статьям/новостям и комментариям, скорректировать рейтинги этих объектов.

    Comment.objects.get(id=1).like()
    Comment.objects.get(id=1).dislike()

    Post.objects.get(id=1).like()
    Post.objects.get(id=1).dislike()
    
    проверка рейтинга пользователя
    Comment.objects.get(id=1).rating

    проверка рейтинга поста
    Post.objects.get(id=1).rating

# 8. Обновить рейтинги пользователей.
    a = Author.objects.get(id=1)
    a.update_rating()
    a.ratingAuthor

    >>> a = Author.objects.get(id=2)

    чтобы посмотреть суммарный рейтинг комментариев пользователя, можно обратиться к нему напрямую

    >>> a.author.comment_set.aggregate(comment_rating=Sum('comment_rate'))
    >>> a.update_rating()
    >>> a.user_rate

# 9. Вывести username и рейтинг лучшего пользователя (применяя сортировку и возвращая поля первого объекта).
    a = Author.objects.order_by('-ratingAuthor')[:1]
    for i in a:
        i.ratingAuthor
        i.authorUser.username    

    28
    'Matt Harrison'

# 10. Вывести дату добавления, username автора, рейтинг, заголовок и превью лучшей статьи, основываясь на лайках/дислайках к этой статье.
    p = Post.objects.order_by('-rating')
    for i in p[:1]:
    ...     i.dateCreation
    ...     i.author.authorUser   
    ...     i.rating
    ...     i.title
    ...     i.preview()

# 11. Вывести все комментарии (дата, пользователь, рейтинг, текст) к этой статье.
    Post.objects.all().order_by('-rating')[0].comment_set.values(
    'dateCreation', 
    'commentUser', 
    'rating',
    'text'
    )

