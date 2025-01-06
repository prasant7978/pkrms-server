from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone




class Balai(models.Model):
    
    name = models.CharField(max_length=100, verbose_name="Balai Name")
    balai_code = models.BigIntegerField(null=True, blank=True)
    def __str__(self):
        return self.name
class Province(models.Model):
    balai = models.ForeignKey(Balai, on_delete=models.CASCADE, verbose_name="BALAI")
    code = models.CharField(max_length=10, unique=True, verbose_name="Province Code")
    name = models.CharField(max_length=100, verbose_name="Province Name")
    default_province = models.BooleanField(default=False, verbose_name="Default Province")
    stable_network_objective = models.TextField(verbose_name="Stable Network Objective")

    def __str__(self):
        return self.name




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


class CorridorName(models.Model):
    name = models.CharField(max_length=100, verbose_name="Corridor Name")

    def __str__(self):
        return self.name

class Link(models.Model):
    # Foreign key to link status
    STATUS_CHOICES = [
        ('provincial', 'Provincial'),
        ('Kabupaten', 'Kabupaten'),
       
    ]
    link_status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        verbose_name="Link Status",
        null=True,
        blank=True
    )

    # Foreign key to Province and Kabupaten
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

    # Link fields
    link_number = models.IntegerField(
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
    link_function = models.CharField(
        max_length=255, 
        verbose_name="Link Function",
        null=True,
        blank=True
    )
    official_length_km = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        verbose_name="Link Official Length (km)",
        null=True,
        blank=True
    )
    actual_length_km = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        verbose_name="Link Actual Length (km)",
        null=True,
        blank=True
    )

    # Choices for highest access (without forcing a default)
    HIGHEST_ACCESS_CHOICES = [
        ('nasional', 'Nasional'),
        ('provinsi', 'Provinsi'),
        ('kabupaten', 'Kabupaten'),
        ('lokal', 'Lokal'),
    ]
    highest_access = models.CharField(
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
    link_function = models.CharField(
        max_length=50, 
        choices=LINK_FUNCTION_CHOICES, 
        verbose_name="Link Function",
        null=True,
        blank=True
    )
    priority_area = models.ForeignKey(PriorityArea, on_delete=models.SET_NULL, null=True, blank=True)
    corridor_name = models.ForeignKey(CorridorName, on_delete=models.SET_NULL, null=True, blank=True)
    def __str__(self):
        return f"{self.link_name} ({self.link_number})"




    
    
   
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
    total_length = models.IntegerField(null=True, blank = True)
    unit = models.CharField(
        max_length=10,
        default='km',
        verbose_name="Unit of Measurement"
    )
    LINK_CLASS_CHOICES = [
        ('I', '10 tons'),
        ('II', '10 tons'),
        ('IIIA', '8 tons'),
        ('IIIB', '5 tons'),
        ('IIIC', '3.5 tons'),
    ]

    # Example of the new field
    link_class = models.CharField(
        max_length=10,
        choices= LINK_CLASS_CHOICES,
        default='I',
       
    )



class CorridorLink(models.Model):
    link = models.ForeignKey('Link', on_delete=models.CASCADE, related_name="corridor_links", verbose_name="Link")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")

    def __str__(self):
        return f"{self.link.link_name} - {self.link.link_number}"



class LinkKabupaten(models.Model):
    """Model for Link-Kabupaten Relationships with extra foreign key logic."""
    link = models.ForeignKey(Link, on_delete=models.CASCADE, verbose_name="Link")
    kabupaten = models.ForeignKey(Kabupaten, on_delete=models.CASCADE, verbose_name="Kabupaten")
    province = models.ForeignKey(Province, on_delete=models.CASCADE, verbose_name="Province")
    link_status = models.CharField(max_length=20, choices=Link.STATUS_CHOICES)  # Link status from the Link model
    drp_from = models.IntegerField(null=True, blank=True)
    drp_to = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.link.link_name} - {self.kabupaten.name} from {self.drp_from} to {self.drp_to}"
    


class LinkKacematan(models.Model):
    link = models.ForeignKey(Link, on_delete=models.CASCADE, verbose_name="Link")
    kabupaten = models.ForeignKey(Kabupaten, on_delete=models.CASCADE, verbose_name="Kabupaten")
    province = models.ForeignKey(Province, on_delete=models.CASCADE, verbose_name="Province")
    link_status = models.CharField(max_length=20, choices=Link.STATUS_CHOICES)  # Link status from the Link model
    drp_from = models.IntegerField(null=True, blank=True)
    drp_to = models.IntegerField(null=True, blank=True)
    def __str__(self):
        return f"{self.link.link_name} - {self.kabupaten.name} from {self.drp_from} to {self.drp_to}"
    
class RoadInventory(models.Model):
    link = models.ForeignKey(Link, on_delete=models.CASCADE, verbose_name="Link")
    kabupaten = models.ForeignKey(Kabupaten, on_delete=models.CASCADE, verbose_name="Kabupaten")
    province = models.ForeignKey(Province, on_delete=models.CASCADE, verbose_name="Province")
    link_status = models.CharField(max_length=20, choices=Link.STATUS_CHOICES)
    # Chainage from/to fields
    chainage_from = models.FloatField(verbose_name="Chainage From")
    chainage_to = models.FloatField(verbose_name="Chainage To")

    # Subtype width fields
    row_subtype_width = models.FloatField(verbose_name="Row Subtype Width (m)")
    pavement_subtype_width = models.FloatField(verbose_name="Pavement Subtype Width (m)")

    # Pavement type choices
    PAVEMENT_CHOICES = [
        ('beton', 'Beton'),
        ('blok_beton', 'Blok Beton'),
        ('aspal', 'Aspal'),
        ('lapen', 'Lapen'),
        ('batu_kali', 'Batu Kali'),
        ('keriki', 'Keriki'),
        ('tanah', 'Tanah'),
    ]

    pavement_type = models.CharField(
        max_length=20,
        choices=PAVEMENT_CHOICES,
        default='beton',
        verbose_name="Pavement Type"
    )

    # Shoulder - L and Shoulder - R fields
    shoulder_L_subtype_width = models.FloatField(
        verbose_name="Shoulder-L Subtype Width (m)"
    )
    shoulder_L_type = models.CharField(
        max_length=20,
        choices=PAVEMENT_CHOICES,
        default='beton',
        verbose_name="Shoulder-L Type"
    )

    shoulder_R_subtype_width = models.FloatField(
        verbose_name="Shoulder-R Subtype Width (m)"
    )
    shoulder_R_type = models.CharField(
        max_length=20,
        choices=PAVEMENT_CHOICES,
        default='beton',
        verbose_name="Shoulder-R Type"
    )

    # Drain types with multiple options
    DRAIN_CHOICES = [
        ('tak_ada', 'Tak Ada'),
        ('tak_perlu', 'Tak Perlu'),
        ('tanha', 'Tanha'),
        ('pasangan_batu_terbuka', 'Pasangan Batu Terbuka'),
        ('pasangan_batu_tertutup', 'Pasangan Batu Tertutup'),
    ]

    drain_type_left = models.CharField(
        max_length=30,
        choices=DRAIN_CHOICES,
        default='tak_ada',
        verbose_name="Drain Type Left"
    )
    drain_type_right = models.CharField(
        max_length=30,
        choices=DRAIN_CHOICES,
        default='tak_ada',
        verbose_name="Drain Type Right"
    )

    # Land use types with options
    LAND_USE_CHOICES = [
        ('tak_ada', 'Tak Ada'),
        ('agrikultur', 'Agrikultur'),
        ('desa', 'Desa'),
        ('kota', 'Kota'),
        ('hutan', 'Hutan'),
    ]

    land_use_left = models.CharField(
        max_length=30,
        choices=LAND_USE_CHOICES,
        default='tak_ada',
        verbose_name="Land Use Left"
    )
    land_use_right = models.CharField(
        max_length=30,
        choices=LAND_USE_CHOICES,
        default='tak_ada',
        verbose_name="Land Use Right"
    )

    # Terrain type field
    TERRAIN_CHOICES = [
        ('datar', 'Datar'),
        ('bukit', 'Bukit'),
        ('gunung', 'Gunung'),
    ]

    terrain = models.CharField(
        max_length=20,
        choices=TERRAIN_CHOICES,
        default='datar',
        verbose_name="Terrain Type"
    )

    # Impassable field with a reason
    IMPASSABLE_CHOICES = [
        ('jembatan_runtuh', 'Jembatan Runtuh'),
        ('dungsitapna_jembatan', 'Dungsitapna Jembatan'),
        ('tak_dapat_dilalui_selama_musim', 'Tak Dapat Dilalui Selama Musim'),
        ('lainnya', 'Lainnya'),
    ]

    impassable = models.BooleanField(default=False, verbose_name="Impassable")
    impassable_reason = models.CharField(
        max_length=50,
        choices=IMPASSABLE_CHOICES,
        default='lainnya',
        verbose_name="Impassable Reason"
    )

    def __str__(self):
        return f"{self.link.link_name} - {self.kabupaten.name} from {self.chainage_from} to {self.chainage_to}"
    


class ConditionYear(models.Model):
    """
    Model to represent the year of manual data entry for road condition surveys.
    """
    year = models.PositiveIntegerField(verbose_name="Survey Year")
   

    def __str__(self):
        return f"Condition Year: {self.year}"


class RoadCondition(models.Model):
    """
    Model to represent road conditions associated with links, kabupaten, and province
    with reference to a condition year.
    """
    # Foreign keys
    link = models.ForeignKey('Link', on_delete=models.CASCADE, verbose_name="Link")
    kabupaten = models.ForeignKey('Kabupaten', on_delete=models.CASCADE, verbose_name="Kabupaten")
    province = models.ForeignKey('Province', on_delete=models.CASCADE, verbose_name="Province")
    link_status = models.CharField(
        max_length=20,
        choices=[('provincial', 'Provincial'), ('kabupataen', 'Kabupataen')],  # Replace this with Link.STATUS_CHOICES if Link is defined
        verbose_name="Link Status"
    )
    # Reference to the ConditionYear model
    condition_year = models.ForeignKey(ConditionYear, on_delete=models.CASCADE, verbose_name="Condition Year")
    
    # Additional fields
    survey_year = models.PositiveIntegerField(verbose_name="Survey Year")
    manual_data_entry = models.TextField(
        blank=True, 
        null=True, 
        verbose_name="Manual Data Entry Survey"
    )
    def __str__(self):
        return f"{self.link.link_name} - {self.kabupaten.name} ({self.link_status}) Survey: {self.survey_year}"
    




class MCAcriteria(models.Model):
    # Foreign keys
    link = models.ForeignKey('Link', on_delete=models.CASCADE, verbose_name="Link")
    kabupaten = models.ForeignKey('Kabupaten', on_delete=models.CASCADE, verbose_name="Kabupaten")
    province = models.ForeignKey('Province', on_delete=models.CASCADE, verbose_name="Province")
    
    link_status = models.CharField(
        max_length=20,
        choices=[('provincial', 'Provincial'), ('kabupataen', 'Kabupataen')],
        verbose_name="Link Status"
    )

    link_number = models.IntegerField(
        unique=True, 
        verbose_name="Link Number", 
        null=True,
        blank=True
    )
    # MCA fields with choices
    MCA_1 = models.CharField(max_length=100, choices=[("low", "Low"), ("medium", "Medium"), ("high", "High")])
    MCA_2 = models.CharField(max_length=100, choices=[("low", "Low"), ("medium", "Medium"), ("high", "High")])
    MCA_3 = models.CharField(max_length=100, choices=[("low", "Low"), ("medium", "Medium"), ("high", "High")])
    MCA_4 = models.CharField(max_length=100, choices=[("low", "Low"), ("medium", "Medium"), ("high", "High")])
    
    def save(self, *args, **kwargs):
        """
        Inherit the link_number from the related Link instance when saving.
        """
        if self.link:
            self.link_number = self.link.link_number  # Set the inherited link number
        super().save(*args, **kwargs)

    def __str__(self):
        return f"MCA Criteria for Link: {self.link.link_number}, Status: {self.link_status}"
    

# Culvert Section API  for pkrms 

class CulvertInventory(models.Model):
    link = models.ForeignKey('Link', on_delete=models.CASCADE, verbose_name="Link")
    kabupaten = models.ForeignKey('Kabupaten', on_delete=models.CASCADE, verbose_name="Kabupaten")
    province = models.ForeignKey('Province', on_delete=models.CASCADE, verbose_name="Province")
    
    link_status = models.CharField(
        max_length=20,
        choices=[('provincial', 'Provincial'), ('kabupataen', 'Kabupataen')],
        verbose_name="Link Status"
    )

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

    # Link Status Choices
    LINK_STATUS_CHOICES = [
        ('provincial', 'Provincial'),
        ('kabupaten', 'Kabupaten'),
    ]
    link_status = models.CharField(
        max_length=20,
        choices=LINK_STATUS_CHOICES,
        verbose_name="Link Status",
        help_text="The status of the link (e.g., Provincial or Kabupaten)"
    )

    # Reference to the ConditionYear model
    condition_year = models.ForeignKey('ConditionYear', on_delete=models.CASCADE, verbose_name="Condition Year")
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

    # Link Status Choices
    LINK_STATUS_CHOICES = [
        ('provincial', 'Provincial'),
        ('kabupaten', 'Kabupaten'),
    ]
    link_status = models.CharField(
        max_length=20,
        choices=LINK_STATUS_CHOICES,
        verbose_name="Link Status",
        default=True,
    )
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
    condition_year = models.ForeignKey('ConditionYear', on_delete=models.CASCADE, verbose_name="Condition Year")
    wall_number = models.ForeignKey('Retaining_walls', on_delete=models.CASCADE, verbose_name="wall Number")
    # Link Status Choices
    LINK_STATUS_CHOICES = [
        ('provincial', 'Provincial'),
        ('kabupaten', 'Kabupaten'),
    ]
    link_status = models.CharField(
        max_length=20,
        choices=LINK_STATUS_CHOICES,
        verbose_name="Link Status",
        default=True,
    )

    wall_Mortar_needed = models.IntegerField(null=True, blank=True)
    wall_repair_needed = models.IntegerField(null=True, blank=True)
    wall_rebuiled_needed = models.IntegerField(null=True, blank=True)
    surveyed_by = models.CharField(max_length=200, null=True, blank=True)


# Create API model for traffic volume 


class Traffic_volume(models.Model):
    link = models.ForeignKey('Link', on_delete=models.CASCADE, verbose_name="Link", default=True)
    kabupaten = models.ForeignKey('Kabupaten', on_delete=models.CASCADE, verbose_name="Kabupaten", default=True)
    province = models.ForeignKey('Province', on_delete=models.CASCADE, verbose_name="Province", default=True)
    LINK_STATUS_CHOICES = [
        ('provincial', 'Provincial'),
        ('kabupaten', 'Kabupaten'),
    ]
    link_status = models.CharField(
        max_length=20,
        choices=LINK_STATUS_CHOICES,
        verbose_name="Link Status",
        default=True,
    )
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

class Periodic_UnitCost(models.Model):
 
    kabupaten = models.ForeignKey('Kabupaten', on_delete=models.CASCADE, verbose_name="Kabupaten", default=True)
    province = models.ForeignKey('Province', on_delete=models.CASCADE, verbose_name="Province", default=True)
    LINK_STATUS_CHOICES = [
        ('provincial', 'Provincial'),
        ('kabupaten', 'Kabupaten'),
    ]
    link_status = models.CharField(
        max_length=20,
        choices=LINK_STATUS_CHOICES,
        verbose_name="Link Status",
        default=True,
    )

    overlay_thickness = models.IntegerField()
    periodic_maintenance_unit_cost = models.FloatField()


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
