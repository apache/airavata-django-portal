from django.core.management.base import BaseCommand
from wagtail.models import Revision


class Command(BaseCommand):
    help = "Fix the content_type id in the page revisions content_type which may be correct due to being imported from a different Django instance"

    def handle(self, **options):
        fixed_count = 0
        for pr in Revision.objects.all():
            if pr.content['content_type'] != pr.content_object.content_type.id:
                pr.content['content_type'] = pr.content_object.content_type.id
                pr.save()
                fixed_count = fixed_count + 1
        if fixed_count > 0:
            self.stdout.write(
                self.style.SUCCESS(f"Successfully fixed the content type of {fixed_count} page revisions")
            )
