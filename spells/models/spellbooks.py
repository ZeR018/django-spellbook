from django.db import models
from django.utils.timezone import now

from spells.models.characters import Person

from .spells import Spell


class Spellbook(models.Model):
    """
    Спеллбук - один из наборов заклинаний персонажа
    (у одного персонажа может быть несколько спеллбуков,
    у одного игрока - несколько персонажей)
    """

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    spells = models.ManyToManyField(Spell, related_name="spellbooks", blank=True)
    owner = models.ForeignKey(
        Person, on_delete=models.CASCADE, related_name="spellbooks"
    )

    # Статус
    is_active = models.BooleanField(default=True, help_text="Активен ли этот спеллбук")
    is_shared = models.BooleanField(
        default=False, help_text="Доступен ли для других игроков"
    )

    # Ячейки заклинаний в этом спеллбуке
    max_spell_slots_1 = models.IntegerField(default=0)
    max_spell_slots_2 = models.IntegerField(default=0)
    max_spell_slots_3 = models.IntegerField(default=0)
    max_spell_slots_4 = models.IntegerField(default=0)
    max_spell_slots_5 = models.IntegerField(default=0)
    max_spell_slots_6 = models.IntegerField(default=0)
    max_spell_slots_7 = models.IntegerField(default=0)
    max_spell_slots_8 = models.IntegerField(default=0)
    max_spell_slots_9 = models.IntegerField(default=0)

    current_spell_slots_1 = models.IntegerField(default=0)
    current_spell_slots_2 = models.IntegerField(default=0)
    current_spell_slots_3 = models.IntegerField(default=0)
    current_spell_slots_4 = models.IntegerField(default=0)
    current_spell_slots_5 = models.IntegerField(default=0)
    current_spell_slots_6 = models.IntegerField(default=0)
    current_spell_slots_7 = models.IntegerField(default=0)
    current_spell_slots_8 = models.IntegerField(default=0)
    current_spell_slots_9 = models.IntegerField(default=0)

    # Колдовские ячейки
    warlock_slot_level = models.IntegerField(default=0)
    warlock_max_slots = models.IntegerField(default=0)
    warlock_current_slots = models.IntegerField(default=0)

    # Метаданные
    created_at = models.DateTimeField(default=now)
    updated_at = models.DateTimeField(auto_now=True)
    last_used = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.name} ({self.owner.name})"

    def reset_all_spell_slots(self):
        """Восстановить все ячейки"""
        self.current_spell_slots_1 = self.max_spell_slots_1
        self.current_spell_slots_2 = self.max_spell_slots_2
        self.current_spell_slots_3 = self.max_spell_slots_3
        self.current_spell_slots_4 = self.max_spell_slots_4
        self.current_spell_slots_5 = self.max_spell_slots_5
        self.current_spell_slots_6 = self.max_spell_slots_6
        self.current_spell_slots_7 = self.max_spell_slots_7
        self.current_spell_slots_8 = self.max_spell_slots_8
        self.current_spell_slots_9 = self.max_spell_slots_9
        self.warlock_current_slots = self.warlock_max_slots
        self.save()

    def use_spell_slot(self, spell_level, is_warlock=False):
        """Использовать ячейку заклинания"""
        if is_warlock and self.warlock_current_slots > 0:
            self.warlock_current_slots -= 1
            self.save()
            return True

        slot_field = f"current_spell_slots_{spell_level}"
        current = getattr(self, slot_field, 0)
        if current > 0:
            setattr(self, slot_field, current - 1)
            self.save()
            return True

        return False

    @property
    def total_spells(self):
        return self.spells.count()

    class Meta:
        verbose_name = "Спеллбук"
        verbose_name_plural = "Спеллбуки"
        ordering = ["-updated_at"]
