# Generated by Django 3.2.16 on 2024-07-07 11:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_studentprofile_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Faculty',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('short_form', models.CharField(blank='True', max_length=50)),
                ('gender', models.CharField(choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')], max_length=1)),
                ('qualification', models.CharField(max_length=255)),
                ('designation', models.CharField(blank='True', max_length=255)),
                ('expertise', models.CharField(max_length=255)),
            ],
            options={
                'verbose_name_plural': 'Faculties',
                'unique_together': {('name', 'short_form')},
            },
        ),
        migrations.CreateModel(
            name='ResearchProject',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('project_name', models.CharField(max_length=255)),
                ('funding_agency', models.CharField(max_length=255)),
                ('agency_type', models.CharField(max_length=50)),
                ('submission_date', models.DateField()),
                ('funding_amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('duration', models.CharField(max_length=50)),
                ('pi_name', models.CharField(max_length=255)),
                ('co_pi_name', models.CharField(blank=True, max_length=255, null=True)),
                ('status', models.CharField(choices=[('Accepted', 'Accepted'), ('Not recommended', 'Not recommended'), ('Under Review', 'Under Review')], max_length=50)),
            ],
        ),
        migrations.AlterField(
            model_name='admission',
            name='admission_year',
            field=models.CharField(choices=[('2010', '2010'), ('2011', '2011'), ('2012', '2012'), ('2013', '2013'), ('2014', '2014'), ('2015', '2015'), ('2016', '2016'), ('2017', '2017'), ('2018', '2018'), ('2019', '2019'), ('2020', '2020'), ('2021', '2021'), ('2022', '2022'), ('2023', '2023'), ('2024', '2024')], default=2024, max_length=255),
        ),
        migrations.AlterField(
            model_name='placement',
            name='admission_year',
            field=models.CharField(choices=[('2010', '2010'), ('2011', '2011'), ('2012', '2012'), ('2013', '2013'), ('2014', '2014'), ('2015', '2015'), ('2016', '2016'), ('2017', '2017'), ('2018', '2018'), ('2019', '2019'), ('2020', '2020'), ('2021', '2021'), ('2022', '2022'), ('2023', '2023'), ('2024', '2024')], default=2024, max_length=255),
        ),
        migrations.AlterField(
            model_name='result',
            name='admission_year',
            field=models.CharField(choices=[('2010', '2010'), ('2011', '2011'), ('2012', '2012'), ('2013', '2013'), ('2014', '2014'), ('2015', '2015'), ('2016', '2016'), ('2017', '2017'), ('2018', '2018'), ('2019', '2019'), ('2020', '2020'), ('2021', '2021'), ('2022', '2022'), ('2023', '2023'), ('2024', '2024')], default=2024, max_length=255),
        ),
        migrations.AlterField(
            model_name='resultupload',
            name='admission_year',
            field=models.CharField(choices=[('2010', '2010'), ('2011', '2011'), ('2012', '2012'), ('2013', '2013'), ('2014', '2014'), ('2015', '2015'), ('2016', '2016'), ('2017', '2017'), ('2018', '2018'), ('2019', '2019'), ('2020', '2020'), ('2021', '2021'), ('2022', '2022'), ('2023', '2023'), ('2024', '2024')], default=2024, max_length=255),
        ),
        migrations.AlterField(
            model_name='studentprofile',
            name='admission_year',
            field=models.CharField(choices=[('2010', '2010'), ('2011', '2011'), ('2012', '2012'), ('2013', '2013'), ('2014', '2014'), ('2015', '2015'), ('2016', '2016'), ('2017', '2017'), ('2018', '2018'), ('2019', '2019'), ('2020', '2020'), ('2021', '2021'), ('2022', '2022'), ('2023', '2023'), ('2024', '2024')], default=2024, max_length=255),
        ),
        migrations.CreateModel(
            name='Publication',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('publication_type', models.CharField(choices=[('JOURNAL', 'Journal'), ('CONFERENCE', 'Conference'), ('ARTICLE', 'Article'), ('BOOK', 'Book'), ('OTHER', 'Other')], max_length=50)),
                ('publication_date', models.DateField()),
                ('publication_year', models.CharField(choices=[('1996', '1996'), ('1997', '1997'), ('1998', '1998'), ('1999', '1999'), ('2000', '2000'), ('2001', '2001'), ('2002', '2002'), ('2003', '2003'), ('2004', '2004'), ('2005', '2005'), ('2006', '2006'), ('2007', '2007'), ('2008', '2008'), ('2009', '2009'), ('2010', '2010'), ('2011', '2011'), ('2012', '2012'), ('2013', '2013'), ('2014', '2014'), ('2015', '2015'), ('2016', '2016'), ('2017', '2017'), ('2018', '2018'), ('2019', '2019'), ('2020', '2020'), ('2021', '2021'), ('2022', '2022'), ('2023', '2023'), ('2024', '2024')], max_length=50)),
                ('link', models.URLField(blank=True, null=True)),
                ('authors', models.ManyToManyField(related_name='publications', to='api.Faculty')),
            ],
        ),
        migrations.CreateModel(
            name='AcceptedProject',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('research_project', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='api.researchproject')),
            ],
        ),
    ]