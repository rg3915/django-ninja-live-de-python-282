from django.db import models


class StatusChoices(models.TextChoices):
    CANCELADO = 'C', 'Cancelado'
    PENDENTE = 'P', 'Pendente'
    FINALIZADO = 'F', 'Finalizado'


class Task(models.Model):
    title = models.CharField('título', max_length=100)
    is_completed = models.BooleanField('completo', default=False)
    status = models.CharField(
        max_length=1,
        choices=StatusChoices.choices,
        default=StatusChoices.PENDENTE,
    )
    user = models.ForeignKey(
        'auth.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    class Meta:
        ordering = ('title',)
        verbose_name = 'tarefa'
        verbose_name_plural = 'tarefas'

    def __str__(self):
        return f'{self.title}'
