from django.db import models
from django.core.exceptions import ValidationError

# Create your models here.

class SpellLevels(models.IntegerChoices):
    CONTRIP = 0, "lv0"
    LV1 = 1, "lv1"
    LV2 = 2, "lv2"
    LV3 = 3, "lv3"
    LV4 = 4, "lv4"
    LV5 = 5, "lv5"
    LV6 = 6, "lv6"
    LV7 = 7, "lv7"
    LV8 = 8, "lv8"
    LV9 = 9, "lv9"

class SpellComponentTypes(models.TextChoices):
    VERBAL = "V", "Verbal"
    SOMATIC = "S", "SOMATIC"
    MATERIAL = "M", "Material"

class SpellComponent(models.Model):
    type = models.CharField(choices=SpellComponentTypes.choices, null=True, blank=True)
    description = models.TextField(blank=True, null=True)
    cost = models.DecimalField(default=0, max_digits=7, decimal_places=2)

    def clean(self):
        # Валидация: стоимость только для материальных компонентов
        if self.type != SpellComponentTypes.MATERIAL and self.cost:
            raise ValidationError({
                'cost': 'Стоимость может быть только у материальных компонентов'
            })


class SpellTime(models.Model):
    time = models.CharField(max_length=49)
    description = models.TextField()

class MagicSchool(models.Model):
    name = models.CharField(max_length=99)
    description = models.TextField()

class Spell(models.Model):
    id = models.IntegerField(primary_key=True)
    level = models.IntegerField(choices=SpellLevels.choices)
    time = models.ForeignKey(SpellTime, on_delete=models.SET_NULL, null=True)
    school = models.ForeignKey(MagicSchool, on_delete=models.SET_NULL, null=True)
    components = models.ManyToManyField(SpellComponent)