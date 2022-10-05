from django.shortcuts import render
from django.http import HttpResponseRedirect, JsonResponse, Http404
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import UpdateView
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.urls import reverse_lazy
from .forms import *
from .models import SimpleUser, List, Points
from django.shortcuts import get_object_or_404
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.edit import CreateView
from django.views.generic.base import TemplateView
from django.core.signing import BadSignature
from .utilities import signer
from followlist.lib.parsepoint import parse_point
from django.db.models import Q

@login_required
def point_is_done(request):
    if request.method == 'GET':
        type = request.GET['type']
        point_id = request.GET['point_id']
        if type == 'checklist':
            point = Points.objects.get(pk=int(point_id))
        elif type == 'goal':
            point = Goal.objects.get(pk=int(point_id))
        else:
            return Http404

        if point.is_done is False:
            point.is_done = True
        else:
            point.is_done = False

        point.save()

        return JsonResponse({'is_done': point.is_done})

@login_required
def create_goal(request):
    template = 'fowlist/add_goal.html'
    if request.method == 'GET':
        form = CreateGoalForm(initial={'user': request.user.pk})
        context = {'form': form}
        return render(request, template, context=context)
    elif request.method == 'POST':
        form = CreateGoalForm(request.POST)
        if form.is_valid() and request.POST['user'] == str(request.user.pk):
            form.save()
            return HttpResponseRedirect(reverse_lazy('fowlist:profile'))

        form = CreateGoalForm(initial={'user': request.user.pk})
        context = {'form': form, 'errors': 'ошибка'}
        return render(request, template, context=context)

@login_required
def create_checklist(request):
    template = 'fowlist/add_checklist.html'
    if request.method == 'GET':
        form = CreateCheckListForm(initial={'user': request.user.pk})
        context = {'form': form}
        return render(request, template, context=context)
    elif request.method == 'POST':
        list_form = CreateCheckListForm(request.POST)
        if list_form.is_valid() and request.POST['user'] == str(request.user.pk):
            points = request.POST.getlist('point')
            instance = list_form.save()
            pk = instance.pk
            for point in points:
                p = Points()
                p.name_point = point
                p.list_id = int(pk)
                p.save()
            return HttpResponseRedirect(reverse_lazy('fowlist:profile'))
        else:
            context = {'form': list_form}
            return render(request, template, context)


def user_activate(request, sign):
    try:
        username = signer.unsign(sign)
    except BadSignature:
        return render(request, 'fowlist/bad_signature.html')
    user = get_object_or_404(SimpleUser, username=username)
    if user.is_activated:
        template = 'fowlist/user_is_activated.html'
    else:
        template = 'fowlist/activation_done.html'
        user.is_activate = True
        user.is_activated = True
        user.save()

    return render(request, template)


class ChangeEmailUserView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = SimpleUser
    template_name = 'fowlist/change_email.html'
    form_class = ChangeEmailUserForm
    success_url = reverse_lazy('fowlist:profile')
    success_message = 'Успешно изменен e-mail'

    def setup(self, request, *args, **kwargs):
        self.user_id = request.user.pk
        return super().setup(request, *args, **kwargs)

    def get_object(self, queryset=None):
        if not queryset:
            queryset = self.get_queryset()
        return get_object_or_404(queryset, pk=self.user_id)


class RegisterDoneView(TemplateView):
    template_name = 'fowlist/register_done.html'


class RegisterUserView(CreateView):
    model = SimpleUser
    template_name = 'fowlist/registration.html'
    form_class = RegisterUserForm
    success_url = reverse_lazy('fowlist:register-done')


class ChangePasswordView(SuccessMessageMixin, LoginRequiredMixin, PasswordChangeView):
    template_name = 'fowlist/password_change.html'
    success_url = reverse_lazy('fowlist:profile')
    success_message = 'пароль успешно изменен'



@login_required
def profile(request):

    checklist = List.objects.filter(type=1).filter(user=request.user.pk)
    dolist = List.objects.filter(type=2).filter(user=request.user.pk)
    goals = Goal.objects.filter(user=request.user.pk)
    dolist_points = {}
    checklist_points = {}
    for i in checklist:
        points = Points.objects.filter(list=i.pk)
        checklist_points.update({i: points})

    for i in dolist:
        points = Points.objects.filter(list=i.pk)
        dolist_points.update({i: points})

    context = {'checklist': checklist_points.items(), 'dolist': dolist_points.items(), 'goals': goals}

    return render(request, 'fowlist/profile.html', context=context)

@login_required
def all_lists(request):
    template = 'fowlist/all_lists.html'
    q = Q(is_private=False) & ~Q(user__pk=request.user.pk)
    q2 = Q(user__pk=request.user.pk) & Q(original_id__gt=-1)
    lists = List.objects.filter(q).order_by()
    lists2 = List.objects.filter(q2).values('original_id')
    lists2 = list(lists2)
    lists_points = {}
    for l in lists:
        if {'original_id': l.pk} in lists2:
            continue
        points = Points.objects.filter(list=l.pk)
        lists_points.update({(l): points})
    context = {'lists': lists_points.items()}

    return render(request, template, context=context)


def index(request):
    if request.user.pk  is not None:
        return HttpResponseRedirect(reverse_lazy('fowlist:profile'))
    return render(request, 'fowlist/start.html')


@login_required
def fowlist_logout(request):
    logout(request)
    return HttpResponseRedirect('/')


class FowlistLoginView(LoginView):
    form_class = LoginForm
    template_name = 'fowlist/login.html'


@login_required
def add_checklist(request):
    if request.method == "GET":
        pk = int(request.GET["list_pk"])

        checklist = List.objects.filter(pk=pk)
        if checklist.exists() is False:
            return JsonResponse({'is_added': False, 'error': 'Запись не найдена'})

        checklist_added = List()
        checklist_added.user = request.user
        checklist_added.original_id = pk
        checklist_added.is_private = True
        checklist_added.name_list = checklist[0]
        checklist_added.type = checklist[0].type
        checklist_added.save()

        points = Points.objects.filter(list=pk)
        for p in points:
            point = Points()
            point.name_point = p.name_point
            point.list_id = checklist_added.pk
            point.is_done = False
            point.save()

    return JsonResponse({'is_added': 'true'})


@login_required
def delete_list(request):
    if request.method == "GET":
        type = request.GET['type']
        id = int(request.GET['id'])
        if type == 'delete-list':
            entry = List.objects.get(pk=id)
        elif type == 'delete-goal':
            entry = Goal.objects.get(pk=id)
        else:
            return JsonResponse({'is_deleted': 'False'})

        pk_user = entry.user.pk
        if pk_user == request.user.pk:
            entry.delete()
            return JsonResponse({'is_deleted': 'True'})

        return JsonResponse({'is_deleted': 'False'})

@login_required
def get_edit_list(request):
    if request.method == "GET":
        id = int(request.GET['id'])
        entry = List.objects.get(pk=id)
        pk_user = entry.user.pk
        if pk_user == request.user.pk:
            entries_points = Points.objects.filter(list=entry.pk)
            points = {}
            for i in entries_points:
                points.update({i.pk: i.name_point})

            return JsonResponse({"name_list": entry.name_list, "points": points, "list_id": entry.pk})

@login_required
def edit_list(request):
    if request.method == "POST":
        name_list = request.POST['name-list']
        pk_list = request.POST['pklist']
        points = parse_point(request.POST)
        template = 'fowlist/error.html'
        if points != {}:
            if List.objects.filter(pk=pk_list).exists() is False:
                return render(request, template, {'error': 'Не найдет редактируемый список.'})
            entry_list = List.objects.get(pk=pk_list)
            if entry_list.user.pk != request.user.pk:
                return render(request, template, {'error': 'Ошибка! Возможно, вы редактируете чужой список.'})
            entry_list.name_list = name_list
            entries_points = Points.objects.filter(list=pk_list)
            for p in entries_points:
                try:
                    p.name_point = points[p.pk]
                except ValueError:
                    return render(request, template, {'error': 'Ошибка при записи пунктов'})
                p.save()
            return HttpResponseRedirect(reverse_lazy('fowlist:profile'))
    return HttpResponseRedirect(reverse_lazy('fowlist:profile'))