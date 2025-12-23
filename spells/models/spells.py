from django.db import models
from django.utils.timezone import now

from spells.models.characters import CharacterClass, Subclass
from spells.models.enums import Characters, EffectCategory, SpellLevels
from spells.models.users import Player


class MaterialComponent(models.Model):
    "Материальный компонент"

    id = models.AutoField(primary_key=True)
    name = models.TextField(max_length=49)
    description = models.TextField(blank=True, null=True)
    cost = models.DecimalField(
        default=0, max_digits=7, decimal_places=2, help_text="Стоимость в ЗМ", null=True
    )

    is_consumable = models.BooleanField(
        default=False, help_text="Расходуется ли компонент при касте заклинания"
    )
    is_focus = models.BooleanField(
        default=False, help_text="Является ли фокусировкой для заклинания"
    )

    def truncate_description(self, description: str = "", max_length: int = 20) -> str:
        if not description:
            description = self.description

        if len(description) > max_length:
            return description[:max_length] + "..."
        return description

    def __str__(self):
        cost_str = f"| ({self.cost} зм) " if self.cost else ""
        description_str = self.truncate_description()
        return f"{self.name} {cost_str}({description_str})"

    class Meta:
        verbose_name = "Материальный компонент"
        verbose_name_plural = "Материальные компоненты"


class SpellTime(models.Model):
    "Время накладывания заклинания"

    id = models.AutoField(primary_key=True)
    time = models.CharField(max_length=49)
    description = models.TextField()

    def __str__(self):
        return self.time


class MagicSchool(models.Model):
    "Школа заклинания"

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=99)
    description = models.TextField()
    color = models.CharField(max_length=7, default="#3498db")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Школа магии"
        verbose_name_plural = "Школы магии"


class DamageType(models.Model):
    "Тип наносимого урона"

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30)
    description = models.TextField(blank=True)
    is_magic = models.BooleanField(default=True)

    def __str__(self):
        magic_str = " (маг.)" if self.is_magic else " (не маг.)"
        return f"{self.name} - {magic_str}"

    class Meta:
        verbose_name = "Тип урона"
        verbose_name_plural = "Типы урона"


class Effect(models.Model):
    """Эффекты от заклинания"""

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=49)
    description = models.TextField()
    category = models.CharField(
        max_length=4, choices=EffectCategory.choices, blank=True
    )
    duration = models.CharField(
        max_length=100, blank=True, help_text="Время действия эффекта"
    )
    damage_type = models.ForeignKey(
        DamageType,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="effects",
        help_text="Тип урона при наличии",
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Эффект заклинания"
        verbose_name_plural = "Эффекты заклинаний"


class Spell(models.Model):
    """Заклинание"""

    class AttackType(models.TextChoices):
        ATTACK_ROLL = "ATTACK", "Бросок атаки"
        SAVE_THROW = "SAVE", "Спасбросок"
        AUTOMATIC = "AUTO", "Автоматическое"
        MIXED = "MIXED", "Комбинированное"
        NONE = "NONE", "Нет броска"

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=150, unique=True)
    level = models.IntegerField(
        choices=SpellLevels.choices, default=SpellLevels.CONTRIP
    )
    time = models.ForeignKey(SpellTime, on_delete=models.SET_NULL, null=True)
    school = models.ForeignKey(MagicSchool, on_delete=models.SET_NULL, null=True)

    # Компоненты
    verbal_component = models.BooleanField(
        default=False, help_text="Вербальный компонент"
    )
    somatic_component = models.BooleanField(
        default=False, help_text="Соматический компонент"
    )
    material_components = models.ManyToManyField(MaterialComponent)

    # Дистанция
    range = models.CharField(
        max_length=100, blank=True, help_text="Дистанция (по умолчанию в футах)"
    )

    # Длительность
    duration = models.CharField(max_length=100)
    concentration = models.BooleanField(default=False)
    ritual = models.BooleanField(default=False)

    # Описание
    description = models.TextField()
    higher_level = models.TextField(blank=True, help_text="На более высоком уровне")

    # Механика
    attack_type = models.CharField(
        max_length=10, choices=AttackType.choices, default=AttackType.NONE
    )
    saving_throw_ability = models.CharField(
        max_length=3,
        choices=Characters.choices,
        blank=True,
        help_text="Характеристика для спасброска (если требуется)",
    )

    # Эффекты
    effects = models.ManyToManyField(Effect, related_name="spells", blank=True)

    # Кто может использовать заклинание
    aviable_classes = models.ManyToManyField(
        CharacterClass, related_name="aviable_spells", blank=True
    )
    aviable_subclasses = models.ManyToManyField(
        Subclass, related_name="aviable_spells", blank=True
    )

    # Источник
    source_book = models.CharField(max_length=100, blank=True)
    page_number = models.IntegerField(null=True, blank=True)

    # Метаданные
    is_official = models.BooleanField(default=True)
    created_by = models.ForeignKey(
        Player,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="created_spells",
        help_text="Пользователь, добавивший заклинание",
    )
    created_at = models.DateTimeField(default=now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        level_str = "Заговор" if self.level == 0 else f"{self.level} уровень"
        return f"{self.name} ({level_str}, {self.school.name})"

    @property
    def is_cantrip(self):
        return self.level == 0

    class Meta:
        verbose_name = "Заклинание"
        verbose_name_plural = "Заклинания"
        ordering = ["level", "name"]
        indexes = [
            models.Index(fields=["level"]),
            models.Index(fields=["school"]),
            models.Index(fields=["attack_type"]),
            models.Index(fields=["concentration"]),
            models.Index(fields=["ritual"]),
        ]
