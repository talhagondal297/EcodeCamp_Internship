from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from contacts.models import Contact
from contacts.forms import ContactForm
from django.db.models.functions import Lower
from django.db.models import Q

def contact_list(request):
    query = request.GET.get('q')
    if query:
        contacts = Contact.objects.filter(
            Q(first_name__icontains=query) | 
            Q(last_name__icontains=query) | 
            Q(phone__icontains=query)
        ).order_by(Lower('first_name'), Lower('last_name'))
    else:
        contacts = Contact.objects.all().order_by(Lower('first_name'), Lower('last_name'))
    return render(request, 'contacts/contact_list.html', {'contacts': contacts})


def contact_create(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            phone = form.cleaned_data['phone']

            # Check if phone number already exists
            existing_contact = Contact.objects.filter(phone=phone).first()
        
            if existing_contact:
                form.add_error('phone', 'Contact with this Phone already exists.')
                return render(request, 'contacts/contact_form.html', {'form': form})

            # Check if a contact with the same name already exists
            existing_contact_with_same_name = Contact.objects.filter(
                first_name=first_name, last_name=last_name
            ).first()

            if existing_contact_with_same_name:
                # Add data to the session to handle confirmation on the frontend
                request.session['contact_to_replace'] = existing_contact_with_same_name.pk
                request.session['new_phone'] = phone
                return render(request, 'contacts/confirm_replace.html', {
                    'contact': existing_contact_with_same_name,
                    'new_phone': phone
                })
            
            # Save the new contact
            form.save()
            messages.success(request, 'Contact added successfully.')
            return redirect('contact_list')
    else:
        form = ContactForm()

    return render(request, 'contacts/contact_form.html', {'form': form})


def contact_update(request, pk):
    contact = get_object_or_404(Contact, pk=pk)
    if request.method == "POST":
        form = ContactForm(request.POST, instance=contact)
        if form.is_valid():
            form.save()
            messages.success(request, "Contact updated successfully.")
            return redirect('contact_list')
    else:
        form = ContactForm(instance=contact)
    return render(request, 'contacts/contact_form.html', {'form': form})

def contact_delete(request, pk):
    contact = get_object_or_404(Contact, pk=pk)
    if request.method == "POST":
        contact.delete()
        messages.success(request, "Contact deleted successfully.")
        return redirect('contact_list')
    return render(request, 'contacts/contact_confirm_delete.html', {'contact': contact})

def confirm_update(request, pk):
    contact = get_object_or_404(Contact, pk=pk)
    if request.method == "POST":
        action = request.POST.get('action')
        if action == 'yes':
            form = ContactForm(request.POST, instance=contact)
            if form.is_valid():
                form.save()
                messages.success(request, "Contact updated successfully.")
            return redirect('contact_list')
        elif action == 'no':
            form = ContactForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "Contact added successfully.")
            return redirect('contact_list')
    else:
        form = ContactForm(instance=contact)
    return render(request, 'contacts/contact_confirm_update.html', {'form': form, 'contact': contact})

def contact_replace(request):
    if request.method == "POST":
        if request.POST.get('confirm') == 'yes':
            contact_id = request.session.get('contact_to_replace')
            new_phone = request.session.get('new_phone')
            contact = get_object_or_404(Contact, pk=contact_id)
            contact.phone = new_phone
            contact.save()
            messages.success(request, 'Contact updated successfully.')
        else:
            # Add new contact with the same name but a different phone number
            first_name = Contact.objects.get(pk=request.session.get('contact_to_replace')).first_name
            last_name = Contact.objects.get(pk=request.session.get('contact_to_replace')).last_name
            new_phone = request.session.get('new_phone')

            # Create a new contact with the same name but different phone number
            Contact.objects.create(first_name=first_name, last_name=last_name, phone=new_phone)
            messages.success(request, 'New contact added successfully with the same name.')

        # Clear session data
        request.session.pop('contact_to_replace', None)
        request.session.pop('new_phone', None)

    return redirect('contact_list')