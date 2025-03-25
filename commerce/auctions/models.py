from django.contrib.auth.models import AbstractUser
from django.db import models
 

class User(AbstractUser):
    auction = models.ManyToManyField("Auction", blank=True, related_name="Auctions")
    watchlist = models.ManyToManyField("Auction", blank=True, related_name="Watchlist")
    won_auctions = models.ManyToManyField("Auction", blank=True, related_name="Won_auctions")
    def __str__(self):
        return f"{self.username}"

class Auction(models.Model):
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=256)
    starting_bid = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='images/')
    category = models.ForeignKey("Category", on_delete=models.CASCADE, related_name="auctions")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="auctions")
    active = models.BooleanField(default=True)
    current = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='current_winner')
    def __str__(self):
        return f"{self.title} - {self.starting_bid}"
    
class Bid(models.Model):
    value = models.DecimalField(max_digits=10, decimal_places=2)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids")
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name="bids")
    def __str__(self):
        return f"{self.value} - {self.user} - {self.auction}"
    
class Comment(models.Model):
    text = models.CharField(max_length=256)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name="comments")
    def __str__(self):
        return f"{self.text} - {self.user} - {self.auction}"
    
class Category(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=64)
    def __str__(self):
        return f"{self.name}"
    
    class Meta:
        verbose_name_plural = "Categories"

