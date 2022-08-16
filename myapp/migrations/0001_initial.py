# Generated by Django 4.0.2 on 2022-07-08 08:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Admin_register',
            fields=[
                ('reg_id', models.AutoField(primary_key=True, serialize=False)),
                ('fullname', models.CharField(default='', max_length=200)),
                ('username', models.CharField(max_length=100)),
                ('joining_date', models.DateTimeField(blank=True, null=True)),
                ('email', models.EmailField(max_length=100)),
                ('password', models.CharField(max_length=50)),
                ('designation', models.CharField(default='', max_length=100)),
                ('photo', models.FileField(blank=True, null=True, upload_to='images/')),
            ],
        ),
        migrations.CreateModel(
            name='categories',
            fields=[
                ('cat_id', models.AutoField(primary_key=True, serialize=False)),
                ('category_name', models.CharField(max_length=255)),
                ('category_logo', models.ImageField(default='default.png', upload_to='images')),
                ('sub_category1', models.CharField(max_length=255)),
                ('sub_category2', models.CharField(max_length=255)),
                ('sub_category3', models.EmailField(max_length=255)),
                ('sub_category4', models.CharField(max_length=255)),
                ('sub_category5', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, null=True)),
                ('email', models.CharField(max_length=200)),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_ordered', models.DateTimeField(auto_now_add=True)),
                ('complete', models.BooleanField(default=False)),
                ('transaction_id', models.CharField(max_length=100, null=True)),
                ('customer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='myapp.customer')),
            ],
        ),
        migrations.CreateModel(
            name='ShippingAddress',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(max_length=200)),
                ('city', models.CharField(max_length=200)),
                ('state', models.CharField(max_length=200)),
                ('zipcode', models.CharField(max_length=200)),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('customer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='myapp.customer')),
                ('order', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='myapp.order')),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('modelname', models.CharField(default='', max_length=200)),
                ('description', models.CharField(default='', max_length=255)),
                ('gib', models.FileField(blank=True, default='', null=True, upload_to='images/')),
                ('price', models.FloatField(default='')),
                ('types', models.CharField(default='', max_length=255)),
                ('format', models.CharField(default='', max_length=255)),
                ('modeltype', models.CharField(default='', max_length=255)),
                ('fbx', models.ImageField(default='default.png', upload_to='images')),
                ('digital', models.BooleanField(blank=True, default=False, null=True)),
                ('image', models.ImageField(blank=True, default='', null=True, upload_to='')),
                ('category', models.ForeignKey(default='', null=True, on_delete=django.db.models.deletion.CASCADE, to='myapp.categories')),
            ],
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(blank=True, default=0, null=True)),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('order', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='myapp.order')),
                ('product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='myapp.product')),
            ],
        ),
    ]