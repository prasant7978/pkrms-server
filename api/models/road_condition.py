from django.db import models
from api.models.Link import Link
from api.models.SysCode.drainCondition import DrainCondition
from api.models.SysCode.footpathCondition import FootPathCondition
from api.models.SysCode.slopeCondition import SlopeCondition
from api.models.SysCode.shoulderCondition import ShoulderCondition


class RoadCondition(models.Model):
    roadConditionId = models.CharField(primary_key=True, max_length=100, null=False)
    analysisBaseYear = models.BooleanField(default=False, null=True)
    barrierL = models.IntegerField(null=True, blank=True)
    barrierR = models.IntegerField(null=True, blank=True)
    bleedingArea = models.FloatField(null=True, blank=True)
    chainageFrom = models.IntegerField(null=False, blank=False)
    chainageTo = models.IntegerField(null=False, blank=False)
    checkData = models.BooleanField(default=False)  # Added default value
    composition = models.FloatField(null=True, blank=True)
    concreteBlowoutsArea = models.FloatField(null=True, blank=True)
    concreteCornerBreakNo = models.IntegerField(null=True, blank=True)
    concreteCrackingArea = models.CharField(max_length=50, null=True, blank=True)
    concretePumpingNo = models.IntegerField(null=True, blank=True)
    concreteSpallingArea = models.CharField(max_length=50, null=True, blank=True)
    concreteStructuralCrackingArea = models.CharField(max_length=50, null=True, blank=True)
    crackDepArea = models.FloatField(null=True, blank=True)
    crackType = models.FloatField(null=True, blank=True)
    crackWidth = models.IntegerField(null=True, blank=True)
    crossfallArea = models.FloatField(null=True, blank=True)
    crossfallShape = models.CharField(max_length=50, null=True, blank=True)
    desintegrationArea = models.FloatField(null=True, blank=True)
    distribution = models.CharField(max_length=50, null=True, blank=True)
    drpFrom = models.CharField(max_length=50, null=True, blank=True)
    drpTo = models.CharField(max_length=50, null=True, blank=True)
    
    edgeDamageArea = models.FloatField(null=True, blank=True)  # Floating-point field for areas
    depressionsArea = models.FloatField(null=True, blank=True)  # Floating-point field for areas
    erosionArea = models.FloatField(null=True, blank=True)  # Floating-point field for areas
    
    shoulderCondL = models.CharField(max_length=50, null=True, blank=True)
    shoulderCondR = models.CharField(max_length=50, null=True, blank=True)

    edgeDamageAreaR = models.FloatField(null=True, blank=True)  # Floating-point field for areas

    
    # Fixed ForeignKey fields with related_name
    drainL = models.ForeignKey('DrainCondition', on_delete=models.CASCADE, null=True, blank=True, related_name='road_condition_left',db_column='drainL')
    drainR = models.ForeignKey('DrainCondition', on_delete=models.CASCADE, null=True, blank=True, related_name='road_condition_right',db_column='drainR')
    footpathL = models.ForeignKey('FootPathCondition', on_delete=models.CASCADE, related_name='road_condition_footpath_left',db_column='footpathL')
    footpathR = models.ForeignKey('FootPathCondition', on_delete=models.CASCADE, related_name='road_condition_footpath_right',db_column='footpathR')
    shoulderL = models.ForeignKey('ShoulderCondition', on_delete=models.CASCADE, related_name='road_condition_shoulder_left',db_column='shoulderL')
    shoulderR = models.ForeignKey('ShoulderCondition', on_delete=models.CASCADE, related_name='road_condition_shoulder_right',db_column='shoulderR')
    slopeL = models.ForeignKey('SlopeCondition', on_delete=models.CASCADE, related_name='road_condition_slope_left',db_column='slopeL')
    slopeR = models.ForeignKey('SlopeCondition', on_delete=models.CASCADE, related_name='road_condition_slope_right',db_column='slopeR')

    gravelSize = models.CharField(max_length=50, null=True, blank=True)
    gravelThickness = models.CharField(max_length=50, null=True, blank=True)
    gravelThicknessArea = models.FloatField(null=True, blank=True)  # Fixed missing parentheses
    
    guidepostL = models.IntegerField(null=True, blank=True)
    guidepostR = models.IntegerField(null=True, blank=True)
    iri = models.CharField(max_length=50, null=True, blank=True)
    offsetFrom = models.IntegerField(null=True, blank=True)
    offsetTo = models.IntegerField(null=True, blank=True)
    othCrackArea = models.FloatField(null=True, blank=True)
    paved = models.BooleanField(null=True, blank=True)
    pavement = models.CharField(max_length=100, null=True, blank=True)
    patchingArea = models.FloatField(null=True, blank=True)
    potholeArea = models.FloatField(null=True, blank=True)
    potholeCount = models.IntegerField(null=True, blank=True)
    potholeSize = models.FloatField(null=True, blank=True)
    rci = models.CharField(max_length=50, null=True, blank=True)
    ravellingArea = models.FloatField(null=True, blank=True)
    roadMarkingL = models.IntegerField(null=True, blank=True, default=False)
    roadMarkingR = models.IntegerField(null=True, blank=True, default=False)
    roughness = models.BooleanField(null=True, blank=True, default=False)
    ruttingArea = models.FloatField(null=True, blank=True)
    ruttingDepth = models.IntegerField(null=True, blank=True)
    sectionStatus = models.FloatField(null=True, blank=True)
    segmentTti = models.CharField(max_length=50, null=True, blank=True)
    
    signL = models.IntegerField(null=True, blank=True)
    signR = models.IntegerField(null=True, blank=True)
    surveyBy = models.CharField(max_length=50, null=True, blank=True)
    surveyBy2 = models.CharField(max_length=50, null=True, blank=True)
    surveyDate = models.DateTimeField()
    wavinessArea = models.FloatField(null=True, blank=True)
    year = models.IntegerField(null=False, blank=False)

    linkId = models.ForeignKey('Link', on_delete=models.CASCADE, related_name='road_conditions',db_column='linkId')

    class Meta:
        db_table = 'RoadCondition'