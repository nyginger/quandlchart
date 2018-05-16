from django.db import models

class API_keys(models.Model):
    name=models.CharField(max_length=25)
    key=models.CharField(max_length=50)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural='keys'


class Items_table(models.Model):
    name=models.CharField(max_length=25)
    dataset=models.CharField(max_length=10)
    category=models.CharField(max_length=100, null=True, blank=True)
    subcategory=models.CharField(max_length=30, null=True, blank=True)
    country=models.CharField(max_length=30, null=True, blank=True)
    ccode=models.CharField(max_length=5, null=True, blank=True)
    symbol=models.CharField(max_length=30)
    description=models.CharField(max_length=300)

    
    def __str__(self):
        return '{}/{}/{}'.format(self.name, self.dataset, self.description)

class Countries(models.Model):
    dataset=models.CharField(max_length=10)
    code=models.CharField(max_length=5)
    name=models.CharField(max_length=30)

    def __str__(self):
        return '{}/{}/{}'.format(self.dataset,self.code,self.name)


class Indicators(models.Model):
    dataset=models.CharField(max_length=10)
    code=models.CharField(max_length=5)
    name=models.CharField(max_length=30)

    def __str__(self):
        return '{}/{}'.format(self.dataset,self.name)