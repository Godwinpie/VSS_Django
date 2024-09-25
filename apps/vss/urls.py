from django.urls import path
from django.views.generic import TemplateView

from . import views

app_name = "vss"
urlpatterns = [
    path("", TemplateView.as_view(template_name="vss/home.html"), name="vss_home"),
    path("language_code/edit/", views.UpdateLanguageView.as_view(), name="vss_language_edit"),
    path("expert/", views.VSSHomeExpertView.as_view(), name="vss_home_expert"),
    path("expert/user", views.VSSExpertParticipantView.as_view(), name="vss_expert_participant"),

    path("components/", views.ComponentView.as_view(), name="vss_components"),
    path("account/", views.AccountView.as_view(), name="vss_account"),
    path("account/edit/", views.AccountEditView.as_view(), name="vss_account_edit"),
    path("events/", views.AccountEventsView.as_view(), name="vss_account_events"),
    path("account/publications/", views.PublicationsListView.as_view(), name="vss_account_publications"),
    path("account/publication/view/", views.PublicationView.as_view(), name="vss_account_publication_view"),
    path("account/publication/notes/", views.PublicationNotesView.as_view(), name="vss_account_publication_notes"),
    path("access/list/", views.ManageAccessView.as_view(), name="vss_manage_access"),
    path("access/add/", views.ManageAccessAddView.as_view(), name="vss_manage_access_add"),
    path("event/event_upcoming/", views.AccountEventDetailUpcomingView.as_view(), name="vss_account_event_detail_upcoming"),
    path("event/event_upcoming_2/", views.AccountEventDetailUpcoming2View.as_view(), name="vss_account_event_detail_upcoming_2"),
    path("event/event_running/", views.AccountEventDetailRunningView.as_view(), name="vss_account_event_detail_running"),
    path("event/event_past/", views.AccountEventDetailPastView.as_view(), name="vss_account_event_detail_past"),
    path("event/<event_name>/signup/", views.EventSignupUsersView.as_view(), name="vss_event_signup"),
    path("order/", views.OrderView.as_view(), name="vss_order_overview"),
    path("invoice/", views.InvoiceView.as_view(), name="vss_invoice_overview"),

    path("expert/", views.VSSHomeExpertView.as_view(), name="vss_home_expert"),
    path("expert/user", views.VSSExpertParticipantView.as_view(), name="vss_expert_participant"),

    # VSS Admin Views
    path("admin/dashboard/", views.VSSAdminDashboard.as_view(), name="vss_admin_dashboard"),
    path("admin/events/", views.VSSAdminEvents.as_view(), name="vss_admin_events"),
    path("admin/events/event/", views.VSSAdminEvents.as_view(), name="vss_admin_sub_events"),
    path("admin/events/cas/", views.VSSAdminCAS.as_view(), name="vss_admin_cas"),
    path("admin/participant-certificate/", views.VSSAdminParticipantCertificate.as_view(), name="vss_admin_participant_certificate"),
    path("admin/administration/", views.VSSAdminAdministration.as_view(), name="vss_admin_administration"),
    path("admin/membership/", views.VSSAdminMembershipAccess.as_view(), name="vss_admin_membership_access"),
]
