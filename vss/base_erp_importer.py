import requests
import  logging
from requests.auth import HTTPBasicAuth
from django.conf import settings
from datetime import datetime

logger = logging.getLogger(__name__)

class BaseImporter:
    def __init__(self):
        self.url = settings.NAVISION_API_URL
        self.username = settings.NAVISION_USERNAME
        self.password = settings.NAVISION_PASSWORD

    def request(self, params):
        #logger.info(params)
        #logger.info(self.url)
        try:
            response = requests.get(self.url, params=params, auth=HTTPBasicAuth(self.username, self.password))
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise RuntimeError(f'Error fetching data: {e}')
    def get_from_datetime(self, from_datetime):
        if not from_datetime:
            from_datetime = datetime.now().strftime("%Y-%m-%dZ%H:%Mh")
        return from_datetime

    def parse_date(self, date_str, format="%Y.%m.%d"):
        """Parse a date string into a datetime.date object. Return None if parsing fails."""
        if not date_str or date_str in ['0000.00.00', '']:
            # Return None if the date string is empty or known to be invalid
            return None

        try:
            # Attempt to parse the date string with the given format
            return datetime.strptime(date_str, format).date()
        except ValueError:
            # Handle any parsing errors by returning None
            return None

    def parse_decimal(self, value):
        try:
            return float(value) if value else 0.00
        except ValueError:
            return 0.00

    def split_name(self, full_name):
        """Split the full name into first and last name."""
        parts = full_name.split(maxsplit=1)  # Split into two parts: first name and last name
        first_name = parts[0] if parts else ''
        last_name = parts[1] if len(parts) > 1 else ''
        return first_name, last_name
    def get_first_row(self, data):
        if data and isinstance(data, list) and len(
                data) > 0:
            return data[0]
        return None
