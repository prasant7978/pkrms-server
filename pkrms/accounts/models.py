from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone




class Province(models.Model):
    code = models.CharField(max_length=10, unique=True, verbose_name="Province Code")
    name = models.CharField(max_length=100, verbose_name="Province Name")
    default_province = models.BooleanField(default=False, verbose_name="Default Province")
    stable_network_objective = models.TextField(verbose_name="Stable Network Objective")

    def __str__(self):
        return self.name


class Balai(models.Model):
    province = models.ForeignKey(Province, on_delete=models.CASCADE, verbose_name="Province")
    name = models.CharField(max_length=100, verbose_name="Balai Name")
    balai_code = models.BigIntegerField(null=True, blank=True, verbose_name="Balai Code")

    def __str__(self):
        return f"{self.name} - {self.province.name}"





class Kabupaten(models.Model):
    province = models.ForeignKey(Province, on_delete=models.CASCADE, related_name="kabupatens", verbose_name="Province")
    balai = models.ForeignKey(Balai, on_delete=models.CASCADE, related_name="kabupatens", verbose_name="Balai")
    
    name = models.CharField(max_length=100, verbose_name="Kabupaten Name")
    code = models.CharField(max_length=10, unique=True, verbose_name="Kabupaten Code")
    default_kabupaten = models.BooleanField(default=False, verbose_name="Default Kabupaten")
    stable_network_objective = models.TextField(verbose_name="Stable Network Objective")

    def __str__(self):
        return self.name

    

class PriorityArea(models.Model):
    name = models.CharField(max_length=100, verbose_name="Priority Area Name")

    def __str__(self):
        return self.name




class Link(models.Model):
    # Status choices
    STATUS_CHOICES = [
        ('provincial', 'Provincial'),
        ('kabupaten', 'Kabupaten'),
    ]
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        verbose_name="Link Status",
        null=True,
        blank=True
    )

    # Foreign keys to Province and Kabupaten
    province = models.ForeignKey(
        Province,
        on_delete=models.CASCADE,
        related_name="links",
        verbose_name="Province Code",
        null=True,
        blank=True
    )
    kabupaten = models.ForeignKey(
        Kabupaten,
        on_delete=models.CASCADE,
        related_name="links",
        verbose_name="Kabupaten Code",
        null=True,
        blank=True
    )

    # Link details
    link_code = models.IntegerField(
        unique=True,
        verbose_name="Link Number",
        null=True,
        blank=True
    )
    link_name = models.CharField(
        max_length=255,
        verbose_name="Link Name",
        null=True,
        blank=True
    )
    link_length_official = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Link Official Length (km)",
        null=True,
        blank=True
    )
    link_length_actual = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Link Actual Length (km)",
        null=True,
        blank=True
    )

    # Access status choices
    HIGHEST_ACCESS_CHOICES = [
        ('nasional', 'Nasional'),
        ('provinsi', 'Provinsi'),
        ('kabupaten', 'Kabupaten'),
        ('lokal', 'Lokal'),
    ]
    access_status = models.CharField(
        max_length=20,
        choices=HIGHEST_ACCESS_CHOICES,
        verbose_name="Highest Link Access",
        null=True,
        blank=True
    )

    # Link function choices
    LINK_FUNCTION_CHOICES = [
        ('kollector_4', 'Kollector 4'),
        ('kollector_2', 'Kollector 2'),
        ('kollector_3', 'Kollector 3'),
        ('arterial', 'Arterial'),
        ('lokal', 'Lokal'),
        ('lingkungan', 'Lingkungan'),
    ]
    function = models.CharField(
        max_length=50,
        choices=LINK_FUNCTION_CHOICES,
        verbose_name="Link Function",
        null=True,
        blank=True
    )

    # Link class choices
    LINK_CLASS_CHOICES = [
        ('I', '10 tons'),
        ('II', '10 tons'),
        ('IIIA', '8 tons'),
        ('IIIB', '5 tons'),
        ('IIIC', '3.5 tons'),
    ]
    link_class = models.CharField(
        max_length=10,
        choices=LINK_CLASS_CHOICES,
        default='I',
        verbose_name="Link Class",
        null=True,
        blank=True
    )

    # Additional fields
    wti = models.IntegerField(null=True, blank=True)
    mca2 = models.IntegerField(null=True, blank=True)
    mca3 = models.IntegerField(null=True, blank=True)
    mca4 = models.IntegerField(null=True, blank=True)
    mca5 = models.IntegerField(null=True, blank=True)
    project_number = models.IntegerField(null=True, blank=True)
    cum_esa = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        verbose_name="Cumulative ESA",
        null=True,
        blank=True
    )
    esa0 = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        verbose_name="ESA0",
        null=True,
        blank=True
    )
    aadt = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        verbose_name="Annual Average Daily Traffic",
        null=True,
        blank=True
    )

    def __str__(self):
        return f"{self.link_name} ({self.link_code})"



    
    
   
class DRP(models.Model):
    # Foreign Keys
    
    province = models.ForeignKey('Province', on_delete=models.CASCADE, verbose_name="Province")
    kabupaten = models.ForeignKey('Kabupaten', on_delete=models.CASCADE, verbose_name="Kabupaten")
    link = models.ForeignKey('Link', on_delete=models.CASCADE, verbose_name="Link")

    # Unique Fields
    drp_number = models.CharField(max_length=50, unique=True, verbose_name="DRP Number", null=True,blank=True)
    chainage = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Chainage")
    drp_length = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="DRP Length")
    DRP_TYPE_CHOICES = [
        ('link_start', 'Link Start'),
        ('link_end', 'Link End'),
        ('km_post_existing', 'KM Post - Existing'),
        ('km_post_temporary', 'KM Post - Temporary'),
        ('pain', 'Pain'),
        ('junction', 'Junction'),
        ('other', 'Other'),
    ]
    
    drp_type = models.CharField(
        max_length=50, 
        choices=DRP_TYPE_CHOICES, 
        verbose_name="DRP Type"
    )
   
   
    drp_description = models.TextField(verbose_name="DRP Description", null=True, blank=True)
    comment = models.TextField(verbose_name="Comment", null=True, blank=True)

    # GPS Coordinates
    gps_north_degree = models.IntegerField(verbose_name="North Degree")
    gps_north_minute = models.IntegerField(verbose_name="North Minute")
    gps_north_second = models.FloatField(verbose_name="North Second")

    gps_east_degree = models.IntegerField(verbose_name="East Degree")
    gps_east_minute = models.IntegerField(verbose_name="East Minute")
    gps_east_second = models.FloatField(verbose_name="East Second")

    class Meta:
        verbose_name = "DRP"
        verbose_name_plural = "DRPs"
        unique_together = ('drp_number', 'chainage')  # Ensures drp_number and chainage are unique together

    def __str__(self):
        return f"DRP {self.drp_number} ({self.link})"
class LinkClass(models.Model):
    province = models.ForeignKey('Province', on_delete=models.CASCADE, verbose_name="Province")
    kabupaten = models.ForeignKey('Kabupaten', on_delete=models.CASCADE, verbose_name="Kabupaten")
    link = models.ForeignKey('Link', on_delete=models.CASCADE, verbose_name="Link")
    KmClass = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Kilometer Class")
    LINK_CLASS_CHOICES = [
        ('I', '10 tons'),
        ('II', '10 tons'),
        ('IIIA', '8 tons'),
        ('IIIB', '5 tons'),
        ('IIIC', '3.5 tons'),
    ]

    # Example of the new field
    Class = models.CharField(
        max_length=10,
        choices= LINK_CLASS_CHOICES,
        default='I',
       
    )






class LinkKabupaten(models.Model):
    """Model for Link-Kabupaten Relationships with extra foreign key logic."""
    link = models.ForeignKey(Link, on_delete=models.CASCADE, verbose_name="Link")
    kabupaten = models.ForeignKey(Kabupaten, on_delete=models.CASCADE, verbose_name="Kabupaten")
    province = models.ForeignKey(Province, on_delete=models.CASCADE, verbose_name="Province")
    #link_status = models.CharField(max_length=20, choices=Link.STATUS_CHOICES)  # Link status from the Link model
    drp_from = models.IntegerField(null=True, blank=True)
    drp_to = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.link.link_name} - {self.kabupaten.name} from {self.drp_from} to {self.drp_to}"
    


class LinkKacematan(models.Model):
    link = models.ForeignKey(Link, on_delete=models.CASCADE, verbose_name="Link")
    kabupaten = models.ForeignKey(Kabupaten, on_delete=models.CASCADE, verbose_name="Kabupaten")
    province = models.ForeignKey(Province, on_delete=models.CASCADE, verbose_name="Province")
   # link_status = models.CharField(max_length=20, choices=Link.STATUS_CHOICES)  # Link status from the Link model
    drp_from = models.IntegerField(null=True, blank=True)
    drp_to = models.IntegerField(null=True, blank=True)
    def __str__(self):
        return f"{self.link.link_name} - {self.kabupaten.name} from {self.drp_from} to {self.drp_to}"
    




    

# Culvert Section API  for pkrms 

class CulvertInventory(models.Model):
    link = models.ForeignKey('Link', on_delete=models.CASCADE, verbose_name="Link")
    kabupaten = models.ForeignKey('Kabupaten', on_delete=models.CASCADE, verbose_name="Kabupaten")
    province = models.ForeignKey('Province', on_delete=models.CASCADE, verbose_name="Province")
    
    

    # Other fields
    chainage = models.FloatField(help_text="Chainage in kilometers")
    culvert_number = models.CharField(max_length=50, help_text="Culvert identification number")
    culvert_length = models.FloatField(help_text="Length of the culvert in meters")
    number_of_openings = models.IntegerField(help_text="Number of openings in the culvert")

    # Choices for culvert type
    CULVERT_TYPE_CHOICES = [
        ('gorong_gorong_kotak', 'Gorong-gorong Kotak'),
        ('gorong_gorong_pipa_beton', 'Gorong-gorong Pipa Beton'),
        ('gorong_gorong_pelat_beton', 'Gorong-gorong Pelat Beton'),
        ('gorong_gorong_pipa_baja', 'Gorong-gorong Pipa Baja'),
        ('lainnya', 'Lainnya'),
        ('struktur_diprelu', 'Struktur Diprelu'),
    ]
    culvert_type = models.CharField(max_length=50, choices=CULVERT_TYPE_CHOICES, help_text="Type of the culvert")

    culvert_width = models.FloatField(help_text="Width of the culvert in meters")
    culvert_height = models.FloatField(help_text="Height of the culvert in meters")

    # Choices for inlet type
    INLET_TYPE_CHOICES = [
        ('non_stuktr', 'Non Stuktr'),
        ('apron_dan_tembok_sayap', 'Apron dan Tembok Sayap'),
        ('tembok_sayap', 'Tembok Sayap'),
        ('beronjong', 'Beronjong'),
        ('batu_kali', 'Batu Kali'),
        ('langsung_ke_drainase_lainnya', 'Langsung ke Drainase Lainnya'),
    ]
    inlet_type = models.CharField(max_length=50, choices=INLET_TYPE_CHOICES, help_text="Type of inlet structure")

    # Choices for outlet type
    OUTLET_TYPE_CHOICES = [
        ('non_stuktr', 'Non Stuktr'),
        ('apron_dan_tembok_sayap', 'Apron dan Tembok Sayap'),
        ('tembok_sayap', 'Tembok Sayap'),
        ('beronjong', 'Beronjong'),
        ('batu_kali', 'Batu Kali'),
        ('langsung_ke_drainase_lainnya', 'Langsung ke Drainase Lainnya'),
    ]
    outlet_type = models.CharField(max_length=50, choices=OUTLET_TYPE_CHOICES, help_text="Type of outlet structure")

    def __str__(self):
        return f"Culvert {self.culvert_number} at chainage {self.chainage}"
    

class CulvertCondition(models.Model):
    # Foreign Key Fields
    link = models.ForeignKey('Link', on_delete=models.CASCADE, verbose_name="Link")
    kabupaten = models.ForeignKey('Kabupaten', on_delete=models.CASCADE, verbose_name="Kabupaten")
    province = models.ForeignKey('Province', on_delete=models.CASCADE, verbose_name="Province")

    

    # Reference to the ConditionYear model
   
    culvert_number = models.ForeignKey('CulvertInventory', on_delete=models.CASCADE, verbose_name="Culvert Number")

    # Condition Choices
    CONDITION_CHOICES = [
        ('amat_baik', 'Amat Baik'),
        ('baik', 'Baik'),
        ('sedang', 'Sedang'),
        ('rusak_ringan', 'Rusak Ringan'),
        ('rusak_berat', 'Rusak Berat'),
        ('struktur_gagal', 'Struktur Gagal'),
        ('elemen_tak_dapat_disurvei', 'Elemen Tak Dapat Disurvei'),
    ]

    condition_barrel = models.CharField(
        max_length=50,
        choices=CONDITION_CHOICES,
        verbose_name="Condition Barrel",
        help_text="The condition of the barrel"
    )

    condition_inlet = models.CharField(
        max_length=50,
        choices=CONDITION_CHOICES,
        verbose_name="Condition Inlet",
        help_text="The condition of the inlet"
    )

    condition_outlet = models.CharField(
        max_length=50,
        choices=CONDITION_CHOICES,
        verbose_name="Condition Outlet",
        help_text="The condition of the outlet"
    )

    # Sitting Choices
    SITTING_CHOICES = [
        ('tak_ada', 'Tak Ada'),
        ('sedikit', 'Sedikit (<10 cm)'),
        ('banyak', 'Banyak (10-30 cm)'),
        ('tersumbat', 'Tersumbat'),
    ]
    sitting = models.CharField(
        max_length=50,
        choices=SITTING_CHOICES,
        verbose_name="Sitting",
        help_text="The sitting condition"
    )

    # Overtopping Field
    overtopping = models.BooleanField(
        verbose_name="Overtopping",
        help_text="Indicates if overtopping is present"
    )

    # Surveyed By Field
    surveyed_by = models.CharField(
        max_length=100,
        verbose_name="Surveyed By",
        help_text="Name of the person who surveyed"
    )

    def __str__(self):
        return f"Culvert Condition for {self.culvert_number}"
    

class Retaining_walls(models.Model):
    
    link = models.ForeignKey('Link', on_delete=models.CASCADE, verbose_name="Link", default=True)
    kabupaten = models.ForeignKey('Kabupaten', on_delete=models.CASCADE, verbose_name="Kabupaten", default=True)
    province = models.ForeignKey('Province', on_delete=models.CASCADE, verbose_name="Province", default=True)

    
    WALL_SIDE_CHOICES = [
        ('left', 'Left'),
        ('right', 'Right'),
    ]
    wall_side = models.CharField(
        max_length=20,
        choices=WALL_SIDE_CHOICES,
        verbose_name="wall side",
        
    )

    WALL_MATERIAL_CHOICES = [
        ("pasangan Batu", 'pasangan batu'),
        ("beton", 'Beton'),
        ("beronjong", 'Beronjong'),
        ("pelat beton", 'Pelot Beton'),
        ("lainnya", 'Lainnya'),
    ]
    wall_material = models.CharField(
        max_length=20,
        choices=WALL_MATERIAL_CHOICES,
        verbose_name="wall material",
        
    )
    wall_height = models.IntegerField(null=True, blank=True)
    chainage_from = models.IntegerField(null=True, blank=True)
    wall_number = models.IntegerField(null=True, blank=True )

    WALL_TYPE_CHOICES = [
        ('tembok bukit', "Tembok bukit"),
        ('tembok laut', "Tembok Laut"),
        ('tembok sungai', "Tembok Sungai"),
        ('lainnya', "Lainnya"),
        ('struktur diperlu', "Struktur Diperlu"),
    ]
    wall_type = models.CharField(
        max_length=20,
        choices=WALL_TYPE_CHOICES,
        verbose_name="wall_type",
        
    )


class Retaining_walls_Condition(models.Model):
    
    link = models.ForeignKey('Link', on_delete=models.CASCADE, verbose_name="Link", default=True)
    kabupaten = models.ForeignKey('Kabupaten', on_delete=models.CASCADE, verbose_name="Kabupaten", default=True)
    province = models.ForeignKey('Province', on_delete=models.CASCADE, verbose_name="Province", default=True)
    # Reference to the ConditionYear model
   
    wall_number = models.ForeignKey('Retaining_walls', on_delete=models.CASCADE, verbose_name="wall Number")
    # Link Status Choicescondition_ye
   

    wall_Mortar_needed = models.IntegerField(null=True, blank=True)
    wall_repair_needed = models.IntegerField(null=True, blank=True)
    wall_rebuiled_needed = models.IntegerField(null=True, blank=True)
    surveyed_by = models.CharField(max_length=200, null=True, blank=True)


# Create API model for traffic volume 


class Traffic_volume(models.Model):
    link = models.ForeignKey('Link', on_delete=models.CASCADE, verbose_name="Link", default=True)
    kabupaten = models.ForeignKey('Kabupaten', on_delete=models.CASCADE, verbose_name="Kabupaten", default=True)
    province = models.ForeignKey('Province', on_delete=models.CASCADE, verbose_name="Province", default=True)
   
    missing_data = models.BooleanField()
    surveyed_by = models.CharField(max_length=200, null=True, blank=True)
    survey_year = models.IntegerField( null=True, blank=True)
    journey_time = models.TimeField()
    TRAFFIC_COUNT_CHOICES = [
        ('stationary', 'Stationary'),
        ('moving count', 'Moving count'),
    ]
    traffic_count = models.CharField(
        max_length=20,
        choices=TRAFFIC_COUNT_CHOICES,
        verbose_name="traffic count",
        default=True,
    )

    AADT_MC = models.BigIntegerField(null=True, blank=True)
    AADT_Car = models.BigIntegerField(null=True, blank=True)
    AADT_Pickup = models.BigIntegerField(null=True, blank=True)
    AADT_Small_Bus = models.BigIntegerField(null=True, blank=True)
    AADT_Large_Bus = models.BigIntegerField(null=True, blank=True)
    AADT_Microtruk = models.BigIntegerField(null=True, blank=True)
    AADT_small_truck = models.BigIntegerField(null=True, blank=True)
    AADT_medium_truck = models.BigIntegerField(null=True, blank=True)
    AADT_large_truck = models.BigIntegerField(null=True, blank=True)
    AADT_truck_trailer = models.BigIntegerField(null=True, blank=True)
    AADT_semi_trailer = models.BigIntegerField(null=True, blank=True)


class Traffic_weighting_factors(models.Model):
    Car_WTI_FACTOR = models.BigIntegerField()
    Car_VDF_Factor = models.BigIntegerField()
    Large_bus_WTI_FACTOR = models.BigIntegerField()
    Large_bus_VDF_Factor = models.BigIntegerField()
    Large_truck_WTI_FACTOR = models.BigIntegerField()
    Large_truck_VDF_Factor = models.BigIntegerField()
    MC_WTI_FACTOR = models.BigIntegerField()
    MC_VDF_Factor = models.BigIntegerField()
    MEDIUM_TRUCK_WTI_FACTOR = models.BigIntegerField()
    MEDIUM_TRUCK_VDF_Factor = models.BigIntegerField()
    Microtruk_WTI_FACTOR = models.BigIntegerField()
    Microtruk_VDF_Factor = models.BigIntegerField()
    Pickup_WTI_FACTOR = models.BigIntegerField()
    Pickup_VDF_Factor = models.BigIntegerField()



  # hirerachy level code 


  
class Role(models.Model):
    SUPERADMIN = 'superadmin'
    PFID = 'pfid'
    BALAI_LG = 'balai_lg'
    PROVINCIAL_LG = 'provience_lg'
    KABUPATEN_LG = 'kabupaten_lg'

    ROLE_CHOICES = [
        (SUPERADMIN, 'Super Admin'),
        (PFID, 'PFID'),
        (BALAI_LG, 'Balai LG'),
        (PROVINCIAL_LG, 'Provincial LG'),
        (KABUPATEN_LG, 'Kabupaten LG'),
    ]

    role_name = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default=PFID,
        verbose_name="Role",
        unique=True,
    )

    def __str__(self):
        return self.role_name
    
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone

class CustomUserManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self.create_user(email, username, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=30, unique=True)  # Added unique=True to username
    name = models.CharField(max_length=100, blank=True, null=True, verbose_name="Full Name")
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)  # Default is False for regular users
    date_joined = models.DateTimeField(default=timezone.now)
    
    balai = models.ForeignKey('Balai', on_delete=models.CASCADE, null=True, blank=True)
    province = models.ForeignKey('Province', on_delete=models.CASCADE, null=True, blank=True)
    Kabupaten = models.ForeignKey('Kabupaten', on_delete=models.CASCADE, null=True, blank=True)
    
    approved = models.BooleanField(default=False)
    role = models.ForeignKey('Role', on_delete=models.CASCADE, null=True, blank=True, related_name="users")

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']  # Since email is the USERNAME_FIELD, username is required here

    def __str__(self):
        return self.username

class ApprovalRequest(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='approval_request')
    approver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='pending_approvals')
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20,
        choices=[('Pending', 'Pending'), ('Approved', 'Approved'), ('Rejected', 'Rejected')],
        default='Pending'
    )


#models for Roads 

class RoadInventory(models.Model):
    # Foreign Key Fields
    link = models.ForeignKey(Link, on_delete=models.CASCADE, verbose_name="Link", default=True)
    kabupaten = models.ForeignKey(Kabupaten, on_delete=models.CASCADE, verbose_name="Kabupaten", default=True)
    province = models.ForeignKey(Province, on_delete=models.CASCADE, verbose_name="Province", default=True)

   
    chainage_from = models.IntegerField(verbose_name="Chainage From (km)")
    chainage_to = models.IntegerField(verbose_name="Chainage To (km)")
    DRP_from = models.IntegerField(verbose_name="drp in (km)")
    DRP_to = models.IntegerField()
    offset_from=models.IntegerField()
    offset_to =models.IntegerField()
    pave_width = models.IntegerField()
    row = models.IntegerField()
    
    should_width_L = models.IntegerField()
    should_width_R = models.IntegerField()



    # Pavement Type Choices
    PAVEMENT_TYPE_CHOICES = [
        ('beton', 'Beton'),
        ('blok_beton', 'Blok Beton'),
        ('aspal', 'Aspal'),
        ('lapen', 'Lapen'),
        ('batu_kali', 'Batu Kali'),
        ('kerikil', 'Kerikil'),
        ('tanah', 'Tanah'),
    ]
    pavement_type = models.CharField(
        max_length=20,
        choices=PAVEMENT_TYPE_CHOICES,
        verbose_name="Pavement Type",
    )

    # Shoulder Fields
    shoulder_L_width = models.IntegerField(verbose_name="Shoulder Left Width (m)", null=True, blank=True)
    shoulder_L_type = models.CharField(
        max_length=20,
        choices=PAVEMENT_TYPE_CHOICES,
        verbose_name="Shoulder Left Type",
        null=True,
        blank=True,
    )
    shoulder_R_width = models.FloatField(verbose_name="Shoulder Right Width (m)", null=True, blank=True)
    shoulder_R_type = models.CharField(
        max_length=20,
        choices=PAVEMENT_TYPE_CHOICES,
        verbose_name="Shoulder Right Type",
        null=True,
        blank=True,
    )

    # Drain Type Choices
    DRAIN_TYPE_CHOICES = [
        ('tak_ada', 'Tak Ada'),
        ('tak_perlu', 'Tak Perlu'),
        ('tanah', 'Tanah'),
        ('pasangan_batu_terbuka', 'Pasangan Batu Terbuka'),
        ('pasangan_batu_tertutup', 'Pasangan Batu Tertutup'),
    ]
    drain_type_left = models.CharField(
        max_length=30,
        choices=DRAIN_TYPE_CHOICES,
        verbose_name="Drain Type Left",
        null=True,
        blank=True,
    )
    drain_type_right = models.CharField(
        max_length=30,
        choices=DRAIN_TYPE_CHOICES,
        verbose_name="Drain Type Right",
        null=True,
        blank=True,
    )

    # Land Use Choices
    LAND_USE_CHOICES = [
        ('tak_ada', 'Tak Ada'),
        ('agrikultur', 'Agrikultur'),
        ('desa', 'Desa'),
        ('kota', 'Kota'),
        ('hutan', 'Hutan'),
    ]
    land_use_left = models.CharField(
        max_length=20,
        choices=LAND_USE_CHOICES,
        verbose_name="Land Use Left",
        null=True,
        blank=True,
    )
    land_use_right = models.CharField(
        max_length=20,
        choices=LAND_USE_CHOICES,
        verbose_name="Land Use Right",
        null=True,
        blank=True,
    )

    # Terrain Choices
    TERRAIN_CHOICES = [
        ('datar', 'Datar'),
        ('bukit', 'Bukit'),
        ('gunung', 'Gunung'),
    ]
    terrain = models.CharField(
        max_length=20,
        choices=TERRAIN_CHOICES,
        verbose_name="Terrain",
    )

    # Impassable Fields
    impassable = models.BooleanField(verbose_name="Impassable", default=False)
    IMPASSABLE_REASON_CHOICES = [
        ('jembatan_runtuh', 'Jembatan Runtuh'),
        ('sungai_tanpa_jembatan', 'Sungai Tanpa Jembatan'),
        ('tak_dapat_dilalui_musim', 'Tak Dapat Dilalui Selama Musim'),
        ('lainnya', 'Lainnya'),
    ]
    reason = models.CharField(
        max_length=30,
        choices=IMPASSABLE_REASON_CHOICES,
        verbose_name="Reason",
        null=True,
        blank=True,
    )

    def __str__(self):
        return f"{self.link} - {self.province} - {self.kabupaten} - {self.chainage_from} to {self.chainage_to} km"
    



class RoadCondition(models.Model):
    # Foreign Keys
    province = models.ForeignKey('Province', on_delete=models.CASCADE, related_name='road_conditions')
    
    kabupaten = models.ForeignKey('Kabupaten', on_delete=models.CASCADE, related_name='road_conditions')
    link = models.ForeignKey('Link', on_delete=models.CASCADE, related_name='road_conditions')

    # Chainage
    chainage_from = models.FloatField()
    chainage_to = models.FloatField()

    # Boolean Fields
    roughness = models.BooleanField(default=False)
    road_marking_left = models.BooleanField(default=False)
    road_marking_right = models.BooleanField(default=False)
    analysis_base_year = models.BooleanField(default=False)
    paved = models.BooleanField(default=False)
    check_data = models.BooleanField(default=False)

    # Area Fields (float for precision)
    bleeding_area = models.FloatField()
    ravelling_area = models.FloatField()
    desintegration_area = models.FloatField()
    crack_dep_area = models.FloatField()
    patching_area = models.FloatField()
    oth_crack_area = models.FloatField()
    pothole_area = models.FloatField()
    rutting_area = models.FloatField()
    edge_damage_area = models.FloatField()
    crossfall_area = models.FloatField()
    depressions_area = models.FloatField()
    erosion_area = models.FloatField()
    waviness_area = models.FloatField()
    gravel_thickness_area = models.FloatField()
    concrete_cracking_area = models.FloatField()
    concrete_spalling_area = models.FloatField()
    concrete_structural_cracking_area = models.FloatField()

    # Choices for Conditions
    SHOULDER_OPTIONS = [
        ('tidak_ada', 'Tidak Ada'),
        ('di_atas_perkerasan', 'Di Atas Perkerasan'),
        ('sama_tinggi', 'Sama Tinggi Dengan Perkerasan'),
        ('di_bawah_perkerasan', 'Di Bawah Perkerasan'),
        ('diperlukan_bahu_beton', 'Diperlukan Bahu Beton'),
    ]
    shoulder_left = models.CharField(max_length=50, choices=SHOULDER_OPTIONS)
    shoulder_right = models.CharField(max_length=50, choices=SHOULDER_OPTIONS)

    DRAIN_OPTIONS = [
        ('tersumbat', 'Tersumbat'),
        ('tidak_ada', 'Tidak Ada'),
        ('bersih', 'Bersih'),
        ('diperlukan_pasangan', 'Diperlukan Drainase Pasangan'),
        ('diperlukan_tanah', 'Diperlukan Drainase Tanah'),
        ('erosi', 'Erosi'),
    ]
    drain_left = models.CharField(max_length=50, choices=DRAIN_OPTIONS)
    drain_right = models.CharField(max_length=50, choices=DRAIN_OPTIONS)

    SLOPE_OPTIONS = [
        ('tidak_ada', 'Tidak Ada'),
        ('runtuh', 'Runtuh'),
    ]
    slope_left = models.CharField(max_length=50, choices=SLOPE_OPTIONS)
    slope_right = models.CharField(max_length=50, choices=SLOPE_OPTIONS)

    FOOTPATH_OPTIONS = [
        ('tidak_ada', 'Tidak Ada'),
        ('baik_aman', 'Baik/Aman'),
        ('bahaya', 'Bahaya'),
    ]
    footpath_left = models.CharField(max_length=50, choices=FOOTPATH_OPTIONS)
    footpath_right = models.CharField(max_length=50, choices=FOOTPATH_OPTIONS)

    # Road Furniture
    sign_left = models.FloatField()
    sign_right = models.FloatField()
    guidepost_left = models.FloatField()
    guidepost_right = models.FloatField()
    barrier_left = models.FloatField()
    barrier_right = models.FloatField()

    # Additional Fields
    iri = models.FloatField()
    rci = models.FloatField()
    segment_tti = models.FloatField()
    survey_by = models.CharField(max_length=255)
    survey_date = models.DateField()
    section_status = models.CharField(max_length=255)
    
    # Pavement Fields
    PAVEMENT_OPTIONS = [
        ('asphalt', 'Asphalt'),
        ('concrete', 'Concrete'),
        ('unpaved', 'Unpaved'),
    ]
    pavement = models.CharField(max_length=50, choices=PAVEMENT_OPTIONS)

    # Concrete Specific Fields
    concrete_corner_break_no = models.IntegerField()
    concrete_pumping_no = models.IntegerField()
    concrete_blowouts_area = models.FloatField()

    # Composition
    COMPOSITION_OPTIONS = [
        ('baik_rapat', 'Baik/Rapat'),
        ('kasar', 'Kasar'),
    ]
    composition = models.CharField(max_length=50, choices=COMPOSITION_OPTIONS)

    # Crack Details
    CRACK_TYPE_OPTIONS = [
        ('tidak_ada', 'Tidak Ada'),
        ('tidak_berhubungan', 'Tidak Berhubungan'),
        ('saling_berhubungan', 'Saling Berhubungan'),
    ]
    crack_type = models.CharField(max_length=50, choices=CRACK_TYPE_OPTIONS)

    CRACK_WIDTH_OPTIONS = [
        ('tidak_ada', 'Tidak Ada'),
        ('<1mm', '<1mm'),
        ('1-5mm', '1-5mm'),
        ('>5mm', '>5mm'),
    ]
    crack_width = models.CharField(max_length=50, choices=CRACK_WIDTH_OPTIONS)

    # Pothole and Rutting Details
    pothole_count = models.IntegerField()
    POTHOLE_SIZE_OPTIONS = [
        ('tidak_ada', 'Tidak Ada'),
        ('kecil_dangkal', 'Kecil-Dangkal'),
        ('kecil_dalam', 'Kecil-Dalam'),
        ('besar_dangkal', 'Besar-Dangkal'),
        ('besar_dalam', 'Besar-Dalam'),
    ]
    pothole_size = models.CharField(max_length=50, choices=POTHOLE_SIZE_OPTIONS)

    RUT_DEPTH_OPTIONS = [
        ('tidak_ada', 'Tidak Ada'),
        ('<1cm', '<1cm'),
        ('1-3cm', '1-3cm'),
        ('>3cm', '>3cm'),
    ]
    rut_depth = models.CharField(max_length=50, choices=RUT_DEPTH_OPTIONS)

    # Shoulder Conditions
    SHOULDER_COND_OPTIONS = [
        ('tidak_ada', 'Tidak Ada'),
        ('baik_rata', 'Baik/Rata'),
        ('bekas_erosi_ringan', 'Bekas RD/Erosi Ringan'),
        ('bekas_erosi_berat', 'Bekas RD/Erosi Berat'),
    ]
    shoulder_cond_left = models.CharField(max_length=50, choices=SHOULDER_COND_OPTIONS)
    shoulder_cond_right = models.CharField(max_length=50, choices=SHOULDER_COND_OPTIONS)

    # Miscellaneous
    crossfall_shape = models.FloatField()
    gravel_size = models.FloatField()
    gravel_thickness = models.FloatField()
    distribution = models.FloatField()
    edge_damage_area_right = models.FloatField()

    def __str__(self):
        return f"Road Condition for {self.link} ({self.chainage_from} - {self.chainage_to})"
