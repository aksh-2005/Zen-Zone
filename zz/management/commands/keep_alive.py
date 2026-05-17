from django.core.management.base import BaseCommand
import os
from supabase import create_client

class Command(BaseCommand):
    help = 'Ping Supabase to prevent project pause'

    def handle(self, *args, **kwargs):
        url = os.environ.get("https://birzwwtcmtkefnepmwhg.supabase.co/rest/v1/")
        key = os.environ.get("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImJpcnp3d3RjbXRrZWZuZXBtd2hnIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzgxNDc3ODgsImV4cCI6MjA5MzcyMzc4OH0.ogfdXbF1f10n1oMctymwM_rUY77ZtVUFAQ250QFc5dI")
        client = create_client(url, key)
        client.table("auth_user").select("id").limit(1).execute()
        self.stdout.write("Supabase pinged successfully!")