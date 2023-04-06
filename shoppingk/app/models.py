from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator,MinValueValidator

# state navigator

STATE_CHOICES=(
                ('Andaman & Nicobar Islands', 'Andaman & Nicobar Islands'), 
                ('Andhra Pradesh', 'Andhra Pradesh'),
                ('Arunachal Pradesh', 'Arunachal Pradesh'),
                ('Assam', 'Assam'),
                ('Bihar', 'Bihar'),
                ('Chandigarh', 'Chandigarh'),
                ('Chhattisgarh', 'Chhattisgarh'),
                ('Dadra & Nagar Haveli', 'Dadra & Nagar Haveli'), 
                ('Daman and Diu', 'Daman and Diu'),    
                ('Daman and Diu', 'Daman and Diu'),
                ('Dadra & Nagar Haveli', 'Dadra & Nagar Haveli'),
                ('Delhi', 'Delhi'), ('Goa', 'Goa'),
                ('Gujarat', 'Gujarat'),
                ('Haryana', 'Haryana'),
                ('Himachal Pradesh', 'Himachal Pradesh'),
                ('Jammu & Kashmir', 'Jammu & Kashmir'),
                ('Jharkhand', 'Jharkhand'),
                ('Karnataka', 'Karnataka'), 
                ('Kerala', 'Kerala'),
                ('Lakshadweep', 'Lakshadweep'),
                ('Madhya Pradesh', 'Madhya Pradesh'), 
                ('Maharashtra', 'Maharashtra'),
                ('Uttar Pradesh', 'Uttar Pradesh'),
                ('West Bengal', 'West Bengal'),
                
)

# Create your models here.
class Customer (models.Model):

  user = models.ForeignKey (User,on_delete=models. CASCADE)
  name = models.CharField(max_length=200)
  locality = models.CharField (max_length=200)
  city = models.CharField(max_length=50)
  zipcode = models.IntegerField()
  state = models.CharField(choices=STATE_CHOICES, max_length=50)
  
  def __str__(self):
     return str(self.id)

      
CATEGORY_CHOICES=(
    ('M','Mobile'),
    ('L','Laptop'),
    ('TW','Top Wear'),
    ('BW','Bottom Wear'),
)      
                         
class Product(models.Model):
    title=models.CharField(max_length=100)
    selling_price=models.FloatField()
    discount_price=models.FloatField()
    description=models.TextField()
    brand=models.CharField(max_length=100)
    category=models.CharField(choices=CATEGORY_CHOICES,max_length=2)
    product_image=models.ImageField(upload_to='productimg')


def ___str__(self):
     return str(self.id)


class Cart(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    quentity=models.PositiveIntegerField(default=1)

    
def __str__(self):
     return str(self.id)
   
@property
def total_cost(self):
    return self.quentity * self.product.discount_price



STATUS_CHOICES=(
    ('Accepted','Accepted'),
    ('Packed','Packed'),
    ('On The Way','On The Way'),
    ('Delivered','Delivered'),
    ('Cancel','Cancel'),
)

class Orderplaced(models.Model):
    
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    customer=models.ForeignKey(Customer,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    quentity=models.PositiveIntegerField(default=1)
    order_date=models.DateTimeField(auto_now_add=True)
    status=models.CharField(max_length=50,choices=STATUS_CHOICES,default='Pending')
@property
def total_cost(self): #6:10 error
    return self.quentity * self.product.discount_price
