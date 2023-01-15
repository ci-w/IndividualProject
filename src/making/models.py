from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User

class Category(models.Model):
    category = models.CharField(max_length=128)
    slug = models.SlugField()

    class Meta:
        verbose_name_plural = 'Categories'
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.category)
        super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return self.category


class Project(models.Model):    
    title = models.CharField(max_length=128)
    description = models.TextField(max_length=200)
    instructions = models.TextField(max_length=500)    
    views = models.IntegerField(default=0)
    category = models.ManyToManyField(Category)
    slug = models.SlugField(unique=True)
    # alt text for the associated image
    # no max length for alt text in html
    alt_text = models.TextField(max_length=125)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Project, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

class UserProfile(models.Model):
    # required, links UserProfile to a User model instance
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # The additional attributes we wish to include.
    # need to decide what these are
    requirements = models.TextField(max_length=200)
    def __str__(self):
        return self.user.username
