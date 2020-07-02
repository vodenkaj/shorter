from django.db import models

from nanoid import generate
import re
# Create your models here.

class Url(models.Model):
    url = models.URLField(max_length=500)
    slug = models.CharField(max_length=100, blank=True)
    
    def __str__(self):
        return self.url

    def validate(self, form, slug, path):
        error = Url.check_slug(self, slug.lower()) if slug else None
        if form.is_valid() and not error:
            form = form.save(commit=False)
            if not slug:
                form.slug = Url.create_slug()
                slug = form.slug
            else:
                form.slug = slug.lower()
            form.save()
            return None, path + slug
        if not error:
            error = 'Invalid url or slug!'
        return error, None

    def create_slug(self):
        slug = generate(size=5)
        while self.check_slug(slug):
            slug = generate(size=5)
        return slug.lower()

    def check_slug(self, slug):
        if slug:
            if len(Url.objects.filter(slug=slug)) > 0:
                return 'Slug is in use!'
            elif re.sub(r'[\w\-]', '', slug):
                return 'Invalid characters!'
        return None