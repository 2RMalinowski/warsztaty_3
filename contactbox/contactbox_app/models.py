from django.db import models

class Person(models.Model):
    name = models.CharField(max_length=64, default='')
    surname = models.CharField(max_length=64, default='')
    description = models.TextField(null=True, default='')

class Address(models.Model):
    city = models.CharField(max_length=64, default='')
    street = models.CharField(max_length=64, default='')
    house_no = models.CharField(max_length=64, default='')
    flat_no = models.CharField(max_length=64, default='')
    person = models.ForeignKey(Person, on_delete=models.CASCADE)

class Telephone(models.Model):
    tel_no = models.CharField(max_length=64, default='')
    tel_type = models.CharField(max_length=64, default='')
    person = models.ForeignKey(Person, on_delete=models.CASCADE)

class Email(models.Model):
    mail = models.CharField(max_length=64, null=True, default='')
    mail_type = models.CharField(max_length=64, null=True, default='')
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
