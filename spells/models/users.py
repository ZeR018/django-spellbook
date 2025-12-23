from django.db import models
from django.utils.timezone import now


class Player(models.Model):
    """Игрок (пользователь системы)"""

    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(
        "auth.User", on_delete=models.CASCADE, related_name="player_profile"
    )
    nickname = models.CharField(max_length=50, blank=True)
    bio = models.TextField(blank=True, help_text="Краткое описание персонажа")
    experience_points = models.IntegerField(
        default=0, help_text="Опыт игрока (не персонажей)"
    )
    favorite_class = models.ForeignKey(
        "spells.CharacterClass",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="favored_by_players",
    )
    telegram_id = models.CharField(max_length=100, blank=True)
    avatar = models.ImageField(upload_to="player_avatars/", null=True)
    created_at = models.DateTimeField(default=now)
    last_login = models.DateTimeField(default=now)

    def __str__(self):
        return f"{self.nickname or self.user.username}"

    @property
    def total_characters(self):
        return self.characters.count()

    @property
    def active_characters(self):
        return self.characters.filter(is_active=True)

    class Meta:
        verbose_name = "Игрок"
        verbose_name_plural = "Игроки"
