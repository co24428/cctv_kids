from django.db import models

# Create your models here.


class cctv_data(models.Model):
    objects = models.Manager()

    no          = models.AutoField(primary_key=True)
    big_addr    = models.CharField(max_length=30)
    small_addr  = models.CharField(max_length=30)
    cctv_yn     = models.CharField(max_length=5)
    cctv_num    = models.IntegerField()

class user_table(models.Model):
    objects = models.Manager()

    user_id     = models.CharField(max_length=30, primary_key=True)
    name        = models.CharField(max_length=20)
    password    = models.CharField(max_length=30)
    age         = models.IntegerField()
    home        = models.CharField(max_length=70)

class article(models.Model):
    objects = models.Manager()

    no          = models.AutoField(primary_key=True)
    title       = models.CharField(max_length=70)
    thumbnail   = models.BinaryField(null=True)
    report      = models.CharField(max_length=20)
    content     = models.TextField()
    pub_date     = models.DateField()

class favorite(models.Model):
    objects = models.Manager()

    no          = models.AutoField(primary_key=True)
    user_id     = models.ForeignKey(user_table, on_delete = models.CASCADE)
    region_no   = models.ForeignKey(cctv_data, on_delete = models.CASCADE)

class article_scrap(models.Model):
    objects = models.Manager()

    no          = models.AutoField(primary_key=True)
    user_id     = models.ForeignKey(user_table, on_delete = models.CASCADE)
    article_no   = models.ForeignKey(article, on_delete = models.CASCADE)
    scrap_date  = models.DateField()