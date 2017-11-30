from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from contactbox_app.models import *


def contact_book(request):
    if request.method == 'GET':
        html = ''''''
        contacts = Person.objects.order_by('surname')
        for per in contacts:
            html += '''
            <html><body>
                <tr>
                    <td><a href="/show_contact/{}">{} {}</a></td>
                    <td><form action="/edit/{}" style="display:inline">
                        <input type="submit" value="edit">
                    </form></td>
                    <td><form action="/del_contact/{}" style="display:inline">
                        <input type="submit" value="del">
                    </form></td>
                </tr>
            </body></html>
            '''.format(per.id,
                       per.name,
                       per.surname,
                       per.id,
                       per.id)

        table = '''
            <table>
                <tr>
                    <th>My contacts:</th>
                    <th></th>
                    <th></th>
                </tr>
                {}
            </table><br><br>
            <form action="/add_contact">
                <input type="submit" value="add contact">
            </form>
        '''.format(html)

        return HttpResponse(table)


def add_contact(request):
    if request.method == 'GET':
        html = '''
        <html><body>
            <form action="#" method="POST" style="display:inline">
                <label>Name:
                    <input type="text" name="name" placeholder="first name">
                </label>
                <label>Surname:
                    <input type="text" name="surname" placeholder="last name">
                </label>
                <input type="submit" value="add">
            </form>
            <form action="/contact_book" style="display:inline">
                <input type="submit" value="cancel">
            </form>
        </p></body>
            '''
        return HttpResponse(html)

    else:
        name = request.POST.get("name")
        surname = request.POST.get("surname")
        p = Person.objects.create(name=name, surname=surname)
        Address.objects.create(person_id=p.id)
        Telephone.objects.create(person_id=p.id)
        Email.objects.create(person_id=p.id)

        return HttpResponseRedirect('/show_contact/{}'.format(p.id))


def show_contact(request, id):
    p = Person.objects.get(pk=int(id))
    a = Address.objects.filter(person_id=int(id))
    t = Telephone.objects.filter(person_id=int(id))
    e = Email.objects.filter(person_id=int(id))
    addresses = ''''''
    telephones = ''''''
    emails = ''''''
    for add in a:
        addresses += "{}, {} {}/{}<br>".format(add.city,
                                               add.street,
                                               add.house_no,
                                               add.flat_no)
    for tel in t:
        telephones += "{} - {}<br>".format(tel.tel_no,
                                           tel.tel_type)
    for email in e:
        emails += "{} - {}<br>".format(email.mail,
                                       email.mail_type)

    html = '''
    <p><body>
        <table>
            <tr>
                <th>Name:</th>
                <td>{} {}</td>
            </tr>
            <tr>
                <th>Description:</th>
                <td>{}</td>
            </tr>
            <tr>
                <th>Address:</th>
                <td>{}</td>
            </tr>
            <tr>
                <th>Telephone:</th>
                <td>{}</td>
            </tr>
            <tr>
                <th>Email:</th>
                <td>{}</td>
            </tr>
        </table><br><br>
        <form action="/edit/{}" style="display:inline">
            <input type="submit" value="modify">
        </form>
        <form action="/contact_book" style="display:inline">
            <input type="submit" value="back">
        </form>
    </p></body>
    '''.format(p.name,
               p.surname,
               p.description,
               addresses,
               telephones,
               emails,
               p.id)

    return HttpResponse(html)


def edit_contact(request, id):
    if request.method == 'GET':
        html = """
        <p><body>
            <form action="" method="POST" style="display:inline">
                <b>Popraw dane:</b><br><br>
                <table>
                    <tr>
                        <th>Name:</th>
                        <td><input type="text" name="first_name" value='{}'
                            placeholder="first name"></td>
                    </tr>
                    <tr>
                        <th>Surname:</th>
                        <td><input type="text" name="last_name" value='{}'
                            placeholder="last name"></td>
                    </tr>
                    <tr>
                        <th>Description:</th>
                        <td><input type="text" name="description" value='{}'
                            placeholder="description"></td>
                    </tr>
                    {}
                    {}
                    {}
                </table><br>
                <input type="submit" value="accept changes">
            </form>|
            <form action="/{}/addaddress" method="GET" style="display:inline">
                <input type='submit' value='add new address'>
            </form>
            <form action="/{}/addtelephone" method="GET" style="display:inline">
                <input type='submit' value='add new telephone'>
            </form>
            <form action="/{}/addemail" method="GET" style="display:inline">
                <input type='submit' value='add new email'>
            </form>
        </p></body>
        """

        back = '''
            <br><br><form action="/contact_book/" method="GET">
                <input type='submit' value='cancel'>
            </form>
        '''

        p = Person.objects.get(pk=int(id))
        a = Address.objects.filter(person_id=int(id))
        t = Telephone.objects.filter(person_id=int(id))
        e = Email.objects.filter(person_id=int(id))
        addresses = ''''''
        telephones = ''''''
        emails = ''''''
        for add in a:
            addresses += '''
                <tr>
                    <th>Addresss:</th>
                    <td><input type="text" name="city{}" value='{}'
                        placeholder="city"></td>
                    <td><input type="text" name="street{}" value='{}'
                        placeholder="street"></td>
                    <td><input type="text" name="home_no{}" value='{}'
                        placeholder="house number"></td>
                    <td><input type="text" name="flat_no{}" value='{}'
                        placeholder="flat number"></td>
                </tr>'''.format(str(add.id),
                                add.city,
                                str(add.id),
                                add.street,
                                str(add.id),
                                add.house_no,
                                str(add.id),
                                add.flat_no)

        for tel in t:
            telephones += '''
                <tr>
                    <th>Telephone:</th>
                    <td><input type="text" name="tel{}" value='{}'
                        placeholder="tel number"></td>
                    <td><input type="text" name="tel_type{}" value='{}'
                        placeholder="tel type"></td>
                </tr>'''.format(str(tel.id),
                                tel.tel_no,
                                str(tel.id),
                                tel.tel_type)
        for email in e:
            emails += '''
                <tr>
                    <th>Email:</th>
                    <td><input type="text" name="email{}" value='{}'
                        placeholder="email"></td>
                    <td><input type="text" name="email_type{}" value='{}'
                        placeholder="email type"></td>
                </tr>'''.format(str(email.id),
                                email.mail,
                                str(email.id),
                                email.mail_type)

        return HttpResponse(html.format(p.name,
                                        p.surname,
                                        p.description,
                                        addresses,
                                        telephones,
                                        emails,
                                        p.id,
                                        p.id,
                                        p.id)
                                        + back)

    else:
        p = Person.objects.get(pk=int(id))
        add = Address.objects.filter(person_id=int(id))
        tel = Telephone.objects.filter(person_id=int(id))
        email = Email.objects.filter(person_id=int(id))

        p.name = request.POST.get('first_name')
        p.surname = request.POST.get('last_name')
        p.description = request.POST.get('description')
        p.save()

        for a in add:
            a.city = request.POST.get('city{}'.format(a.id))
            a.street = request.POST.get('street{}'.format(a.id))
            a.house_no = request.POST.get('home_no{}'.format(a.id))
            a.flat_no = request.POST.get('flat_no{}'.format(a.id))
            a.save()
        for t in tel:
            t.tel_no = request.POST.get('tel{}'.format(t.id))
            t.tel_type = request.POST.get('tel_type{}'.format(t.id))
            t.save()
        for e in email:
            e.mail = request.POST.get('email{}'.format(e.id))
            e.mail_type = request.POST.get('email_type{}'.format(e.id))
            e.save()

        back = '''
            <form action="/contact_book/" method="GET">
                <input type='submit' value='return home'>
            </form>
        '''
        return HttpResponse('Changes have been made<br><br>' + back)


def del_contact(request, id):
    per = Person.objects.get(pk=id)
    per.delete()
    back = '''
        <form action="/contact_book/" method="GET">
            <input type='submit' value='return home'>
        </form>
    '''
    return HttpResponse('Person successfully deleted<br><br>' + back)


def add_address(request, id):
    id = int(id)
    if request.method == 'GET':
        html = '''
        <p><body>
            <form action="#" method="POST" style="display:inline">
                <table>
                    <tr>
                        <th>Addresss:</th>
                        <td><input type="text" name="city" value=''
                            placeholder="city"></td>
                        <td><input type="text" name="street" value=''
                            placeholder="street"></td>
                        <td><input type="text" name="home_no" value=''
                            placeholder="house number"></td>
                        <td><input type="text" name="flat_no" value=''
                            placeholder="flat number"></td>
                    </tr>
                </table><br>
                <input type="submit" value="add">
            </form>
            <form action="/contact_book" style="display:inline">
                <input type="submit" value="cancel">
            </form>
        </p></body>
                '''
        return HttpResponse(html)

    else:
        Address.objects.create(person_id=id,
                               city=request.POST.get('city'),
                               street=request.POST.get('street'),
                               house_no=request.POST.get('home_no'),
                               flat_no=request.POST.get('flat_no'))

        return HttpResponseRedirect('/show_contact/{}'.format(id))


def add_telephone(request, id):
    id = int(id)
    if request.method == 'GET':
        html = '''
        <p><body>
            <form action="#" method="POST" style="display:inline">
                <table>
                    <tr>
                        <th>Telephone:</th>
                        <td><input type="text" name="tel_num" value=''
                            placeholder="number"></td>
                        <td><input type="text" name="tel_type" value=''
                            placeholder="type"></td>
                    </tr>
                </table><br>
                <input type="submit" value="add">
            </form>
            <form action="/contact_book" style="display:inline">
                <input type="submit" value="cancel">
            </form>
        </p></body>
            '''
        return HttpResponse(html)

    else:
        Telephone.objects.create(person_id=id,
                                 tel_no=request.POST.get('tel_num'),
                                 tel_type=request.POST.get('tel_type'))

        return HttpResponseRedirect('/show_contact/{}'.format(id))


def add_email(request, id):
    id = int(id)
    if request.method == 'GET':
        html = '''
        </p></body>
            <form action="#" method="POST" style="display:inline">
                <table>
                    <tr>
                        <th>Email:</th>
                        <td><input type="text" name="email" value=''
                            placeholder="mail"></td>
                        <td><input type="text" name="email_type" value=''
                            placeholder="mail type"></td>
                    </tr>
                </table><br>
                <input type="submit" value="add">
            </form>
            </form>
            <form action="/contact_book" style="display:inline">
                <input type="submit" value="cancel">
            </form>
        <p><body>
            '''
        return HttpResponse(html)

    else:
        Email.objects.create(person_id=id, mail=request.POST.get('email'), mail_type=request.POST.get('email_type'))

        return HttpResponseRedirect('/show_contact/{}'.format(id))