# Generated by Django 3.0.2 on 2020-03-19 19:46

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='Class',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('class_name', models.CharField(max_length=50)),
                ('dept', models.CharField(default='XXXX', max_length=6)),
                ('course_num', models.IntegerField(default='0000')),
            ],
        ),
        migrations.CreateModel(
            name='QTUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('first_name', models.TextField(max_length=20)),
                ('last_name', models.TextField(max_length=30)),
                ('year', models.IntegerField(null=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='TutorableClass',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('TA', models.BooleanField(default=False)),
                ('experience', models.TextField()),
                ('class_id', models.ManyToManyField(default=1, to='QuickTutor.Class')),
                ('user', models.ManyToManyField(default=1, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Session',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_and_time', models.DateTimeField()),
                ('duration_of_session', models.DurationField()),
                ('Student', models.ManyToManyField(default=1, related_name='Student', to=settings.AUTH_USER_MODEL)),
                ('Tutor', models.ManyToManyField(default=1, related_name='Tutor', to=settings.AUTH_USER_MODEL)),
                ('subject_in_regards_to', models.ManyToManyField(default=1, to='QuickTutor.Class')),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.IntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')], help_text='Please rate your experience.')),
                ('description', models.TextField(help_text='Please enter some additional information regarding your experience')),
                ('type_of_review', models.CharField(choices=[('S', 'student'), ('T', 'tutor')], default='T', max_length=1)),
                ('time_of_review', models.DateTimeField(default=django.utils.timezone.now)),
                ('Author', models.ManyToManyField(default=1, related_name='Author', to=settings.AUTH_USER_MODEL)),
                ('Recipient', models.ManyToManyField(default=1, related_name='Recipient', to=settings.AUTH_USER_MODEL)),
                ('subject_in_regards_to', models.ManyToManyField(default=1, to='QuickTutor.Class')),
            ],
        ),
        migrations.CreateModel(
            name='ClassNeedsHelp',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('elaboration', models.TextField()),
                ('class_id', models.ManyToManyField(default=1, to='QuickTutor.Class')),
                ('user', models.ManyToManyField(default=1, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
