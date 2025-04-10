from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType

from book.models import FileUpload

moder_group, created = Group.objects.get_or_create(name="Moderator")
permission_book = Permission.objects.get(codename='can_manage_books')
permission_author = Permission.objects.get(codename='can_manage_author')
moder_group.permissions.add(permission_book, permission_author)


def setup_groups_and_permissions():
    admin_group, _ = Group.objects.get_or_create(name='Admin')
    moder_group, _ = Group.objects.get_or_create(name='Moderator')
    user_group, _ = Group.objects.get_or_create(name='User')
    premium_group, _ = Group.objects.get_or_create(name='Premium')

    content_type = ContentType.objects.get_for_model(FileUpload)
    upload_perm = Permission.objects.get(codename='can_upload_file', content_type=content_type)
    view_all_perm = Permission.objects.get(codename='can_view_all_files', content_type=content_type)

    admin_group.permissions.add(upload_perm, view_all_perm)

    moder_group.permissions.add(view_all_perm)

    user_group.permissions.add(upload_perm)