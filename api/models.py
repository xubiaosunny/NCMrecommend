from django.db import models

# Create your models here.


class HistoryRecord(models.Model):
    u_id = models.IntegerField(db_index=True)
    m_id = models.IntegerField(db_index=True)
    m_name = models.CharField(max_length=50, null=True)
    time = models.DateTimeField(auto_now_add=True)


class Tag(models.Model):
    # categories = {
    #     "0": "语种",
    #     "1": "风格",
    #     "2": "场景",
    #     "3": "情感",
    #     "4": "主题"
    # }
    name = models.CharField(max_length=50, db_index=True)
    category = models.IntegerField(db_index=True)


class PlayList(models.Model):
    p_id = models.IntegerField(db_index=True)
    name = models.CharField(max_length=50, db_index=True)
    tags = models.ManyToManyField('Tag', null=True)


class Music(models.Model):
    m_id = models.IntegerField(db_index=True)
    name = models.CharField(max_length=50, db_index=True)
    playlists = models.ManyToManyField('PlayList', null=True)