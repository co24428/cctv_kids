from django.db import models

# Create your models here.


class cctv_data(models.Model):
    objects = models.Manager()

    no          = models.AutoField(primary_key=True)
    big_addr    = models.CharField(max_length=30, null=True)
    small_addr  = models.CharField(max_length=30, null=True)
    sisul       = models.CharField(max_length=30, null=True)
    cctv_yn     = models.CharField(max_length=5, null=True)
    cctv_num    = models.IntegerField(null=True)

class user_table(models.Model):
    objects = models.Manager()

    user_id     = models.CharField(max_length=30, primary_key=True)
    name        = models.CharField(max_length=20, null=True)
    password    = models.CharField(max_length=30, null=True)
    age         = models.IntegerField(null=True)
    home        = models.CharField(max_length=70, null=True)

class article(models.Model):
    objects = models.Manager()

    no          = models.AutoField(primary_key=True)
    title       = models.CharField(max_length=70, null=True)
    thumbnail_i   = models.TextField(null=True)
    report      = models.CharField(max_length=20, null=True)
    link        = models.CharField(max_length=100, null=True)
    content     = models.TextField(null=True)
    pub_date    = models.DateField(null=True)

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
    