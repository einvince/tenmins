from django.db import models

from django.contrib.auth.models import User
from faker import Factory
# Create your models here.


class Article(models.Model):
    title = models.CharField(max_length=500)
    img = models.URLField(null=True, blank=True)
    content = models.TextField(null=True, blank=True)
    views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    createtime = models.DateField(auto_now=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    belong_to = models.ForeignKey(to=Article, related_name="under_comments", null=True, blank=True)
    name = models.CharField(max_length=500)
    avatar = models.CharField(max_length=250, default="static/images/default.png")
    comment = models.TextField(null=True, blank=True)
    createtime = models.DateField(auto_now=True)

    def __str__(self):
        return self.name


class Ticket(models.Model):
    voter = models.ForeignKey(to=User, related_name="user_tickets")
    article = models.ForeignKey(to=Article, related_name="article_tickets")

    ARTICLE_CHOICES = {
        ("like", "like"),
        ("dislike", "dislike"),
        ("normal", "normal")
    }
    choice = models.CharField(choices=ARTICLE_CHOICES, default="normal",max_length=10)

    def __str__(self):
        # return u"用户: "+str(self.voter) + u"----投票文章:   " + str(self.article) + u"----感觉:" + str(self.choice)
        return str(self.id)



class UserProfile(models.Model):
    belong_to = models.OneToOneField(to=User, related_name='profile')
    SEX_CHOICES = (('male', '男'), ('female', '女'))
    sex = models.CharField(choices=SEX_CHOICES,max_length=20)
    avatar = models.ImageField(upload_to='avatar')
    def __str__(self):
        return str(self.belong_to.username)


# f = open('web.txt', 'r')
# fake = Factory.create()
# for url in f.readlines():
#     ar = Article(
#         title=fake.text(max_nb_chars=25),
#         content=fake.text(max_nb_chars=3000),
#         img=url,
#         )
#     ar.save()


# articles=Article.objects.all()
# x=0
# for article in articles:
#     print(x)
#     article.img = '/upload/article/'+str(x)+'.jpg'
#     article.save()

#     x=x+1
