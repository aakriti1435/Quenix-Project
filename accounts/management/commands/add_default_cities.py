from django.core.management.base import BaseCommand
from accounts.models import *

CITIES_LIST = ["Delhi","Mumbai","Kolkata","Bangalore","Chennai","Hyderabad","Ahmadabad","Surat","Pune","Jaipur","Lucknow","Kozhikode","Malappuram","Gurugram","Noida","Ghaziabad","Faridabad","Thrissur","Kochi","Kanpur","Indore","Nagpur","Coimbatore","Thiruvananthapuram","Patna","Bhopal","Agra","Vadodara","Kannur","Visakhapatnam","Nashik","Vijayawada","Kollam","Rajkot","Ludhiana","Madurai","Meerut","Raipur","Varanasi","Jamshedpur","Srinagar","Aurangabad","Jodhpur","Mohali","Panchkula"]


class Command(BaseCommand):
    help = "Adding default cities...."
    def handle(self, *args, **options):
        try:        
            user=User.objects.get(is_superuser=1, role_id='1')
        except:
            self.stdout.write(self.style.NOTICE("Admin rights, Create Admin First"))
            return None
        Cities.objects.all().delete()            
        for city in range(len(CITIES_LIST)):
            added_city = Cities.objects.create(city=CITIES_LIST[city])
            self.stdout.write(self.style.SUCCESS('City - %s' %CITIES_LIST[city]))
