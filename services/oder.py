from django.db import transaction
from datetime import datetime
from db.models import Order, Ticket, User


@transaction.atomic
def create_order(tickets, username, date=None):

    user = User.objects.get(username=username)
    order = Order(user=user)

    if date is not None:
        if isinstance(date, str):
            order.created_at = datetime.strptime(date, "%Y-%m-%d %H:%M")
        else:
            order.created_at = date

    order.save()

    for ticket_data in tickets:
        Ticket.objects.create(
            row=ticket_data["row"],
            seat=ticket_data["seat"],
            movie_session_id=ticket_data["movie_session"],
            order=order
        )

    return order


def get_orders(username=None):
    queryset = Order.objects.all()

    if username is not None:
        queryset = queryset.filter(user__username=username)

    return queryset
