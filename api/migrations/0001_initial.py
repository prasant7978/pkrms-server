# Generated by Django 5.0.7 on 2025-02-14 16:01

import django.core.validators
import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Balai',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('balaiCode', models.CharField(max_length=5, unique=True)),
                ('balaiName', models.CharField(max_length=30)),
                ('contactPerson', models.CharField(max_length=20)),
            ],
            options={
                'db_table': 'Balai',
            },
        ),
        migrations.CreateModel(
            name='DrainCondition',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(blank=True, null=True)),
                ('codeDescriptionEng', models.CharField(blank=True, max_length=50, null=True)),
                ('codeDescriptionInd', models.CharField(blank=True, max_length=50, null=True)),
                ('order', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'DrainCondition',
            },
        ),
        migrations.CreateModel(
            name='DrainType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(blank=True, null=True)),
                ('codeDescriptionEng', models.CharField(blank=True, max_length=50, null=True)),
                ('codeDescriptionInd', models.CharField(blank=True, max_length=50, null=True)),
                ('order', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'DrainType',
            },
        ),
        migrations.CreateModel(
            name='FootPathCondition',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(blank=True, null=True)),
                ('codeDescriptionEng', models.CharField(blank=True, max_length=50, null=True)),
                ('codeDescriptionInd', models.CharField(blank=True, max_length=50, null=True)),
                ('order', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'FootPathCondition',
            },
        ),
        migrations.CreateModel(
            name='Impassible',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(blank=True, null=True)),
                ('codeDescriptionEng', models.CharField(blank=True, max_length=50, null=True)),
                ('codeDescriptionInd', models.CharField(blank=True, max_length=50, null=True)),
                ('order', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'Impassible',
            },
        ),
        migrations.CreateModel(
            name='Kabupaten',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('KabupatenCode', models.CharField(blank=True, default=None, max_length=5, null=True)),
                ('KabupatenName', models.CharField(max_length=255)),
                ('IslandCode', models.CharField(blank=True, max_length=5)),
                ('DefaultKabupaten', models.BooleanField(default=False)),
                ('Stable', models.IntegerField()),
            ],
            options={
                'db_table': 'kabupaten',
            },
        ),
        migrations.CreateModel(
            name='LandUse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(blank=True, null=True)),
                ('codeDescriptionEng', models.CharField(blank=True, max_length=50, null=True)),
                ('codeDescriptionInd', models.CharField(blank=True, max_length=50, null=True)),
                ('order', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'LandUse',
            },
        ),
        migrations.CreateModel(
            name='LinkClass',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(blank=True, null=True)),
                ('codeDescriptionEng', models.CharField(blank=True, max_length=50, null=True)),
                ('codeDescriptionInd', models.CharField(blank=True, max_length=50, null=True)),
                ('order', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'LinkClassCode',
            },
        ),
        migrations.CreateModel(
            name='LinkFunction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(blank=True, null=True)),
                ('codeDescriptionEng', models.CharField(blank=True, max_length=50, null=True)),
                ('codeDescriptionInd', models.CharField(blank=True, max_length=50, null=True)),
                ('order', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'LinkFunctionCode',
            },
        ),
        migrations.CreateModel(
            name='LinkStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(blank=True, null=True)),
                ('codeDescriptionEng', models.CharField(blank=True, max_length=50, null=True)),
                ('codeDescriptionInd', models.CharField(blank=True, max_length=50, null=True)),
                ('order', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'LinkStatusCode',
            },
        ),
        migrations.CreateModel(
            name='PavementType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(blank=True, null=True)),
                ('codeDescriptionEng', models.CharField(blank=True, max_length=50, null=True)),
                ('codeDescriptionInd', models.CharField(blank=True, max_length=50, null=True)),
                ('order', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'PavementType',
            },
        ),
        migrations.CreateModel(
            name='Province',
            fields=[
                ('provinceCode', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('provinceName', models.CharField(max_length=50)),
                ('defaultProvince', models.BooleanField(default=False)),
                ('stable', models.IntegerField()),
            ],
            options={
                'db_table': 'province',
            },
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role_name', models.CharField(choices=[('pfid', 'PFID'), ('dpsi', 'DPSI'), ('spdjd', 'SPDJD'), ('balai', 'Balai '), ('provience_lg', 'Provincial LG'), ('kabupaten_lg', 'Kabupaten LG')], default='pfid', max_length=20, unique=True, verbose_name='Role')),
            ],
        ),
        migrations.CreateModel(
            name='ShoulderCondition',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(blank=True, null=True)),
                ('codeDescriptionEng', models.CharField(blank=True, max_length=50, null=True)),
                ('codeDescriptionInd', models.CharField(blank=True, max_length=50, null=True)),
                ('order', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'ShoulderCondition',
            },
        ),
        migrations.CreateModel(
            name='ShoulderType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(blank=True, null=True)),
                ('codeDescriptionEng', models.CharField(blank=True, max_length=50, null=True)),
                ('codeDescriptionInd', models.CharField(blank=True, max_length=50, null=True)),
                ('order', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'ShouderType',
            },
        ),
        migrations.CreateModel(
            name='SlopeCondition',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(blank=True, null=True)),
                ('codeDescriptionEng', models.CharField(blank=True, max_length=50, null=True)),
                ('codeDescriptionInd', models.CharField(blank=True, max_length=50, null=True)),
                ('order', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'SlopeCondition',
            },
        ),
        migrations.CreateModel(
            name='Terrain',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(blank=True, null=True)),
                ('codeDescriptionEng', models.CharField(blank=True, max_length=50, null=True)),
                ('codeDescriptionInd', models.CharField(blank=True, max_length=50, null=True)),
                ('order', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'Terrain',
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('username', models.CharField(max_length=30, unique=True)),
                ('phone_number', models.CharField(blank=True, max_length=15, null=True, validators=[django.core.validators.RegexValidator(message='Phone number must be in Indonesian format, starting with +62 followed by 9 to 13 digits.', regex='^\\+62\\d{9,13}$')])),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now)),
                ('approved', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
                ('balai', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.balai')),
                ('Kabupaten', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.kabupaten')),
                ('province', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.province')),
                ('role', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='users', to='api.role')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ApprovalRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(choices=[('Pending', 'Pending'), ('Approved', 'Approved'), ('Rejected', 'Rejected')], default='Pending', max_length=20)),
                ('approver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pending_approvals', to=settings.AUTH_USER_MODEL)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='approval_request', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Link',
            fields=[
                ('linkId', models.CharField(primary_key=True, serialize=False)),
                ('linkNo', models.CharField(unique=True)),
                ('linkCode', models.CharField(unique=True)),
                ('linkName', models.CharField(blank=True, max_length=100, null=True)),
                ('linkLengthOfficial', models.FloatField(blank=True, null=True)),
                ('linkLengthActual', models.FloatField(blank=True, null=True)),
                ('status', models.CharField(unique=True)),
                ('function', models.CharField(unique=True)),
                ('class_field', models.CharField(unique=True)),
                ('wti', models.IntegerField(blank=True, null=True)),
                ('mca2', models.IntegerField(blank=True, null=True)),
                ('mca3', models.IntegerField(blank=True, null=True)),
                ('mca4', models.IntegerField(blank=True, null=True)),
                ('mca5', models.IntegerField(blank=True, null=True)),
                ('projectNumber', models.CharField(blank=True, null=True)),
                ('cumesa', models.FloatField(blank=True, null=True)),
                ('esa0', models.FloatField(blank=True, null=True)),
                ('aadt', models.IntegerField(blank=True, null=True)),
                ('accessStatus', models.CharField(blank=True, null=True)),
                ('inbound', models.CharField(blank=True, null=True)),
                ('kabupaten', models.CharField(unique=True)),
                ('province', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.province')),
            ],
            options={
                'db_table': 'link',
            },
        ),
        migrations.AddField(
            model_name='kabupaten',
            name='Province',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.province'),
        ),
        migrations.AddField(
            model_name='balai',
            name='provinceCode',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.province', verbose_name='Province code'),
        ),
        migrations.CreateModel(
            name='RoadCondition',
            fields=[
                ('roadConditionId', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('analysisBaseYear', models.CharField(blank=True, null=True)),
                ('barrierL', models.CharField(blank=True, null=True)),
                ('barrierR', models.CharField(blank=True, null=True)),
                ('bleedingArea', models.CharField(blank=True, null=True)),
                ('chainageFrom', models.CharField()),
                ('chainageTo', models.CharField()),
                ('checkData', models.CharField()),
                ('composition', models.CharField(blank=True, null=True)),
                ('concreteBlowoutsArea', models.CharField(blank=True, null=True)),
                ('concreteCornerBreakNo', models.CharField(blank=True, null=True)),
                ('concreteCrackingArea', models.CharField(blank=True, max_length=50, null=True)),
                ('concretePumpingNo', models.CharField(blank=True, null=True)),
                ('concreteSpallingArea', models.CharField(blank=True, max_length=50, null=True)),
                ('concreteStructuralCrackingArea', models.CharField(blank=True, max_length=50, null=True)),
                ('crackDepArea', models.CharField(blank=True, null=True)),
                ('crackType', models.CharField(blank=True, null=True)),
                ('crackWidth', models.CharField(blank=True, null=True)),
                ('crossfallArea', models.CharField(blank=True, null=True)),
                ('crossfallShape', models.CharField(blank=True, max_length=50, null=True)),
                ('desintegrationArea', models.CharField(blank=True, null=True)),
                ('distribution', models.CharField(blank=True, max_length=50, null=True)),
                ('drpFrom', models.CharField(blank=True, max_length=50, null=True)),
                ('drpTo', models.CharField(blank=True, max_length=50, null=True)),
                ('edgeDamageArea', models.CharField(blank=True, null=True)),
                ('depressionsArea', models.CharField(blank=True, null=True)),
                ('erosionArea', models.CharField(blank=True, null=True)),
                ('shoulderCondL', models.CharField(blank=True, max_length=50, null=True)),
                ('shoulderCondR', models.CharField(blank=True, max_length=50, null=True)),
                ('edgeDamageAreaR', models.CharField(blank=True, null=True)),
                ('drainL', models.CharField()),
                ('drainR', models.CharField()),
                ('footpathL', models.CharField()),
                ('footpathR', models.CharField()),
                ('shoulderL', models.CharField()),
                ('shoulderR', models.CharField()),
                ('slopeL', models.CharField()),
                ('slopeR', models.CharField()),
                ('gravelSize', models.CharField(blank=True, max_length=50, null=True)),
                ('gravelThickness', models.CharField(blank=True, max_length=50, null=True)),
                ('gravelThicknessArea', models.CharField(blank=True, null=True)),
                ('guidepostL', models.CharField(blank=True, null=True)),
                ('guidepostR', models.CharField(blank=True, null=True)),
                ('iri', models.CharField(blank=True, max_length=50, null=True)),
                ('offsetFrom', models.CharField(blank=True, null=True)),
                ('offsetTo', models.CharField(blank=True, null=True)),
                ('othCrackArea', models.CharField(blank=True, null=True)),
                ('paved', models.CharField()),
                ('pavement', models.CharField(blank=True, max_length=100, null=True)),
                ('patchingArea', models.CharField(blank=True, null=True)),
                ('potholeArea', models.CharField(blank=True, null=True)),
                ('potholeCount', models.CharField(blank=True, null=True)),
                ('potholeSize', models.CharField(blank=True, null=True)),
                ('rci', models.CharField(blank=True, max_length=50, null=True)),
                ('ravellingArea', models.CharField(blank=True, null=True)),
                ('roadMarkingL', models.CharField(blank=True, default=False, null=True)),
                ('roadMarkingR', models.CharField(blank=True, default=False, null=True)),
                ('roughness', models.CharField()),
                ('ruttingArea', models.CharField(blank=True, null=True)),
                ('ruttingDepth', models.CharField(blank=True, null=True)),
                ('sectionStatus', models.CharField(blank=True, null=True)),
                ('segmentTti', models.CharField(blank=True, max_length=50, null=True)),
                ('signL', models.CharField(blank=True, null=True)),
                ('signR', models.CharField(blank=True, null=True)),
                ('surveyBy', models.CharField(blank=True, max_length=50, null=True)),
                ('surveyBy2', models.CharField(blank=True, max_length=50, null=True)),
                ('surveyDate', models.CharField()),
                ('wavinessArea', models.CharField(blank=True, null=True)),
                ('year', models.CharField()),
                ('linkId', models.ForeignKey(db_column='linkId', on_delete=django.db.models.deletion.CASCADE, related_name='road_conditions', to='api.link')),
            ],
            options={
                'db_table': 'roadcondition',
            },
        ),
        migrations.CreateModel(
            name='RoadInventory',
            fields=[
                ('roadInventoryId', models.CharField(primary_key=True, serialize=False)),
                ('linkNo', models.CharField(blank=True, null=True)),
                ('chainageFrom', models.IntegerField(blank=True, null=True)),
                ('chainageTo', models.IntegerField(blank=True, null=True)),
                ('drpFrom', models.IntegerField(blank=True, null=True)),
                ('offsetFrom', models.IntegerField(blank=True, null=True)),
                ('drpTo', models.IntegerField(blank=True, null=True)),
                ('offsetTo', models.IntegerField(blank=True, null=True)),
                ('paveWidth', models.FloatField(blank=True, null=True)),
                ('row', models.FloatField(blank=True, null=True)),
                ('paveType', models.IntegerField(blank=True, null=True)),
                ('shoulderWidthL', models.FloatField(blank=True, null=True)),
                ('shoulderWidthR', models.FloatField(blank=True, null=True)),
                ('impassable', models.BooleanField()),
                ('impassableReason', models.CharField(blank=True, null=True)),
                ('shoulderTypeL', models.IntegerField(blank=True, null=True)),
                ('shoulderTypeR', models.IntegerField(blank=True, null=True)),
                ('drainTypeL', models.IntegerField(blank=True, null=True)),
                ('drainTypeR', models.IntegerField(blank=True, null=True)),
                ('terrain', models.IntegerField(blank=True, null=True)),
                ('landUseL', models.IntegerField(blank=True, null=True)),
                ('landUseR', models.IntegerField(blank=True, null=True)),
                ('linkId', models.ForeignKey(db_column='linkId', on_delete=django.db.models.deletion.CASCADE, related_name='road_inventory', to='api.link')),
            ],
            options={
                'db_table': 'roadinventory',
            },
        ),
    ]
