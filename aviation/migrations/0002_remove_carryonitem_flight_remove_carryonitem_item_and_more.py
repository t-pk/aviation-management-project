# Generated by Django 5.0.3 on 2024-04-01 07:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aviation', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='carryonitem',
            name='flight',
        ),
        migrations.RemoveField(
            model_name='carryonitem',
            name='item',
        ),
        migrations.RemoveField(
            model_name='carryonitem',
            name='passenger',
        ),
        migrations.RemoveField(
            model_name='paymentinformation',
            name='booking',
        ),
        migrations.RemoveField(
            model_name='passenger',
            name='passport_id',
        ),
        migrations.AddField(
            model_name='booking',
            name='total_amount',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.DeleteModel(
            name='ItemInformation',
        ),
        migrations.DeleteModel(
            name='CarryOnItem',
        ),
        migrations.DeleteModel(
            name='PaymentInformation',
        ),
    ]