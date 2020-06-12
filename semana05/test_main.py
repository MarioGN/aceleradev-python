import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')
import django
django.setup()
from django.test import TestCase
from api.models import User, Agent, Group, Event, GroupUser

import datetime
from django.utils import timezone
from django.core.validators import ValidationError
from django.db.utils import IntegrityError


class TestChallenge9(TestCase):

    def setUp(self):
        user = User.objects.create(name="Jose", email="jose@gmail.com", password="xxxxxxxxxxxxxxxxxxxxxxx")
        agent = Agent.objects.create(name="Machine1", address="192.168.1.1", status=True, env="prod", version="1.1.1")
        group = Group.objects.create(name="Admin")
        GroupUser.objects.create(user=user, group=group)
        Event.objects.create(level="CRITICAL", data="django.core.exceptions.ValidationError", user=user, agent=agent, arquivado=False)

    def test_1(self):
        user = User.objects.get(name="Jose")
        self.assertEqual(user.email, "jose@gmail.com")

    def test_2(self):
        agent = Agent.objects.get(name="Machine1")
        self.assertEqual(agent.name, "Machine1")

    def test_3(self):
        group = Group.objects.get(name="Admin")
        self.assertEqual(group.name, "Admin")

    def test_4(self):
        event = Event.objects.get(level="CRITICAL")
        self.assertEqual(event.level, "CRITICAL")


class AgentModelTestCase(TestCase):
    def setUp(self):
        self.obj = Agent.objects.create(
            name='PC001-office',
            status=True,
            env='production',
            version='1.1.1',
            address='192.168.1.1'
        )

    def get_meta_field(self, field):
        return Agent._meta.get_field(field)

    def test_agent_created_should_exists(self):
        self.assertTrue(Agent.objects.exists())

    def test_name_cant_be_blank(self):
        self.assertFalse(self.get_meta_field('name').blank)
    
    def test_name_cant_be_null(self):
        self.assertFalse(self.get_meta_field('name').null)

    def test_name_max_length_should_be_50(self):
        self.assertEqual(self.get_meta_field('name').max_length, 50)

    def test_status(self):
        self.assertIsInstance(self.obj.status, bool)

    def test_status_default_to_true(self):
        self.assertTrue(self.get_meta_field('status').default)

    def test_env_cant_be_blank(self):
        self.assertFalse(self.get_meta_field('env').blank)
    
    def test_env_cant_be_null(self):
        self.assertFalse(self.get_meta_field('env').null)

    def test_env_max_length_should_be_20(self):
        self.assertEqual(self.get_meta_field('env').max_length, 20)

    def test_version_cant_be_blank(self):
        self.assertFalse(self.get_meta_field('version').blank)
    
    def test_version_cant_be_null(self):
        self.assertFalse(self.get_meta_field('version').null)

    def test_version_max_length_should_be_5(self):
        self.assertEqual(self.get_meta_field('version').max_length, 5)

    def test_address_cant_be_blank(self):
        self.assertFalse(self.get_meta_field('address').blank)

    def test_address_cant_be_null(self):
        self.assertFalse(self.get_meta_field('address').null)

    def test_address_max_length_should_be_5(self):
        self.assertEqual(self.get_meta_field('address').max_length, 39)

    def test_address_cant_be_invalid_format(self):
        with self.assertRaises(ValidationError):
            self.obj.address = 'invalid.ip.address'
            self.obj.full_clean()

    def test_verbose_name(self):
        verbose_name = Agent._meta.verbose_name
        self.assertEqual(verbose_name, 'Agente')

    def test_verbose_name_plural(self):
        verbose_name_plural = Agent._meta.verbose_name_plural
        self.assertEqual(verbose_name_plural, 'Agentes')

    def test_agent_str(self):
        self.assertEqual(str(self.obj), 'PC001-office')


class EventModelTestCase(TestCase):
    def setUp(self):
        self.agent = Agent.objects.create(
            name='PC001-office',
            status=True,
            env='production',
            version='1.1.1',
            address='192.168.1.1'
        )

        self.user = User.objects.create(
            name='Mario G. Neto',
            last_login=timezone.now(),
            email='mariog.neto@gmail.com',
            password='abc12345'
        )

        self.obj = Event.objects.create(
            level='CRITICAL',
            data='django.core.exceptions.ValidationError',
            arquivado=False,
            date=datetime.date.today(),
            agent=self.agent,
            user=self.user
        )

    def get_meta_field(self, field):
        return Event._meta.get_field(field)

    def test_event_created_should_exists(self):
        self.assertTrue(Event.objects.exists())

    def test_level_cant_be_blank(self):
        self.assertFalse(self.get_meta_field('level').blank)

    def test_level_cant_be_null(self):
        self.assertFalse(self.get_meta_field('level').null)

    def test_level_max_length_should_be_20(self):
        self.assertEqual(self.get_meta_field('level').max_length, 20)

    def test_level_invalid_option_should_raise_value_error(self):
        with self.assertRaises(ValidationError):
            self.obj.level = 'INVALID_OPTION'
            self.obj.full_clean()

    def test_data_cant_be_blank(self):
        self.assertFalse(self.get_meta_field('data').blank)

    def test_data_cant_be_null(self):
        self.assertFalse(self.get_meta_field('data').null)

    def test_data_max_length_should_be_None(self):
        self.assertEqual(self.get_meta_field('data').max_length, None)

    def test_arquivado(self):
        self.assertIsInstance(self.obj.arquivado, bool)

    def test_arquivado_default_to_false(self):
        self.assertFalse(self.get_meta_field('arquivado').default)

    def test_date(self):
        self.assertIsInstance(self.obj.date, datetime.date)

    def test_date_can_be_blank(self):
        self.assertTrue(self.get_meta_field('date').blank)

    def test_date_can_be_null(self):
        self.assertTrue(self.get_meta_field('date').null)

    def test_agent(self):
        self.assertIsInstance(self.obj.agent, Agent)

    def test_agent_saved(self):
        self.assertEqual(self.obj.agent, self.agent)

    def test_agent_cant_be_blank(self):
        self.assertFalse(self.get_meta_field('agent').blank)

    def test_agent_cant_be_null(self):
        self.assertFalse(self.get_meta_field('agent').null)

    def test_agent_related(self):
        self.assertEqual(self.agent.events.all().count(), 1)

    def test_user(self):
        self.assertIsInstance(self.obj.user, User)

    def test_user_saved(self):
        self.assertEqual(self.obj.user, self.user)

    def test_user_cant_be_blank(self):
        self.assertFalse(self.get_meta_field('user').blank)

    def test_user_cant_be_null(self):
        self.assertFalse(self.get_meta_field('user').null)

    def test_user_ralated(self):
        self.assertEqual(self.user.events.all().count(), 1)

    def test_verbose_name(self):
        verbose_name = Event._meta.verbose_name
        self.assertEqual(verbose_name, 'Evento')

    def test_verbose_name_plural(self):
        verbose_name_plural = Event._meta.verbose_name_plural
        self.assertEqual(verbose_name_plural, 'Eventos')

    def test_event_str(self):
        event = f'[{datetime.date.today()}] [CRITICAL] django.core.exceptions.ValidationError user=mariog.neto@gmail.com agent=PC001-office'
        self.assertEqual(str(self.obj), event)


class GroupModelTestCase(TestCase):
    def setUp(self):
        self.obj = Group.objects.create(
            name='ADMIN'
        )

    def get_meta_field(self, field):
        return Group._meta.get_field(field)

    def test_group_created_should_exists(self):
        self.assertTrue(Group.objects.exists())

    def test_name_cant_be_blank(self):
        self.assertFalse(self.get_meta_field('name').blank)
    
    def test_name_cant_be_null(self):
        self.assertFalse(self.get_meta_field('name').null)

    def test_name_max_length_should_be_50(self):
        self.assertEqual(self.get_meta_field('name').max_length, 50)

    def test_verbose_name(self):
        verbose_name = Group._meta.verbose_name
        self.assertEqual(verbose_name, 'Grupo')

    def test_verbose_name_plural(self):
        verbose_name_plural = Group._meta.verbose_name_plural
        self.assertEqual(verbose_name_plural, 'Grupos')

    def test_group_str(self):
        self.assertEqual(str(self.obj), 'ADMIN')


class GroupUserModelTestCase(TestCase):
    def setUp(self):
        self.group = Group.objects.create(
            name='ADMIN'
        )
        
        self.user = User.objects.create(
            name='Mario G. Neto',
            last_login=timezone.now(),
            email='mariog.neto@gmail.com',
            password='abc12345'
        )

        self.obj = GroupUser.objects.create(
            group=self.group,
            user=self.user
        )

    def get_meta_field(self, field):
        return GroupUser._meta.get_field(field)

    def test_groupuser_created_should_exists(self):
        self.assertTrue(GroupUser.objects.exists())

    def test_group(self):
        self.assertIsInstance(self.obj.group, Group)

    def test_group_saved(self):
        self.assertEqual(self.obj.group, self.group)
    
    def test_group_cant_be_blank(self):
        self.assertFalse(self.get_meta_field('group').blank)

    def test_group_cant_be_null(self):
        self.assertFalse(self.get_meta_field('group').null)

    def test_group_ralated(self):
        self.assertEqual(self.group.groupuser.all().count(), 1)
    
    def test_user(self):
        self.assertIsInstance(self.obj.user, User)

    def test_user_saved(self):
        self.assertEqual(self.obj.user, self.user)

    def test_user_cant_be_blank(self):
        self.assertFalse(self.get_meta_field('user').blank)

    def test_user_cant_be_null(self):
        self.assertFalse(self.get_meta_field('user').null)

    def test_user_ralated(self):
        self.assertEqual(self.user.groupuser.all().count(), 1)

    def test_unique_together_group_user_constraint(self):
        with self.assertRaises(IntegrityError):
            GroupUser.objects.create(
                group=self.group,
                user=self.user
            )

    def test_verbose_name(self):
        verbose_name = GroupUser._meta.verbose_name
        self.assertEqual(verbose_name, 'Grupo/Usuário')

    def test_verbose_name_plural(self):
        verbose_name_plural = GroupUser._meta.verbose_name_plural
        self.assertEqual(verbose_name_plural, 'Grupos/Usuários')

    def test_groupuser_str(self):
        groupuser = f'Grupo: ADMIN / Usuário: mariog.neto@gmail.com'
        self.assertEqual(str(self.obj), groupuser)


class UserModelTestCase(TestCase):
    def setUp(self):
        self.obj = User.objects.create(
            name='Mario G. Neto',
            last_login=timezone.now(),
            email='mariog.neto@gmail.com',
            password='abc12345'
        )

    def get_meta_field(self, field):
        return User._meta.get_field(field)

    def test_user_created_should_exists(self):
        self.assertTrue(User.objects.exists())

    def test_name_cant_be_blank(self):
        self.assertFalse(self.get_meta_field('name').blank)
    
    def test_name_cant_be_null(self):
        self.assertFalse(self.get_meta_field('name').null)

    def test_name_max_length_should_be_50(self):
        self.assertEqual(self.get_meta_field('name').max_length, 50)

    def test_last_login(self):
        self.assertIsInstance(self.obj.last_login, datetime.datetime)

    def test_last_login_can_be_blank(self):
        self.assertTrue(self.get_meta_field('last_login').blank)
    
    def test_last_login_can_be_null(self):
        self.assertTrue(self.get_meta_field('last_login').null)

    def test_email_cant_be_blank(self):
        self.assertFalse(self.get_meta_field('email').blank)

    def test_email_cant_be_null(self):
        self.assertFalse(self.get_meta_field('email').null)

    def test_email_max_length_should_be_254(self):
        self.assertEqual(self.get_meta_field('email').max_length, 254)

    def test_password_cant_be_blank(self):
        self.assertFalse(self.get_meta_field('password').blank)
    
    def test_password_cant_be_null(self):
        self.assertFalse(self.get_meta_field('password').null)

    def test_password_max_length_should_be_50(self):
        self.assertEqual(self.get_meta_field('password').max_length, 50)

    def test_password_min_length_should_be_8(self):
        with self.assertRaises(ValidationError):
            self.obj.password = '1234567'
            self.obj.full_clean()

    def test_verbose_name(self):
        verbose_name = User._meta.verbose_name
        self.assertEqual(verbose_name, 'Usuário')

    def test_verbose_name_plural(self):
        verbose_name_plural = User._meta.verbose_name_plural
        self.assertEqual(verbose_name_plural, 'Usuários')

    def test_user_str(self):
        self.assertEqual(str(self.obj), 'mariog.neto@gmail.com')
