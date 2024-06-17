from django.shortcuts import render
from django.http import HttpResponse
from .models import product, Contact, Orders, OrderUpdate
import json
from math import ceil
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.shortcuts import render
import razorpay
from django.http import HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt


from .models import Payment
MERCHANT_KEY = 'rzp_test_YkIpE0xCwUxjNN'
def index(request):
    products=product.objects.all()
    allProds = []
    catprods = product.objects.values('category', 'id')
    cats = {item['category'] for item in catprods}
    for i in cats:
        prod = product.objects.filter(category=i)
        n = len(prod)
        nslides = n // 4 + ceil((n / 4) - (n // 4))
        allProds.append([prod, range(1, nslides), nslides])
        params={'allProds':allProds}
    return render(request,'shop/index.html',params)

def searchMatch(query, item):
    if query in item.product_name or query in item.Description.lower() or query in item.category or query in item.subcategory:
        return True
    else:
        return False

def search(request):
    query= request.GET.get('search')
    allProds = []
    catprods = product.objects.values('category', 'id')
    cats = {item['category'] for item in catprods}
    for cat in cats:
        prodtemp = product.objects.filter(category=cat)
        prod=[item for item in prodtemp if searchMatch(query, item)]
        n = len(prod)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        if len(prod)!= 0:
            allProds.append([prod, range(1, nSlides), nSlides])
    params = {'allProds': allProds, "msg":""}
    if len(allProds)==0 or len(query)<4:
        params={'msg':"Please make sure to enter relevant search query"}
    return render(request, 'shop/search.html', params)

def about(request):
    return render(request,'shop/about.html')
def contact(request):
    if request.method=="POST":
        name=request.POST.get('name', '')
        email=request.POST.get('email', '')
        phone=request.POST.get('phone', '')
        desc=request.POST.get('desc', '')
        contact=Contact(name=name,email=email,phone=phone,Description=desc)
        contact.save()
        Submitted=True
        return render(request, 'shop/contact.html', {'Submitted':Submitted})
    return render(request, "shop/contact.html")
def tracker(request):
    if request.method=="POST":
        orderId = request.POST.get('orderId', '')
        email = request.POST.get('email', '')
        try:
            order = Orders.objects.filter(order_id=orderId, email=email)
            if len(order)>0:
                update = OrderUpdate.objects.filter(order_id=orderId)
                updates = []
                for item in update:
                    updates.append({'text': item.update_desc, 'time': item.timestamp})
                    response = json.dumps({"status":"success", "updates": updates, "itemsJson": order[0].items_json}, default=str)
                
                return HttpResponse(response)
            else:
                return HttpResponse('"status":"noitem"')
        except Exception as e:
            return HttpResponse('"status":"error"')

    return render(request, 'shop/tracker.html')
def products(request, myid):
    product = product.objects.filter(id=myid)
    return render(request, 'shop/prodView.html', {'product':product[0]})
def checkout(request):
    if request.method == "POST":
        items_json = request.POST.get('itemsJson', '')
        name = request.POST.get('name', '')
        amount = request.POST.get('amount', '')
        email = request.POST.get('email', '')
        address = request.POST.get('address1', '') + " " + request.POST.get('address2', '')
        city = request.POST.get('city', '')
        state = request.POST.get('state', '')
        zip_code = request.POST.get('zip_code', '')
        phone = request.POST.get('phone', '')
        
        order = Orders(items_json=items_json, name=name, email=email, address=address, city=city,
                       state=state, zip_code=zip_code, phone=phone, amount=amount)
        order.save()
        update = OrderUpdate(order_id=order.order_id, update_desc="The order has been placed")
        update.save()
        
        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
        payment = client.order.create({'amount': int(amount) * 100, 'currency': 'INR', 'payment_capture': '1'})
        
        payment_obj = Payment.objects.create(
            order_id=payment['id'],
            amount=amount,
        )
        
        context = {
            'razorpay_key_id': settings.RAZORPAY_KEY_ID,
            'payment': payment,
            'amount': int(amount) * 100,  
            'name': name,
            'email': email,
            'phone': phone,
            'address': address,
            'city': city,
            'state': state,
            'zip_code': zip_code,
        }
        
        return render(request, 'shop/checkout.html', context)

    return render(request, 'shop/checkout.html')

@csrf_exempt
def payment_success(request):
    if request.method == "POST":
        payment_id = request.POST.get('razorpay_payment_id', '')
        order_id = request.POST.get('razorpay_order_id', '')
        signature = request.POST.get('razorpay_signature', '')

        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
        try:
            client.utility.verify_payment_signature({
                'razorpay_order_id': order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature
            })
            payment = Payment.objects.get(order_id=order_id)
            payment.payment_id = payment_id
            payment.status = 'paid'
            payment.save()
            return HttpResponse('Payment Successful')
        except:
            return HttpResponseBadRequest()
    return HttpResponseBadRequest()

from .models import product
def productlist(request):
    context = {
        'product':product.objects.all()
    }
    return render(request,'shop/product.html',context)

from django.shortcuts import render
from .models import product

def subcategory_view(request, subcategory):
    products = product.objects.filter(subcategory=subcategory)
    context = {
        'subcategory': subcategory,
        'products': products
    }
    return render(request, 'shop/subcategory.html', context)







