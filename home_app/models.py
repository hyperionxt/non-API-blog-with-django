from django.db import models
from django.utils import timezone
from tinymce.models import HTMLField
from django.contrib.auth import get_user_model
from django.utils.text import slugify
from django.dispatch import receiver
from django.db.models.signals import pre_save


class Category(models.Model):
    
    title = models.CharField(max_length=50)
    slug = models.SlugField('Category slug', unique=True, blank= True, null = True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(get_user_model(), default=1, on_delete=models.SET_DEFAULT)
    
    
    class Meta:
        verbose_name='category'
        verbose_name_plural='categories'
        
    def __str__(self):
        return self.title
    
    
class Sub_Category(models.Model):
    
    title = models.CharField(max_length=50)
    slug = models.SlugField('Sub-Category slug', unique=False, blank= True, null = True)
    category = models.ForeignKey(Category, blank =False, null=False, default=None,on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(get_user_model(), default=1, on_delete=models.SET_DEFAULT)
    
    
    class Meta:
        verbose_name='subcategory'
        verbose_name_plural='subcategories'
        
    def __str__(self):
        return self.title


class Community(models.Model):
    
    
    title = models.CharField(max_length=100, blank=False)
    about = models.CharField(max_length=200, blank=False, unique = True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, blank=False, null=True)
    subcategory = models.ForeignKey(Sub_Category, blank= True, null = True, on_delete=models.SET_NULL)
    adult_content = models.BooleanField('Adult content(+18)',default = False)
    slug = models.SlugField('Community slug', unique=True, blank= True, null = True)
    published = models.DateTimeField('Date created', auto_now_add=True)
    updated=models.DateTimeField('Updated', auto_now=True)
    author = models.ForeignKey(get_user_model(), default=1, on_delete=models.SET_DEFAULT)
    image = models.ImageField("File(image, gif or video)", upload_to='community', null=True, blank=True,max_length=255)
    
    
  
    def __str__(self):
        return self.title
    
    
    class Meta:
        verbose_name_plural="communities"
        ordering = ['-published']
                            
class Post(models.Model):
    

    title = models.CharField(max_length=100, blank=False)
    post_slug = models.SlugField('Post slug', unique=True, blank= False, null = False)
    content =  HTMLField(blank=True, default="")
    published = models.DateTimeField('Date published', auto_now_add=True)
    modified = models.DateTimeField('Date modified', auto_now=True)
    community = models.ForeignKey(Community, default = "", verbose_name="Community", on_delete=models.CASCADE)
    author = models.ForeignKey(get_user_model(), default=1, on_delete=models.SET_DEFAULT)
    image = models.ImageField(upload_to='posts', null=True, blank=True)
    post_category = models.ForeignKey(Category, default=None, on_delete=models.SET_DEFAULT, blank=False, verbose_name="category")
    post_subcategory = models.ForeignKey(Sub_Category, blank=True, null=True, default=None, on_delete=models.SET_DEFAULT, verbose_name="subcategory")

    def save(self, *args, **kwargs):
        if self.community:
            self.post_category = self.community.category
            self.post_subcategory = self.community.subcategory
        super().save(*args, **kwargs)
    
  
    def __str__(self):
        return self.title
    
    @property
    def slug(self):
        return self.community.slug + "/" + self.post_slug
    
    class Meta:
        verbose_name_plural="Posts"
        ordering = ['-published']
    
    
# Slug auto-generator based in objects's title.

@receiver(pre_save, sender=Category)
def post_pre_save(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.title)

@receiver(pre_save, sender=Sub_Category)
def post_pre_save(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.title)
        
@receiver(pre_save, sender=Community)
def post_pre_save(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.title)
        
@receiver(pre_save, sender=Post)
def post_pre_save(sender, instance, *args, **kwargs):
    if not instance.post_slug:
        instance.post_slug = slugify(instance.title)

    

    
