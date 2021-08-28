from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponseForbidden
from django.shortcuts import get_object_or_404, render, redirect
from django.views.decorators.http import require_safe, require_http_methods

from snippets.forms import SnippetFrom
from snippets.models import Snippet



@require_safe
def top(request):
    snippets = Snippet.objects.all()
    context = {'snippets': snippets}
    return render(request, 'snippets/top.html', context)

@login_required
@require_http_methods(['GET', 'POST', 'HEAD'])
def snippet_new(request):
    if request.method == 'POST':
        form = SnippetFrom(request.POST)
        if form.is_valid():
            snippet = form.save(commit=False)
            snippet.created_by = request.user
            snippet.save()
            return redirect('snippets:snippet_detail', snippet_id=snippet.pk)
    else:
        form = SnippetFrom()
    return render(request, 'snippets/snippet_new.html', {'form': form})


def snippet_edit(request, snippet_id):
    snippet = get_object_or_404(Snippet, pk=snippet_id)
    if snippet.created_by_id != request.user.id:
        return HttpResponseForbidden('このスニペットの編集は許可されていません。')

    if request.method == 'POST':
        form = SnippetFrom(request.POST, instance=snippet)
        if form.is_valid():
            form.save()
            return redirect('snippets:snippet_detail', snippet_id=snippet.pk)
    else:
        form = SnippetFrom(instance=snippet)
    return render(request, 'snippets/snippet_edit.html', {'form': form})


def snippet_detail(request, snippet_id):
    snippet = get_object_or_404(Snippet, pk=snippet_id)
    return render(request, 'snippets/snippet_detail.html', {'snippet': snippet})
