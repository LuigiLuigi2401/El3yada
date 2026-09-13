from MainMenu.models import appointments, Payments
from django.db.models import Sum

missing_payments_count = 0
total_missing_amount = 0

for app in appointments.objects.filter(Paid__gt=0):
    # Get total paid from Payments model
    total_paid_in_payments = Payments.objects.filter(Appointment=app).aggregate(total=Sum('Paid_Amount'))['total'] or 0
    
    if app.Paid > total_paid_in_payments:
        diff = app.Paid - total_paid_in_payments
        missing_payments_count += 1
        total_missing_amount += diff

print(f"--- RESULTS ---")
print(f"Appointments missing payments: {missing_payments_count}")
print(f"Total Missing Income in L.E.: {total_missing_amount}")
