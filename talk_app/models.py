from django.db import models


class Address(models.Model):
    city = models.CharField(
        verbose_name='City',
        max_length=60)
    street = models.CharField(
        verbose_name='Street',
        max_length=60)
    house_number = models.PositiveSmallIntegerField(
        verbose_name='House number')
    apartment_number = models.PositiveSmallIntegerField(
        verbose_name='Apartment number',
        null=True,
        blank=True)

    def __str__(self):
        if self.apartment_number:
            return self.city + ' ' + self.street + ' ' + str(self.house_number) + '/' + str(self.apartment_number)
        return self.city + ' ' + self.street + ' ' + str(self.house_number)

    class Meta:
        verbose_name = 'Address'
        verbose_name_plural = 'Addresses'


class Person(models.Model):
    name = models.CharField(
        verbose_name='Name',
        max_length=33)
    surname = models.CharField(
        verbose_name='Surname',
        max_length=33)
    description = models.TextField(
        verbose_name='Description')
    address = models.ForeignKey(
        Address,
        verbose_name='Address',
        on_delete=models.SET_NULL,
        null=True,)

    def __str__(self):
        return self.surname + ' ' + self.name

    class Meta:
        verbose_name = 'Person'
        verbose_name_plural = 'Persons'


class Phone(models.Model):

    person = models.ForeignKey(
        Person,
        verbose_name='Owner',
        on_delete=models.SET_NULL,
        null=True)
    number = models.PositiveSmallIntegerField(
        verbose_name='Phone number')
    type = models.CharField(
        verbose_name='Type',
        max_length=20)


    def __str__(self):
        return self.type + ': ' + str(self.number)

    class Meta:
        verbose_name = 'Phone number'
        verbose_name_plural = 'Phone numbers'


class Email(models.Model):

    person = models.ForeignKey(
        Person,
        verbose_name='Owner',
        on_delete=models.SET_NULL,
        null=True)
    email = models.EmailField(
        verbose_name='Email')
    type = models.CharField(
        verbose_name='Type',
        max_length=20)

    def __str__(self):
        return self.type + ': ' + self.email

    class Meta:
        verbose_name = 'Email'
        verbose_name_plural = 'Emails'


class Group(models.Model):
    name = models.CharField(
        verbose_name='Group name',
        max_length=60)
    person = models.ManyToManyField(
        Person,
        verbose_name='Group member')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Group'
        verbose_name_plural = 'Groups'
