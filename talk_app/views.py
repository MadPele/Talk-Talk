from django.shortcuts import render
from django.views import View
from .models import Phone, Person, Group, Email, Address
from django.shortcuts import redirect
from django.urls import reverse
from django.db.models import Q


class Home(View):

    def get(self, request):

        persons = Person.objects.all().order_by('name')
        return render(request, 'home.html', {'persons': persons})

    def post(self, request):

        pass


class Add_person(View):

    def get(self, request):
        return render(request, 'add_person.html')

    def post(self, request):
        name = request.POST.get('name')
        surname = request.POST.get('surname')
        description = request.POST.get('description')

        new = Person.objects.create(name=name.capitalize(), surname=surname.capitalize(), description=description)
        person_id = new.id

        return redirect(reverse('show_person', kwargs={'person_id': person_id}))


def show_person(request, person_id):

    person = Person.objects.get(pk=person_id)
    phones = Phone.objects.filter(person__pk=person_id)
    emails = Email.objects.filter(person__pk=person_id)
    return render(request, 'show_person.html', {'person': person, 'phones': phones, 'emails': emails})


def delete_person(request, person_id):

    person = Person.objects.get(pk=person_id)
    person.delete()
    return redirect(reverse('home'))


class Edit_person(View):

    def get(self, request, person_id):

        person = Person.objects.get(pk=person_id)
        phones = Phone.objects.filter(person__pk=person_id)
        emails = Email.objects.filter(person__pk=person_id)
        return render(request, 'edit_person.html', {'person': person, 'phones': phones, 'emails': emails})

    def post(self, request, person_id):
        person = Person.objects.get(pk=person_id)
        if request.POST.get('name'):
            person.name = request.POST.get('name')
        if request.POST.get('surname'):
            person.surname = request.POST.get('surname')
        if request.POST.get('description'):
            person.description = request.POST.get('description')


        person.save()

        return redirect(reverse('show_person', kwargs={'person_id': person_id}))


class Add_email(View):

    def get(self, request, person_id):

        person = Person.objects.get(pk=person_id)
        return render(request, 'add_email.html', {'person': person})

    def post(self, request, person_id):

        person = Person.objects.get(pk=person_id)
        email = request.POST.get('email')
        type = request.POST.get('type')

        Email.objects.create(person=person, email=email, type=type)

        return redirect(reverse('edit_person', kwargs={'person_id': person_id}))


def delete_email(request, email_id):

    email = Email.objects.get(pk=email_id)
    person_id = email.person.id
    email.delete()

    return redirect(reverse('edit_person', kwargs={'person_id': person_id}))


class Add_phone(View):

    def get(self, request, person_id):

        person = Person.objects.get(pk=person_id)
        return render(request, 'add_phone.html', {'person': person})

    def post(self, request, person_id):

        person = Person.objects.get(pk=person_id)
        number = request.POST.get('number')
        type = request.POST.get('type')

        Phone.objects.create(person=person, number=number, type=type)

        return redirect(reverse('edit_person', kwargs={'person_id': person_id}))


def delete_phone(request, phone_id):

    phone = Phone.objects.get(pk=phone_id)
    person_id = phone.person.id
    phone.delete()

    return redirect(reverse('edit_person', kwargs={'person_id': person_id}))


class Add_address(View):

    def get(self, request, person_id):

        person = Person.objects.get(pk=person_id)
        return render(request, 'add_address.html', {'person': person})

    def post(self, request, person_id):

        person = Person.objects.get(pk=person_id)
        city = request.POST.get('city')
        street = request.POST.get('street')
        house = request.POST.get('house')
        if request.POST.get('apartment'):
            apartment = request.POST.get('apartment')
            address = Address.objects.create(city=city, street=street, house_number=house, apartment_number=apartment)
        else:
            address = Address.objects.create(city=city, street=street, house_number=house)
        person.address = address
        person.save()

        return redirect(reverse('edit_person', kwargs={'person_id': person_id}))


def delete_address(request, person_id):

    person = Person.objects.get(pk=person_id)
    person_id = person.id
    address = Address.objects.get(person__id=person_id)
    address.delete()

    return redirect(reverse('edit_person', kwargs={'person_id': person_id}))


class Create_group(View):

    def get(self, request):

        return render(request, 'create_group.html')

    def post(self, request):

        name = request.POST.get('name')

        group = Group.objects.create(name=name)
        group_id = group.id

        return redirect(reverse('show_group', kwargs={'group_id': group_id}))


class Show_group(View):

    def get(self, request, group_id):

        group = Group.objects.get(pk=group_id)

        if request.GET.get('search'):
            search = request.GET.get('search')
            search = search.split(' ')
            s_member = []

            for word in search:
                s_member.append(word.capitalize())

            members = group.person.filter(Q(name__in=s_member) | Q(surname__in=s_member))
            #members = group.person(name__in=s_member) | group.person(surname__in=s_member)
        else:
            members = group.person.all()
        memberss = group.person.all()
        persons = Person.objects.exclude(id__in=memberss)

        return render(request, 'show_group.html', {'group': group, 'members': members, 'persons': persons})

    def post(self, request, group_id):

        person_id = request.POST.get('person')
        person = Person.objects.get(pk=person_id)
        group = Group.objects.get(pk=group_id)

        group.person.add(person)
        group.save()

        return redirect(reverse('show_group', kwargs={'group_id': group_id}))


def delete_member(request, group_id, member_id):

    person = Person.objects.get(pk=member_id)
    group = Group.objects.get(pk=group_id)
    group.person.remove(person)

    return redirect(reverse('show_group', kwargs={'group_id': group_id}))


def show_all_groups(request):

    groups = Group.objects.all()

    return render(request, 'show_all_groups.html', {'groups': groups})
