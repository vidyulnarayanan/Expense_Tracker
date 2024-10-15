# Generated by Django 5.1.2 on 2024-10-15 18:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('expenses', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='expense',
            name='name',
        ),
        migrations.AddField(
            model_name='expense',
            name='description',
            field=models.CharField(default='Unnamed Expense', max_length=255),
        ),
        migrations.AlterField(
            model_name='expense',
            name='category',
            field=models.CharField(choices=[('Food', 'Food'), ('Transportation', 'Transportation'), ('Entertainment', 'Entertainment'), ('Utilities', 'Utilities'), ('Other', 'Other')], max_length=50),
        ),
        migrations.AlterField(
            model_name='expense',
            name='date',
            field=models.DateField(),
        ),
    ]