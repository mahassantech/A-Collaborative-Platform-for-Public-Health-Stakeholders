from .models import UserSubscription

def can_book_appointment(user):
    try:
        sub = UserSubscription.objects.get(user=user)
        return sub.is_valid()
    except UserSubscription.DoesNotExist:
        return False
