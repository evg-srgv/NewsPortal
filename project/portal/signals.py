from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from .models import Post, PostCategory
from django.template.loader import render_to_string
from project import settings


def send_notifications(preview, pk, title, subscriptions):
    html_content = render_to_string(
        'post_created_email.html',
        {
            'text' : preview,
            'link' : f'{settings.SITE_URL}/portal/{pk}' 
        }
    )


    msg = EmailMultiAlternatives(
        subject=title,
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=subscriptions,
    )


    msg.attach_alternative(html_content, 'text/html')
    msg.send()



@receiver(m2m_changed, sender=PostCategory)
def notify_about_new_post(sender, instance, **kwargs):
    if kwargs['action'] == 'post_add':
        categories = instance.category.all()
        subscriptions_emails = []


        for cat in categories:
            subscriptions = cat.subscriptions.all()
            subscriptions_emails += [s.email for s in subscriptions]


        send_notifications(instance.preview(), instance.pk, instance.postTitle,
                           subscriptions_emails)
        