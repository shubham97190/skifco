import json

from django.conf import settings
from django.http import JsonResponse
from django.utils import timezone
from django.views.decorators.http import require_POST
from django.views.generic import TemplateView

from .models import Donation


class DonateView(TemplateView):
    template_name = 'donations/page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['razorpay_key_id'] = settings.RAZORPAY_KEY_ID
        return context


class DonationSuccessView(TemplateView):
    template_name = 'donations/success.html'


@require_POST
def create_order(request):
    try:
        import razorpay
        data = json.loads(request.body)
        amount = int(float(data.get('amount', 0)) * 100)

        if amount < 100:
            return JsonResponse({'error': 'Minimum donation is ₹1'}, status=400)

        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
        order = client.order.create({
            'amount': amount,
            'currency': 'INR',
            'payment_capture': 1,
        })

        Donation.objects.create(
            donor_name=data.get('name', ''),
            donor_email=data.get('email', ''),
            donor_phone=data.get('phone', ''),
            donor_pan=data.get('pan', ''),
            donor_address=data.get('address', ''),
            amount=data.get('amount'),
            razorpay_order_id=order['id'],
            donor=request.user if request.user.is_authenticated else None,
        )

        return JsonResponse({'order_id': order['id'], 'amount': amount})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@require_POST
def verify_payment(request):
    try:
        import razorpay
        data = json.loads(request.body)

        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
        client.utility.verify_payment_signature({
            'razorpay_order_id': data['razorpay_order_id'],
            'razorpay_payment_id': data['razorpay_payment_id'],
            'razorpay_signature': data['razorpay_signature'],
        })

        donation = Donation.objects.get(razorpay_order_id=data['razorpay_order_id'])
        donation.razorpay_payment_id = data['razorpay_payment_id']
        donation.razorpay_signature = data['razorpay_signature']
        donation.status = Donation.Status.PAID
        donation.paid_at = timezone.now()
        donation.save()

        return JsonResponse({'success': True})
    except razorpay.errors.SignatureVerificationError:
        return JsonResponse({'error': 'Payment verification failed'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
