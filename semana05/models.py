from django.db import models
from django.core.validators import MinLengthValidator


class User(models.Model):
    name = models.CharField('Nome', max_length=50)
    last_login = models.DateTimeField('Último Acesso', null=True, blank=True)
    email = models.EmailField('E-mail', max_length=254)
    password = models.CharField(
        'Senha', max_length=50, validators=[MinLengthValidator(8)])

    class Meta:
        verbose_name = 'Usuário'

    def __str__(self):
        return self.email


class Agent(models.Model):
    name = models.CharField('Nome', max_length=50)
    status = models.BooleanField('Status', default=True)
    env = models.CharField('Ambiente', max_length=20)
    version = models.CharField('Versão', max_length=5)
    address = models.GenericIPAddressField(
        'Endereço', max_length=39, protocol='IPv4')

    class Meta:
        verbose_name = 'Agente'

    def __str__(self):
        return self.name


class Event(models.Model):
    EVENT_LEVELS = (
        ('CRITICAL', 'CRITICAL'),
        ('DEBUG', 'DEBUG'),
        ('ERROR', 'ERROR'),
        ('WARNING', 'WARNING'),
        ('INFO', 'INFO'),
    )

    level = models.CharField('Level', max_length=20, choices=EVENT_LEVELS)
    data = models.TextField('Dados')
    arquivado = models.BooleanField('Arquivado', default=False)
    date = models.DateField('Data', null=True, blank=True)
    agent = models.ForeignKey(
        'Agent', on_delete=models.CASCADE, related_name='events')
    user = models.ForeignKey(
        'User', on_delete=models.CASCADE, related_name='events')

    class Meta:
        verbose_name = 'Evento'

    def __str__(self):
        return f'[{self.date}] [{self.level}] ' \
               f'{self.data} user={self.user} agent={self.agent}'


class Group(models.Model):
    name = models.CharField('Nome', max_length=50)

    class Meta:
        verbose_name = 'Grupo'

    def __str__(self):
        return self.name


class GroupUser(models.Model):
    group = models.ForeignKey(
        'Group', on_delete=models.CASCADE, related_name='groupuser')
    user = models.ForeignKey(
        'User', on_delete=models.CASCADE, related_name='groupuser')

    class Meta:
        unique_together = ('group', 'user')
        verbose_name = 'Grupo/Usuário'
        verbose_name_plural = 'Grupos/Usuários'

    def __str__(self):
        return f'Grupo: {self.group} / Usuário: {self.user}'
