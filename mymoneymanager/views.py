from django.shortcuts import render, get_object_or_404, get_list_or_404
from .models import Exchange_rate, Document, DocumentItem, Currency
from .forms import NewDocumentForm, NewDocumentItemForm, DocumentForm, DocumentFormSet
from django.contrib.auth.models import User
from django.views.generic import UpdateView
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView
from django.shortcuts import render
from django_tables2 import RequestConfig
from .tables import DocumentTable

from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def home(request):
    all_documents = Document.objects.all()
    return render(request, 'home.html', {'all_documents': all_documents})


def documents_list(request):
    #all_documents = Document.objects.all()
    element_fields = {'number': '#',
                      'document_type': 'Document type',
                      'active': 'Active',
                      'counterparty': 'Counterparty',
                      'wallet': 'Wallet',
                      'currency': 'Currency',
                      'amount': 'Amount',
                      'user': 'User',
                      'comment': 'Comment'}
    queryset = Document.objects.all()
    page = request.GET.get('page', 1)

    paginator = Paginator(queryset, 10)

    try:
        all_documents = paginator.page(page)
    except PageNotAnInteger:
        all_documents = paginator.page(1)
    except EmptyPage:
        all_documents = paginator.page(paginator.num_pages)

    if request.is_ajax():
        data = dict()
        data['html_document_list'] = render_to_string('partial_document_list.html', {
            'all_documents': all_documents, 'element_fields': element_fields
        })
        data['html_pagination'] = render_to_string('includes/pagination_fbv.html', {
            'all_documents': all_documents, 'element_fields': element_fields
        })
        return JsonResponse(data)

    return render(request, 'documents_list.html', {'all_documents': all_documents, 'element_fields': element_fields})


def save_document_form(request, form, template_name, formset=None):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            all_documents = Document.objects.all()
            data['html_document_list'] = render_to_string('partial_document_list.html', {
                'all_documents': all_documents
            })
        else:
            data['form_is_valid'] = False
    context = {'form': form, 'formset': formset}
    data['html_form'] = render_to_string(
        template_name, context, request=request)
    return JsonResponse(data)


def document_create(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST)
    else:
        form = DocumentForm()
    return save_document_form(request, form, 'partial_document_create.html')


def document_update(request, pk):
    document = get_object_or_404(Document, pk=pk)
    if request.method == 'POST':
        form = DocumentForm(request.POST, instance=document)
    else:
        form = DocumentForm(instance=document)
        formset = DocumentFormSet(instance=document)
    return save_document_form(request, form, 'partial_document_update.html', formset)


def document_delete(request, pk):
    document = get_object_or_404(Document, pk=pk)
    data = dict()
    if request.method == 'POST':
        document.delete()
        # This is just to play along with the existing code
        data['form_is_valid'] = True
        all_documents = Document.objects.all()
        data['html_document_list'] = render_to_string('partial_document_list.html', {
            'all_documents': all_documents
        })
    else:
        context = {'document': document}
        data['html_form'] = render_to_string('partial_document_delete.html',
                                             context,
                                             request=request,
                                             )
    return JsonResponse(data)


def currency_list(request):
    element_fields = {'digital_code': 'Code',
                      'name': 'Name',
                      'active': 'Active',
                      'char_code': 'Char code',
                      'upload_rates': 'Upload_rates'}
    queryset = Currency.objects.all()
    page = request.GET.get('page', 1)

    paginator = Paginator(queryset, 10)

    try:
        dictionary_elements = paginator.page(page)
    except PageNotAnInteger:
        dictionary_elements = paginator.page(1)
    except EmptyPage:
        dictionary_elements = paginator.page(paginator.num_pages)

    if request.is_ajax():
        data = dict()
        data['html_dictionary_list'] = render_to_string('partial_dictionary_list.html', {
            'dictionary_elements': dictionary_elements, 'element_fields': element_fields
        })
        data['html_pagination'] = render_to_string('includes/dictionary_pagination.html', {
            'dictionary_elements': dictionary_elements, 'element_fields': element_fields
        })
        return JsonResponse(data)

    return render(request, 'dictionary_list.html', {'dictionary_elements': dictionary_elements, 'element_fields': element_fields})


@login_required
def new_document(request, pk):
    document = get_object_or_404(Document, pk=pk)
    user = User.objects.first()
    if request.method == 'POST':
        pass
        # form = NewDocumentForm(request.POST)
        # if form.is_valid():
        #     topic = form.save(commit=False)
        #     topic.save()
        #     post = Post.objects.create(
        #         message=form.cleaned_data.get('message'),
        #         topic=topic,
        #         created_by=user
        #     )
        #     return redirect('document', pk=document.pk)  # TODO: redirect to the created topic page
    else:
        form = NewDocumentForm()
        itemform = NewDocumentItemForm(auto_id=False)
    return render(request, 'new_document.html', {'form': form, 'itemform': itemform})


@login_required
def documents(request, pk):
    document = get_object_or_404(Document, pk=pk)
    document_table = get_list_or_404(DocumentItem, document=document)
    return render(request, 'document.html', {'document': document, 'document_table': document_table})


class DocumentListView(ListView):
    model = Document
    template_name = 'home.html'
    context_object_name = 'all_documents'
    paginate_by = 10


class DocumentUpdateView(UpdateView):
    model = Document
    fields = ('message', )
    template_name = 'edit_document.html'
    pk_url_kwarg = 'document_pk'
    context_object_name = 'document'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset

    def form_valid(self, form):
        post = form.save(commit=False)
        post.updated_by = self.request.user
        post.updated_at = timezone.now()
        post.save()
        return redirect('topic_posts', pk=post.topic.board.pk, topic_pk=post.topic.pk)
