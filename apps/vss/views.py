from django.shortcuts import redirect
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, FormView
from apps.users.models import Person, CustomerShippingAddress
from apps.firm.models import FirmPerson
from apps.firm.forms import FirmPersonAddressForm, FirmAddressForm
from apps.users.forms import PersonAddressForm, CustomerShippingAddressForm, UpdateLanguageForm


vss_home = [
    {
        "label": "Home",
        "url": reverse_lazy("vss:vss_home"),
    },
]


class ThemeContextData:
    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context["theme_name"] = "light"
        return context


class ComponentView(LoginRequiredMixin, ThemeContextData, TemplateView):
    template_name = "vss/components.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context["breadcrumbs"] = [
            {
                "label": "Home",
                "url": "/"
            },
            {
                "label": "Components"
            },
        ]
        return context


class AccountView(LoginRequiredMixin, ThemeContextData, TemplateView):
    template_name = "vss/customer_portal/views/account.html"

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        person = Person.objects.filter(person_no=self.request.user.customer_number).first()
        firm_person = FirmPerson.objects.filter(person_no=self.request.user).first()
        context["title"] = _('Welcome {username}').format(username=self.request.user.get_display_name())
        context["active_tab"] = "vss_account"
        context["breadcrumbs"] = vss_home + [
            {
                "label": "Account"
            },
        ]
        context["membership"] = self.request.user.get_membership(person) if person else None
        context["magazine_suv"] = self.request.user.get_magazine_suv(person) if person else None
        context["firm_address"] = firm_person
        if firm_person:
            context["invoice_billing_address"] = firm_person.firm_no if firm_person.firm_no.active else self.request.user
        context["private_address"] = person
        context["shipping_address"] = self.request.user.customershippingaddress_set.first()
        return context


class AccountEditView(LoginRequiredMixin, ThemeContextData, FormView):
    template_name = "vss/customer_portal/views/account_edit.html"
    success_url = reverse_lazy("vss:vss_account")

    def dispatch(self, request, *args, **kwargs):
        # Check if form class is available before processing the view
        if self.get_form_class() is None:
            return HttpResponseRedirect(reverse('vss:vss_account'))
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = _('Edit address')
        context["active_tab"] = "vss_account"
        context["type"] = self.request.GET.get('type')
        context["breadcrumbs"] = vss_home + [
            {
                "label": "Account",
                "url": reverse_lazy("vss:vss_account")
            },
            {
                "label": "Edit"
            },
        ]
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        request_type = self.request.GET.get('type')
        try:
            firm_person = FirmPerson.objects.get(person_no=self.request.user)
            if request_type == 'firm_address':
                kwargs['instance'] = firm_person
            elif request_type == 'billing_address':
                kwargs['instance'] = firm_person.firm_no
            elif request_type == 'private_address':
                kwargs['instance'] = Person.objects.filter(person_no=self.request.user.customer_number).first()
            elif request_type == 'delivery_address':
                kwargs['instance'] = CustomerShippingAddress.objects.filter(person_no=self.request.user.customer_number).first()
        except Exception as e:
            pass
        return kwargs

    def get_form_class(self):
        request_type = self.request.GET.get('type')
        if request_type == 'firm_address':
            return FirmPersonAddressForm
        elif request_type == 'billing_address':
            return FirmAddressForm
        elif request_type == 'private_address':
            return PersonAddressForm
        elif request_type == 'delivery_address':
            return CustomerShippingAddressForm
        return None

    def form_valid(self, form):
        form.save() # save the form
        return super().form_valid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)


class UpdateLanguageView(LoginRequiredMixin, FormView):
    template_name = "vss/customer_portal/views/language_edit.html"
    success_url = reverse_lazy("vss:vss_account")
    form_class = UpdateLanguageForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = _('Edit Language')
        context["active_tab"] = "vss_account"
        context["breadcrumbs"] = [
            {"label": "Account", "url": reverse_lazy("vss:vss_account")},
            {"label": "Edit Language"}
        ]
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['instance'] = self.request.user  # Pass customer instance to the form
        return kwargs

    def form_valid(self, form):
        customer = form.save()
        Person.objects.filter(customer_number=customer.customer_number).update(language_code=customer.language_code)

        return super().form_valid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)

class AccountEventsView(LoginRequiredMixin, ThemeContextData, TemplateView):
    template_name = "vss/customer_portal/views/account_events.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = _('My events')
        context["active_tab"] = "vss_account_events"
        context["breadcrumbs"] = vss_home + [
            {
                "label": _("My events")
            },
        ]
        return context


class AccountEventDetailUpcomingView(LoginRequiredMixin, ThemeContextData, TemplateView):
    template_name = "vss/customer_portal/views/account_event_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = _('Networking event mobility')
        context["active_tab"] = "vss_account_events"
        context["breadcrumbs"] = vss_home + [
            {
                "label": _("My events"),
                "url": reverse_lazy("vss:vss_account_events")
            },
            {
                "label": _("Future"),
            },
            {
                "label": _("Networking event mobility"),
            },
        ]
        return context


class AccountEventDetailUpcoming2View(LoginRequiredMixin, ThemeContextData, TemplateView):
    template_name = "vss/customer_portal/views/account_event_detail_2.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = _('Networking event mobility')
        context["active_tab"] = "vss_account_events"
        context["breadcrumbs"] = vss_home + [
            {
                "label": _("My events"),
                "url": reverse_lazy("vss:vss_account_events")
            },
            {
                "label": _("Future"),
            },
            {
                "label": _("Networking event mobility"),
            },
        ]
        return context


class AccountEventDetailRunningView(LoginRequiredMixin, ThemeContextData, TemplateView):
    template_name = "vss/customer_portal/views/account_event_detail_running.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = _('Networking event mobility')
        context["active_tab"] = "vss_account_event"
        context["breadcrumbs"] = vss_home + [
            {
                "label": _("My events"),
                "url": reverse_lazy("vss:vss_account_events")
            },
            {
                "label": _("Networking event mobility"),
            },
        ]
        return context


class AccountEventDetailPastView(LoginRequiredMixin, ThemeContextData, TemplateView):
    template_name = "vss/customer_portal/views/account_event_detail_past.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = _('Networking event mobility')
        context["active_tab"] = "vss_account_event"
        context["breadcrumbs"] = vss_home + [
            {
                "label": _("My events"),
                "url": reverse_lazy("vss:vss_account_events")
            },
            {
                "label": _("Networking event mobility"),
            },
        ]
        return context


class EventSignupUsersView(LoginRequiredMixin, ThemeContextData, TemplateView):
    template_name = "vss/customer_portal/views/event_users_signup.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = _('Networking event mobility')
        context["active_tab"] = "vss_account_event"
        context["breadcrumbs"] = vss_home + [
            {
                "label": _("My events"),
                "url": reverse_lazy("vss:vss_account_events")
            },
            {
                "label": _("Networking event mobility"),
            },
        ]
        return context


class ManageAccessView(LoginRequiredMixin, ThemeContextData, TemplateView):
    template_name = "vss/customer_portal/views/manage_access.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = _('Manage access')
        context["active_tab"] = "vss_manage_access"
        context["breadcrumbs"] = vss_home + [
            {
                "label": _('Manage access')
            },
        ]
        return context


class ManageAccessAddView(LoginRequiredMixin, ThemeContextData, TemplateView):
    template_name = "vss/customer_portal/views/manage_access_add.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = _('Create new access')
        context["active_tab"] = "vss_manage_access"
        context["breadcrumbs"] = vss_home + [
            {
                "label": _("Manage Access"),
                "url": reverse_lazy("vss:vss_manage_access")
            },
            {
                "label": _("Add")
            },
        ]
        return context


class PublicationsListView(LoginRequiredMixin, ThemeContextData, TemplateView):
    template_name = "vss/customer_portal/views/publications.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = _('My publications')
        context["active_tab"] = "vss_account_publications"
        context["breadcrumbs"] = vss_home + [
            {
                "label": _('My publications')
            },
        ]
        return context


class PublicationView(LoginRequiredMixin, ThemeContextData, TemplateView):
    template_name = "vss/customer_portal/views/publication_view.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = _('Passive safety in the road space - railings')
        context["active_tab"] = "vss_account_publications"
        context["breadcrumbs"] = vss_home + [
            {
                "label": _("My publications"),
                "url": reverse_lazy("vss:vss_account_publications")
            },
            {
                "label": _("Passive safety in the road space - railings")
            },
        ]
        return context


class PublicationNotesView(LoginRequiredMixin, ThemeContextData, TemplateView):
    template_name = "vss/customer_portal/views/publication_notes.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = _('My notes')
        context["active_tab"] = "vss_account_publications_notes"
        context["breadcrumbs"] = vss_home + [
            {
                "label": _("My publications"),
                "url": reverse_lazy("vss:vss_account_publications")
            },
            {
                "label": _("Notes")
            },
        ]
        return context


class VSSHomeExpertView(LoginRequiredMixin, ThemeContextData, TemplateView):
    template_name = "vss/customer_portal_expert/views/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = _('Welcome Expert (Course Instructor)')
        context["active_tab"] = "vss_home_expert"
        return context


class VSSExpertParticipantView(LoginRequiredMixin, ThemeContextData, TemplateView):
    template_name = "vss/customer_portal_expert/views/participant.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = _('Welcome Expert (Course Instructor)')
        context["active_tab"] = "vss_home_expert"
        return context


class OrderView(LoginRequiredMixin, ThemeContextData, TemplateView):
    template_name = "vss/customer_portal/views/order.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = _('My orders')
        context["active_tab"] = "vss_order_overview"
        context["breadcrumbs"] = vss_home + [
            {
                "label": _('My orders')
            },
        ]
        return context


class InvoiceView(LoginRequiredMixin, ThemeContextData, TemplateView):
    template_name = "vss/customer_portal/views/invoice.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = _('My invoices')
        context["active_tab"] = "vss_invoice_overview"
        context["breadcrumbs"] = vss_home + [
            {
                "label": _('My invoices')
            },
        ]
        return context


# @login_and_team_required
# def team_home(request, team_slug):
#     assert request.team.slug == team_slug
#     return render(
#         request,
#         "web/app_home.html",
#         context={
#             "team": request.team,
#             "active_tab": "dashboard",
#             "page_title": _("{team} Dashboard").format(team=request.team),
#         },
#     )


# def simulate_error(request):
#     raise Exception("This is a simulated error.")


# VSS Admin Views

class VSSAdminMixin(LoginRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.has_firm_vss():
            return redirect("vss:vss_account")
        return super().dispatch(request, *args, **kwargs)


class VSSAdminDashboard(VSSAdminMixin, TemplateView):
    template_name = "vss/admin/views/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context["active_tab"] = "vss_admin_dashboard"
        context["title"] = _("VSS Dashboard")
        return context


class VSSAdminEvents(VSSAdminMixin, TemplateView):
    template_name = "vss/admin/views/events.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context["active_tab"] = "vss_admin_events" if not self.request.resolver_match.url_name == "vss_admin_sub_events" else "vss_admin_sub_events"
        context["title"] = _("Events")
        return context


class VSSAdminCAS(VSSAdminMixin, TemplateView):
    template_name = "vss/admin/views/cas.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context["active_tab"] = "vss_admin_cas"
        context["title"] = _("CAS")
        return context


class VSSAdminParticipantCertificate(VSSAdminMixin, TemplateView):
    template_name = "vss/admin/views/participant_certificate.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context["active_tab"] = "vss_admin_participant_certificate"
        context["title"] = _("Participant certificate")
        return context


class VSSAdminAdministration(VSSAdminMixin, TemplateView):
    template_name = "vss/admin/views/administration.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context["active_tab"] = "vss_admin_administration"
        context["title"] = _("Participant certificate")
        return context


class VSSAdminMembershipAccess(VSSAdminMixin, TemplateView):
    template_name = "vss/admin/views/membership_access.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context["active_tab"] = "vss_admin_membership_access"
        context["title"] = _("Membership and access")
        return context


