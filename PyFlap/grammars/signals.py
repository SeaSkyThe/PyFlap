from grammars.models import Rule, Grammar

from django.db.models.signals import pre_delete, post_save, post_init
from django.dispatch import receiver



@receiver(pre_delete, sender=Rule)
def signal_1(sender, instance, **kwargs):
    g = Grammar.load()
    g.regex = ""
    g.save()
    
@receiver(post_save, sender=Rule)
def signal_2(sender, instance, created, **kwargs):
    if(created):
        g = Grammar.load()
        g.regex = ""
        g.save()