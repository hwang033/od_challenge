from django.db import models

class Listings(models.Model):
    """listing model
    """
    street = models.CharField(max_length=255)
    status = models.CharField(max_length=20)
    price = models.IntegerField()
    bedrooms = models.IntegerField()
    bathrooms = models.IntegerField()
    sq_ft = models.IntegerField()
    lat = models.DecimalField(max_digits=65, decimal_places=30)
    lng = models.DecimalField(max_digits=65, decimal_places=30)

    def get_properties(self):
        properties = {}
        properties['id'] = self.id
        properties['street'] = self.street
        properties['status'] = self.status
        properties['price'] = self.price
        properties['bathrooms'] = self.bathrooms
        properties['bedrooms'] = self.bedrooms
        properties['sq_ft'] = self.sq_ft
        return properties

    def get_geom(self):
        return (float(self.lng), float(self.lat))

