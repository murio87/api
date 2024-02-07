from django.db import models
from django.db.models.signals import pre_save, post_delete
from django.utils.text import slugify
from django.conf import settings
from django.dispatch import receiver
from PIL import Image
from rest_framework.authtoken.models import Token
from django.db.models.signals import post_save


# to create the location for the image
def upload_location(instance, filename, **kwargs):
    file_path = 'post/{author_id}/{title}-{filename}'.format(
        author_id=str(instance.author.id), title=str(instance.title), filename=filename
    )
    return file_path


def resize_image(image_path, output_size=(200, 250)):
    img = Image.open(image_path)
    img.thumbnail(output_size)
    img.save(image_path)


class BlogPost(models.Model):
    title = models.CharField(max_length=30, null=False, blank=False)
    body = models.TextField(max_length=1000, null=False, blank=False)
    price = models.CharField(max_length=10, null=False, blank=False)
    image = models.ImageField(upload_to=upload_location, null=False, blank=False)
    date_publish = models.DateTimeField(auto_now_add=True, verbose_name='date published')
    date_updated = models.DateTimeField(auto_now=True, verbose_name='date updated')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    slug = models.SlugField(blank=True, unique=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        # Check if the image field is not None
        if self.image:
            # Get the path of the uploaded image
            image_path = self.image.path

            # Resize the image to 200x250 pixels
            resize_image(image_path)

    def __str__(self):
        return self.title


# signal receiver that gets triggered when a BlogPost object is deleted
@receiver(post_delete, sender=BlogPost)
# Delete the associated image file when a BlogPost object is deleted
# The 'False' argument means the image file should not be deleted from the storage immediately
def submission_delete(sender, instance, **kwargs):
    instance.image.delete(False)


# This is a signal receiver that gets triggered before a BlogPost object is saved
def pre_save_blog_post_receiver(sender, instance, *args, **kwargs):
    # BlogPost instance doesn't have a slug a new post, generate one using the author's username and post title
    if not instance.slug:
        instance.slug = slugify(instance.author.username + "-" + instance.title)


# Connect the pre_save_blog_post_receiver function to the pre_save signal of the BlogPost model
pre_save.connect(pre_save_blog_post_receiver, sender=BlogPost)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def created_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
