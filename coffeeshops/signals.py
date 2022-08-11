from django.core.mail import send_mail
from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save, post_delete
from coffeeshops.models import CafeOwner
from django.template.defaultfilters import slugify
from utils import create_slug
from .models import CoffeeShop,CoffeeShopAddress

@receiver(post_save, sender=CafeOwner)
def send_new_owner_email(sender, instance, created, **kwargs):
    if created==True:
     send_mail(
        subject='Subject here',
        message='Here is the message.',
        from_email='from@example.com',
        recipient_list= ['to@example.com'],
        )


@receiver(pre_save, sender=CoffeeShop)
def slugify_coffee_shop(instance,*args, **kwargs):
  if not instance.slug:
        instance.slug=create_slug(instance)
       
       
@receiver(post_save, sender=CoffeeShop )        
def add_default_address(sender,instance,created, **kwargs):
    if created==True and instance.location is None:
       location= CoffeeShopAddress.objects.create()
       instance.location= location
       instance.save()

@receiver(post_delete, sender=CoffeeShopAddress)
def restore_default_address (sender, instance, **kwargs):
    deletecoffee= instance.coffee_shop
    address = CoffeeShopAddress.objects.create()
    deletecoffee.location=address
    deletecoffee.save()
    
