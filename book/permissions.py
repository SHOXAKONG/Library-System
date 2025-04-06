from django.contrib.auth.models import Group, Permission


moder_group, created = Group.objects.get_or_create(namme="Moderator")
permission_book = Permission.objects.get(codename='can_manage_books')
permission_author = Permission.objects.get(codename='can_manage_author')
moder_group.permissions.add(permission_book, permission_author)
