
from apps.norm.models import Norm
from vss.base_erp_importer import BaseImporter


class NormImporter(BaseImporter):
    def process_sngle_norm(self, norm_item):
        try:
            norm, created = Norm.objects.update_or_create(
                no=norm_item.get('No'),  # Matching on 'No' field to update existing or create new
                defaults={
                    'description': norm_item.get('Description'),
                    'unit_price': norm_item.get('UnitPrice'),
                    'vat_print': norm_item.get('VAT_Print'),
                    'vat_download': norm_item.get('VAT_Download'),
                    'discount_group': norm_item.get('DiscountGroup'),
                    'sales_unit_text': norm_item.get('SalesUnitText'),
                    'stock_status': norm_item.get('StockStatus'),
                    'stock': norm_item.get('Stock'),
                    'price_includes_vat': bool(int(norm_item.get('PriceIncludesVat', 0))),
                    'sort_key': norm_item.get('SortKey'),
                    'special_offer': bool(int(norm_item.get('SpecialOffer', 0))),
                    'new_item': bool(int(norm_item.get('NewItem', 0))),
                    'delivery_times_in_days': norm_item.get('DeliveryTimesInDays'),
                    'spec_weight': norm_item.get('SpecWeight'),
                    'no2': norm_item.get('No2'),
                    'description2': norm_item.get('Description2'),
                    'issue': norm_item.get('Issue'),
                    'comment': norm_item.get('Comment'),
                    'standard_draft': norm_item.get('StandardDraft'),
                    'fidaskey': norm_item.get('Fidaskey'),
                    'edvnr': norm_item.get('EDVNr'),
                    'status': norm_item.get('Status'),
                    'pages': norm_item.get('Pages'),
                    'perinorm_country_code': norm_item.get('PerinormCountryCode'),
                    'date_objection': self.parse_date(norm_item.get('DateObjection')),
                    'snv_tk': norm_item.get('SNV-TK'),
                    'author': norm_item.get('Author'),
                    'switec_info_0': self.parse_date(norm_item.get('SwitecInfo0')),
                    'switec_info_1': self.parse_date(norm_item.get('SwitecInfo1')),
                    'switec_info_6': self.parse_date(norm_item.get('SwitecInfo6')),
                    'switec_info_9': self.parse_date(norm_item.get('SwitecInfo9')),
                    'alarm_revision': self.parse_date(norm_item.get('AlarmRevision')),
                    'belongs_to_wi': norm_item.get('BelongsToWi'),
                    'rule': norm_item.get('Rule'),
                    'dok_art': norm_item.get('DokArt'),
                    'text_of_withdrawal': norm_item.get('TextOfWithdrawl'),
                    'date_of_withdrawal': self.parse_date(norm_item.get('DateOfWithdrawl')),
                    'dok_nr_alternative': norm_item.get('DokNrAlternative'),
                    'norm_valid_from': self.parse_date(norm_item.get('NormValidFrom')),
                    'dok_nr': norm_item.get('DokNr'),
                    'approved_from': self.parse_date(norm_item.get('ApprovedFrom'))
                }
            )
            return norm, created, None
        except Exception as e:
            return None, False, str(e)+norm_item.get('No')

    def import_norm(self, norms_data):
        for norm_item in norms_data:
            norm_obj, created, error = self.process_sngle_norm(norm_item)
            yield norm_obj, created, error
    def fetch_data(self, norm_no=None, from_datetime=None):
        # Set the parameters based on whether norm_no or from_datetime is provided
        params = {'Action': 'GetNorm'}
        # Add parameters conditionally based on their presence
        if norm_no:
            params['normno'] = norm_no
        if from_datetime:
            params['fromdatetime'] = self.get_from_datetime(from_datetime)
        return self.request(params).get("Norm", [])