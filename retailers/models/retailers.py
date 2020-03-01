# built-in imports

# third-party imports
from django.db import models


# custom imports


class Retailer(models.Model):
    name = models.CharField(max_length=30, blank=True, null=True)

    clientId = models.CharField(max_length=50, unique=True)
    clientSecret = models.CharField(max_length=100, unique=True)

    createdDatetime = models.DateTimeField(auto_now_add=True)
    updatedDatetime = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "Retailer %s, Client %s" % (self.name, self.clientId)

    def __repr__(self):
        return f"<<{self.__class__.__name__}> ClientId:{self.clientId}>"
