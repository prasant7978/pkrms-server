from django.db import models
from api.models.Link import Link
from api.models.SysCode.drainCondition import DrainCondition
from api.models.SysCode.footpathCondition import FootPathCondition
from api.models.SysCode.slopeCondition import SlopeCondition
from api.models.SysCode.shoulderCondition import ShoulderCondition


class RoadCondition(models.Model):
    roadConditionId = models.CharField(primary_key=True, max_length=100, null=False)
    analysisBaseYear = models.CharField(null=True, blank=True)
    barrierL = models.CharField(null=True, blank=True)
    barrierR = models.CharField(null=True, blank=True)
    bleedingArea = models.CharField(null=True, blank=True)
    chainageFrom = models.CharField(null=False, blank=False)
    chainageTo = models.CharField(null=False, blank=False)
    checkData = models.CharField(null=False, blank=False)  # Added default value
    composition = models.CharField(null=True, blank=True)
    concreteBlowoutsArea = models.CharField(null=True, blank=True)
    concreteCornerBreakNo = models.CharField(null=True, blank=True)
    concreteCrackingArea = models.CharField(max_length=50, null=True, blank=True)
    concretePumpingNo = models.CharField(null=True, blank=True)
    concreteSpallingArea = models.CharField(max_length=50, null=True, blank=True)
    concreteStructuralCrackingArea = models.CharField(max_length=50, null=True, blank=True)
    crackDepArea = models.CharField(null=True, blank=True)
    crackType = models.CharField(null=True, blank=True)
    crackWidth = models.CharField(null=True, blank=True)
    crossfallArea = models.CharField(null=True, blank=True)
    crossfallShape = models.CharField(max_length=50, null=True, blank=True)
    desintegrationArea = models.CharField(null=True, blank=True)
    distribution = models.CharField(max_length=50, null=True, blank=True)
    drpFrom = models.CharField(max_length=50, null=True, blank=True)
    drpTo = models.CharField(max_length=50, null=True, blank=True)
    
    edgeDamageArea = models.CharField(null=True, blank=True)  # Floating-point field for areas
    depressionsArea = models.CharField(null=True, blank=True)  # Floating-point field for areas
    erosionArea = models.CharField(null=True, blank=True)  # Floating-point field for areas
    
    shoulderCondL = models.CharField(max_length=50, null=True, blank=True)
    shoulderCondR = models.CharField(max_length=50, null=True, blank=True)

    edgeDamageAreaR = models.CharField(null=True, blank=True)  # Floating-point field for areas

    
    # Fixed ForeignKey fields with related_name
    drainL = models.CharField(null=False, blank=False)
    drainR = models.CharField(null=False, blank=False)
    footpathL = models.CharField(null=False, blank=False)
    footpathR = models.CharField(null=False, blank=False)
    shoulderL = models.CharField(null=False, blank=False)
    shoulderR = models.CharField(null=False, blank=False)
    slopeL = models.CharField(null=False, blank=False)
    slopeR = models.CharField(null=False, blank=False)

    gravelSize = models.CharField(max_length=50, null=True, blank=True)
    gravelThickness = models.CharField(max_length=50, null=True, blank=True)
    gravelThicknessArea = models.CharField(null=True, blank=True)  # Fixed missing parentheses
    
    guidepostL = models.CharField(null=True, blank=True)
    guidepostR = models.CharField(null=True, blank=True)
    iri = models.CharField(max_length=50, null=True, blank=True)
    offsetFrom = models.CharField(null=True, blank=True)
    offsetTo = models.CharField(null=True, blank=True)
    othCrackArea = models.CharField(null=True, blank=True)
    paved = models.CharField(null=False, blank=False)
    pavement = models.CharField(max_length=100, null=True, blank=True)
    patchingArea = models.CharField(null=True, blank=True)
    potholeArea = models.CharField(null=True, blank=True)
    potholeCount = models.CharField(null=True, blank=True)
    potholeSize = models.CharField(null=True, blank=True)
    rci = models.CharField(max_length=50, null=True, blank=True)
    ravellingArea = models.CharField(null=True, blank=True)
    roadMarkingL = models.CharField(null=True, blank=True, default=False)
    roadMarkingR = models.CharField(null=True, blank=True, default=False)
    roughness = models.CharField(null=False, blank=False)
    ruttingArea = models.CharField(null=True, blank=True)
    ruttingDepth = models.CharField(null=True, blank=True)
    sectionStatus = models.CharField(null=True, blank=True)
    segmentTti = models.CharField(max_length=50, null=True, blank=True)
    
    signL = models.CharField(null=True, blank=True)
    signR = models.CharField(null=True, blank=True)
    surveyBy = models.CharField(max_length=50, null=True, blank=True)
    surveyBy2 = models.CharField(max_length=50, null=True, blank=True)
    surveyDate = models.CharField(null=False, blank=False)
    wavinessArea = models.CharField(null=True, blank=True)
    year = models.CharField(null=False, blank=False)

    linkId = models.ForeignKey('Link', on_delete=models.CASCADE, related_name='road_conditions',db_column='linkId')

    class Meta:
        db_table = 'roadcondition'