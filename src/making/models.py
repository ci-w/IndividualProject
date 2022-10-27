from django.db import models
from django.template.defaultfilters import slugify

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
    instructions = models.TextField(max_length=500)    
    views = models.IntegerField(default=0)
    category = models.ManyToManyField(Category)
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Project, self).save(*args, **kwargs)

    def __str__(self):
        return self.title
