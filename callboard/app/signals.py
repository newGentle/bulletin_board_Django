from django.dispatch import receiver 
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from .models import Post, User, Response, PostCategory
from django.conf import settings
from django.shortcuts import get_object_or_404, redirect, HttpResponseRedirect
from django.db.models.signals import post_save, m2m_changed

@receiver(post_save, sender=Response)
def response_emailing(sender, instance, created, **kwarga):
    if created:
        response = instance.response_post
        post = Post.objects.get(pk=response.pk)
        usr = User.objects.get(pk=post.post_author.pk)
        content = f'Вы получили новый отклик на ваше объявление - {settings.SITE_URL}/{response.id}'
        send_mail(subject='Новый отклик', message=content, from_email=settings.DEFAULT_FROM_EMAIL, recipient_list=(usr.email,))
        
@receiver(post_save, sender=Response)
def response_accept_emailing(sender, instance, created, **kwargs):
        if not created:
            response = instance.response_post
            post = Post.objects.get(pk=response.pk)
            # print(User.objects.get(pk=instance.response_author.pk))
            usr = User.objects.get(pk=instance.response_author.pk)
            content = f'Ваш отклик был одобрен на объявление - {settings.SITE_URL}/{post.id}'
            send_mail(subject='Отклик принят', message=content, from_email=settings.DEFAULT_FROM_EMAIL, recipient_list=(usr.email,))

@receiver(m2m_changed, sender=PostCategory)
def subscribers_emailing(sender, instance, **kwargs):
    
    if kwargs['action'] == 'post_add':
        categories = instance.post_category.all()
        subscribers = []
        for cats in categories:
            subscribers += cats.subscribers.all()
            print(subscribers)

        print(subscribers)
        username = [usr.username for usr in subscribers]
        subscribers =[usr.email for usr in subscribers]
        html_content = render_to_string(
            template_name='subscribers_email_notify.html',
            context={
                'text': instance.preview(),
                'post_link': f'{settings.SITE_URL}/{instance.id}',
                'username': username,
            }
        )
        msg = EmailMultiAlternatives(
            subject=instance.post_title,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=subscribers,
        )

        msg.attach_alternative(html_content, 'text/html')
        msg.send()