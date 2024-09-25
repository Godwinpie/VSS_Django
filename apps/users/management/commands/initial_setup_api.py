
from django.core.management.base import BaseCommand
from django.core.management import call_command

class Command(BaseCommand):
    help = 'Executes all commands from API sequentially.'
    def handle(self, *args, **options):
        try:
            self.stdout.write(self.style.SUCCESS('Starting execution of all commands...'))
            commands = [
                {
                    'name': 'get_persons',
                    'args': [],
                    'kwargs': {'fromdatetime': '2024-01-01Z08:00h'},
                },
                {
                    'name': 'getcustomers',
                    'args': [],
                    'kwargs': {'fromdatetime': '2024-01-01Z08:00h'},
                },
                {
                    'name': 'getsubscriptions',
                    'args': [],
                    'kwargs': {'fromdatetime': '2024-01-01Z08:00h'},
                },
                {
                    'name': 'getfirms',
                    'args': [],
                    'kwargs': {'fromdatetime': '2001-01-01Z08:00h'},
                },
                {
                    'name': 'getfirmpersons',
                    'args': [],
                    'kwargs': {'fromdatetime': '2001-01-01Z08:00h'},
                },
                {
                    'name': 'get_expert_rights',
                    'args': [],
                    'kwargs': {'fromdatetime': '2001-01-01Z08:00h'},
                },
                {
                    'name': 'getnorms',
                    'args': [],
                    'kwargs': {'fromdatetime': '2001-01-01Z08:00h'},
                },
                # Add more commands here as needed
            ]
            self.stdout.write(self.style.SUCCESS('Starting execution of all commands...'))
            for cmd in commands:
                name = cmd.get('name')
                args = cmd.get('args', [])
                kwargs = cmd.get('kwargs', {})

                self.stdout.write(f'Running {name}...')
                try:
                    call_command(name, *args, **kwargs)
                    self.stdout.write(self.style.SUCCESS(f'{name} completed successfully.'))
                except Exception as e:
                    self.stderr.write(self.style.ERROR(f'Error executing {name}: {e}'))
                    # Optionally, decide whether to continue or halt on error
                    # For example, to halt:
                    # raise e
                    # To continue, simply pass
                    continue

        except Exception as e:
            self.stderr.write(self.style.ERROR(f'An error occurred: {e}'))
            # Optionally, you can raise the exception if you want to halt execution
            # raise e