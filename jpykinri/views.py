from django.shortcuts import render
from django.http import HttpResponse
from django.db import transaction
from django.contrib import messages
from jpykinri.models import Kinri, Deposit, Ois
from jpykinri.forms import KinriForm, DepositForm, OisForm

# Create your views here.

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def get_ois_yield(yield_type, bid, offer):
    if yield_type == 'bid':
        return bid
    elif yield_type == 'offer':
        return offer
    return (bid + offer) / 2

def build_graph_data(yield_type, deposit_list, ois_list):
    #data['labels'] = []
    labels = []
    data = []
    # deposit
    for entry in deposit_list:
        if entry['term'] == "":
            continue 
        labels.append(entry['term'])
        data.append(entry['rate'])
    
    # ois
    for entry in ois_list:
        if entry['term'] == "":
            continue 
        labels.append(entry['term'])
        data.append(get_ois_yield(yield_type, entry['bid'], entry['offer']))
        
    return { 'labels': labels, 'data': data }

@transaction.atomic
def kinri_store(setting, deposit_list, ois_list):
    # remove old data
    qs = Kinri.objects.filter(**setting)
    qs.delete()

    kinri_form = KinriForm(setting)
    if not kinri_form.is_valid():
        raise Exception("general setting: invalid value")

    kinri = kinri_form.save()
    # deposit
    for entry in deposit_list:
        print(entry)
        deposit_form = DepositForm(entry)
        if not deposit_form.is_valid():
            raise Exception("deposit: invalid value")
        deposit = deposit_form.save(commit=False)
        deposit.kinri = kinri
        deposit.save()

    # ois
    for entry in ois_list:
        print(entry)
        ois_form = OisForm(entry)
        if not ois_form.is_valid():
            raise Exception("ois: invalid value")
        ois = ois_form.save(commit=False)
        ois.kinri = kinri
        ois.save()

def my_float(x):
    try:
        x = float(x)
    except:
        x = float(0)
    return x

def deposit_parser(x):
    return {
        "term": x[0],
        "rate": my_float(x[1])
    }

def ois_parser(x):
    return {
        "term": x[0],
        "bid": my_float(x[1]),
        "offer": my_float(x[2])
    }

def jpy_kinri_add(request):
    if request.method == 'GET':
        setting = {
            'curve_name': '',
            'curve_currency': '',
            'interest_type': '',
            'curve_date': ''
        }
        deposit_list = [deposit_parser(("1D",""))]
        ois_list = [ois_parser(("","",""))]
        yield_type = 'bid'
    else:
        setting = {
            'curve_name': request.POST['curve_name'],
            'curve_currency': request.POST['curve_currency'],
            'interest_type': request.POST['interest_type'],
            'curve_date': request.POST['curve_date'].replace('/', '-')
        }
        print(request.POST)
        # deposit
        deposit_term = request.POST.getlist('deposit_term')
        deposit_rate = request.POST.getlist('deposit_rate')
        deposit_list = [deposit_parser(x) for x in zip(deposit_term, deposit_rate)]
        # ois
        ois_term = request.POST.getlist('ois_term')
        ois_bid = request.POST.getlist('ois_bid')
        ois_offer = request.POST.getlist('ois_offer')
        ois_list = [ois_parser(x) for x in zip(ois_term, ois_bid, ois_offer)]
        yield_type = request.POST['yield_type']
        if 'submit_type' in request.POST and request.POST['submit_type'] == 'register':
            try:
                kinri_store(setting, deposit_list, ois_list)
            except Exception as e:
                messages.warning(request, e.args)

    graph_data = build_graph_data(yield_type, deposit_list, ois_list)
    print('data', graph_data)
        
    #latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {
        'setting': setting,
        'yield_type': yield_type,
        'deposit_list': deposit_list,
        'ois_list': ois_list,
        'data': graph_data
    }
    return render(request, 'jpykinri/jpy_kinri_add.html', context)

