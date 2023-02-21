from django.db import models


class KeyWords(models.Model):
    key_words = models.CharField(db_column="KeyWords", max_length=200, primary_key=True)

    class Meta:
        verbose_name_plural = "KeyWords"
        db_table = 'KeyWords'
        ordering = ['key_words']

    def __str__(self):
        return self.key_words


class IgnoreWords(models.Model):
    key_ignore = models.CharField(db_column="IgnoreWords", max_length=200, primary_key=True)

    class Meta:
        verbose_name_plural = "IgnoreWords"
        db_table = 'IgnoreWords'
        ordering = ['key_ignore']

    def __str__(self):
        return self.key_ignore


class Client(models.Model):
    client_id = models.IntegerField(db_column="ClientId", primary_key=True)
    job_title = models.CharField(db_column="Job title", max_length=200, blank=True, null=True)
    date_published = models.DateTimeField(db_column="PublishedDate", blank=True, null=True)
    job_location = models.CharField(db_column="Job location", max_length=200, blank=True, null=True)
    type_klus = models.CharField(db_column="Type klus", max_length=400, blank=True, null=True)
    soort_probleem = models.CharField(db_column="Soort probleem", max_length=400, blank=True, null=True)
    aanvullende_informatie = models.CharField(db_column="Aanvullende informatie", max_length=700, blank=True, null=True)
    contact_name = models.CharField(db_column="Contact name", max_length=100, blank=True, null=True)
    contact_email = models.EmailField(db_column="Contact email", max_length=254, blank=True, null=True)
    contact_phone = models.CharField(db_column="Contact phone", max_length=20, blank=True, null=True)
    client_url = models.URLField(db_column="Url address", max_length=200, blank=True, null=True)

    class Meta:
        verbose_name_plural = "Clients"
        db_table = 'Clients'
        ordering = ['-date_published']

    def __str__(self):
        return f"{self.client_id} {self.job_title} {self.date_published} {self.job_location}"
