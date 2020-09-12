from kinri.models import Kinri, Deposit, Future, Ois
from django.forms import ModelForm

class KinriForm(ModelForm):
    class Meta:
        model = Kinri
        fields = ( 'curve_name', 'curve_currency', 'interest_type', 'curve_date' )

class DepositForm(ModelForm):
    class Meta:
        model = Deposit
        fields = ('term', 'rate')

class FutureForm(ModelForm):
    class Meta:
        model = Future
        fields = ('contract', 'price', 'convexity_adj')

class OisForm(ModelForm):
    class Meta:
        model = Ois
        fields = ('term', 'bid', 'offer')
        
