from django.db import models
from colorfield.fields import ColorField

class Data(models.Model):
    # 아이콘 위치
    icon_location_y = models.IntegerField()
    # 아이콘 크기
    icon_width = models.IntegerField()
    icon_height = models.IntegerField()
    # 아이콘 각도
    icon_angle = models.IntegerField()

    # 책 표지 색깔
    book_color = ColorField()
    # 책 제목
    book_title = models.CharField(max_length=100)
    # 폰트
    font = models.CharField(max_length=100)
