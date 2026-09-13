import os
import django
import sys
from datetime import date

# Add the project root to the path so it can find El3yada.settings
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Configure Django settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "El3yada.settings")
django.setup()

from MainMenu.models import appointments, Payments
from django.db.models import Sum

missing_payments_count = 0
total_missing_amount = 0
payments_created = 0

for app in appointments.objects.filter(Paid__gt=0):
    # Get total paid from Payments model
    total_paid_in_payments = Payments.objects.filter(Appointment=app).aggregate(total=Sum('Paid_Amount'))['total'] or 0
    
    if app.Paid > total_paid_in_payments:
        diff = app.Paid - total_paid_in_payments
        missing_payments_count += 1
        total_missing_amount += diff
        
        # Create missing payment
        Payments.objects.create(
            Appointment=app,
            Paid_Amount=diff,
            Date=app.Adate if app.Adate else date.today(),
            MoneyBy="Migrated Legacy Payment"
        )
        payments_created += 1

print(f"--- MIGRATION RESULTS ---")
print(f"Appointments found with missing payments: {missing_payments_count}")
print(f"Total Missing Income in L.E. migrated: {total_missing_amount}")
print(f"Payments records successfully created: {payments_created}")
print(f"Migration completed successfully.")
