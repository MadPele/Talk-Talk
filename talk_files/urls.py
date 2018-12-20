from django.contrib import admin
from django.urls import path
from talk_app.views import Home, Add_person, show_person, delete_person, Edit_person, Add_email, delete_email, Add_phone,\
    delete_phone, Add_address, delete_address, Create_group, Show_group, delete_member, show_all_groups

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', Home.as_view(), name='home'),
    path('new', Add_person.as_view(), name='add_person'),
    path('show/<int:person_id>', show_person, name='show_person'),
    path('delete/<int:person_id>', delete_person, name='delete_person'),
    path('addEmail/<int:person_id>', Add_email.as_view(), name='add_email'),
    path('addPhone/<int:person_id>', Add_phone.as_view(), name='add_phone'),
    path('addAddress/<int:person_id>', Add_address.as_view(), name='add_address'),
    path('deleteEmail/<int:email_id>', delete_email, name='delete_email'),
    path('deletePhone/<int:phone_id>', delete_phone, name='delete_phone'),
    path('deleteAddress/<int:person_id>', delete_address, name='delete_address'),
    path('edit/<int:person_id>', Edit_person.as_view(), name='edit_person'),
    path('createGroup', Create_group.as_view(), name='create_group'),
    path('showGroup/<int:group_id>', Show_group.as_view(), name='show_group'),
    #path('showGroup/<int:group_id>/<members>', Show_group.as_view(), name='show_group'),
    path('show_all_groups', show_all_groups, name='show_all_groups'),
    path('deleteMember/<int:group_id>/<int:member_id>', delete_member, name='delete_member'),

]
