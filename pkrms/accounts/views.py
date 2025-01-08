from django.shortcuts import render

from django.http import JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import json
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from .models import Traffic_weighting_factors, Periodic_UnitCost
from .models import ApprovalRequest, Traffic_volume,Traffic_weighting_factors,Link,Retaining_walls,Retaining_walls_Condition,CulvertCondition,CulvertInventory,MCAcriteria,ConditionYear,RoadCondition, DRP,RoadInventory, Province, Kabupaten , LinkClass, CorridorLink, PriorityArea,LinkKabupaten, LinkKacematan, CorridorName
from rest_framework import serializers
from .serializers import MCAcriteriaSerializer, RoadInventorySerializer, LinkSerializer, DRPSerializer , LinkClassSerializer, LinkKabupatenSerializer, LinkKacematanSerializer
from rest_framework.response import Response
from rest_framework import status 
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.generics import GenericAPIView
from django.shortcuts import render, redirect
from .serializers import ConditionYearSerializer, RoadConditionSerializer
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render, redirect
from django.http import HttpResponse
# views.py

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import UserRegistrationSerializer, OTPVerificationSerializer
from django.core.cache import cache
from django.core.mail import send_mail
from django.conf import settings
from .models import User, Role, Balai, Province, Kabupaten
import random

from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login as auth_login
from django.shortcuts import render, redirect
from django.http import HttpResponse

from django.contrib.auth.hashers import check_password

from rest_framework import viewsets
from .models import Balai, Province, Kabupaten
from .serializers import BalaiSerializer, ProvinceSerializer, KabupatenSerializer
# registration modules 
from django.contrib.auth import authenticate
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import LoginSerializer
class BalaiViewSet(viewsets.ModelViewSet):
    queryset = Balai.objects.all()
    serializer_class = BalaiSerializer

class ProvinceViewSet(viewsets.ModelViewSet):
    queryset = Province.objects.all()
    serializer_class = ProvinceSerializer

class KabupatenViewSet(viewsets.ModelViewSet):
    queryset = Kabupaten.objects.all()
    serializer_class = KabupatenSerializer


# api view in order to get update and maintain data 
class LinksByProvinceKabupatenView(APIView):
    def get(self, request, province_code, kabupaten_code):
        try:
            # Get province and kabupaten based on codes
            province = Province.objects.get(code=province_code)
            kabupaten = Kabupaten.objects.get(code=kabupaten_code, province=province)

            # Fetch all links for this province and kabupaten
            links = Link.objects.filter(province=province, kabupaten=kabupaten)

            # Serialize data
            serializer = LinkSerializer(links, many=True)
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)

        except Province.DoesNotExist:
            return Response({"status": "error", "message": "Province not found"}, status=status.HTTP_404_NOT_FOUND)
        except Kabupaten.DoesNotExist:
            return Response({"status": "error", "message": "Kabupaten not found"}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request, province_code, kabupaten_code):
        try:
            province = Province.objects.get(code=province_code)
            kabupaten = Kabupaten.objects.get(code=kabupaten_code, province=province)

            # Validate and create new link
            serializer = LinkSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(province=province, kabupaten=kabupaten)
                return Response({"status": "success", "message": "Link created successfully", "data": serializer.data},
                                status=status.HTTP_201_CREATED)
            return Response({"status": "error", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        except Province.DoesNotExist:
            return Response({"status": "error", "message": "Province not found"}, status=status.HTTP_404_NOT_FOUND)
        except Kabupaten.DoesNotExist:
            return Response({"status": "error", "message": "Kabupaten not found"}, status=status.HTTP_404_NOT_FOUND)

    def patch(self, request, province_code, kabupaten_code):
        try:
            province = Province.objects.get(code=province_code)
            kabupaten = Kabupaten.objects.get(code=kabupaten_code, province=province)
            data = request.data

            # Find and update link
            link = Link.objects.get(id=data["id"], province=province, kabupaten=kabupaten)
            serializer = LinkSerializer(link, data=data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({"status": "success", "message": "Link updated successfully", "data": serializer.data},
                                status=status.HTTP_200_OK)
            return Response({"status": "error", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        except Province.DoesNotExist:
            return Response({"status": "error", "message": "Province not found"}, status=status.HTTP_404_NOT_FOUND)
        except Kabupaten.DoesNotExist:
            return Response({"status": "error", "message": "Kabupaten not found"}, status=status.HTTP_404_NOT_FOUND)
        except Link.DoesNotExist:
            return Response({"status": "error", "message": "Link not found"}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, province_code, kabupaten_code):
        try:
            province = Province.objects.get(code=province_code)
            kabupaten = Kabupaten.objects.get(code=kabupaten_code, province=province)
            data = request.data

            # Delete link
            link = Link.objects.get(id=data["id"], province=province, kabupaten=kabupaten)
            link.delete()
            return Response({"status": "success", "message": "Link deleted successfully"}, status=status.HTTP_200_OK)

        except Province.DoesNotExist:
            return Response({"status": "error", "message": "Province not found"}, status=status.HTTP_404_NOT_FOUND)
        except Kabupaten.DoesNotExist:
            return Response({"status": "error", "message": "Kabupaten not found"}, status=status.HTTP_404_NOT_FOUND)
        except Link.DoesNotExist:
            return Response({"status": "error", "message": "Link not found"}, status=status.HTTP_404_NOT_FOUND)
# APIVIEW in order to get (DRP) data we can aslo put and patch data as per our requirement 



@method_decorator(csrf_exempt, name="dispatch")
class DRPByProvinceKabupatenLinkAPIView(APIView):
    def get(self, request, province_code, kabupaten_code, link_id):
        """Retrieve all DRPs for a specific province, kabupaten, and link."""
        try:
            province = Province.objects.get(code=province_code)
            kabupaten = Kabupaten.objects.get(code=kabupaten_code, province=province)
            link = Link.objects.get(id=link_id, province=province, kabupaten=kabupaten)
            drps = DRP.objects.filter(link=link)

            serializer = DRPSerializer(drps, many=True)
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        except Province.DoesNotExist:
            return Response({"status": "error", "message": "Province not found"}, status=status.HTTP_404_NOT_FOUND)
        except Kabupaten.DoesNotExist:
            return Response({"status": "error", "message": "Kabupaten not found"}, status=status.HTTP_404_NOT_FOUND)
        except Link.DoesNotExist:
            return Response({"status": "error", "message": "Link not found"}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request, province_code, kabupaten_code, link_id):
        """Create a new DRP for a specific link."""
        try:
            province = Province.objects.get(code=province_code)
            kabupaten = Kabupaten.objects.get(code=kabupaten_code, province=province)
            link = Link.objects.get(id=link_id, province=province, kabupaten=kabupaten)

            data = request.data
            data["link"] = link.id  # Associate the DRP with the correct link

            serializer = DRPSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response({"status": "success", "message": "DRP created successfully", "data": serializer.data}, status=status.HTTP_201_CREATED)

            return Response({"status": "error", "message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Province.DoesNotExist:
            return Response({"status": "error", "message": "Province not found"}, status=status.HTTP_404_NOT_FOUND)
        except Kabupaten.DoesNotExist:
            return Response({"status": "error", "message": "Kabupaten not found"}, status=status.HTTP_404_NOT_FOUND)
        except Link.DoesNotExist:
            return Response({"status": "error", "message": "Link not found"}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, province_code, kabupaten_code, link_id):
        """Update an existing DRP record entirely."""
        try:
            province = Province.objects.get(code=province_code)
            kabupaten = Kabupaten.objects.get(code=kabupaten_code, province=province)
            link = Link.objects.get(id=link_id, province=province, kabupaten=kabupaten)

            data = request.data
            drp = DRP.objects.get(id=data["id"], link=link)

            serializer = DRPSerializer(drp, data=data)
            if serializer.is_valid():
                serializer.save()
                return Response({"status": "success", "message": "DRP updated successfully", "data": serializer.data}, status=status.HTTP_200_OK)

            return Response({"status": "error", "message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Province.DoesNotExist:
            return Response({"status": "error", "message": "Province not found"}, status=status.HTTP_404_NOT_FOUND)
        except Kabupaten.DoesNotExist:
            return Response({"status": "error", "message": "Kabupaten not found"}, status=status.HTTP_404_NOT_FOUND)
        except Link.DoesNotExist:
            return Response({"status": "error", "message": "Link not found"}, status=status.HTTP_404_NOT_FOUND)
        except DRP.DoesNotExist:
            return Response({"status": "error", "message": "DRP not found"}, status=status.HTTP_404_NOT_FOUND)

    def patch(self, request, province_code, kabupaten_code, link_id):
        """Partially update an existing DRP record."""
        try:
            province = Province.objects.get(code=province_code)
            kabupaten = Kabupaten.objects.get(code=kabupaten_code, province=province)
            link = Link.objects.get(id=link_id, province=province, kabupaten=kabupaten)

            data = request.data
            drp = DRP.objects.get(id=data["id"], link=link)

            serializer = DRPSerializer(drp, data=data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({"status": "success", "message": "DRP partially updated successfully", "data": serializer.data}, status=status.HTTP_200_OK)

            return Response({"status": "error", "message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Province.DoesNotExist:
            return Response({"status": "error", "message": "Province not found"}, status=status.HTTP_404_NOT_FOUND)
        except Kabupaten.DoesNotExist:
            return Response({"status": "error", "message": "Kabupaten not found"}, status=status.HTTP_404_NOT_FOUND)
        except Link.DoesNotExist:
            return Response({"status": "error", "message": "Link not found"}, status=status.HTTP_404_NOT_FOUND)
        except DRP.DoesNotExist:
            return Response({"status": "error", "message": "DRP not found"}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, province_code, kabupaten_code, link_id):
        """Delete a specific DRP record."""
        try:
            province = Province.objects.get(code=province_code)
            kabupaten = Kabupaten.objects.get(code=kabupaten_code, province=province)
            link = Link.objects.get(id=link_id, province=province, kabupaten=kabupaten)

            drp_id = request.data.get("id")
            drp = DRP.objects.get(id=drp_id, link=link)
            drp.delete()

            return Response({"status": "success", "message": "DRP deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except Province.DoesNotExist:
            return Response({"status": "error", "message": "Province not found"}, status=status.HTTP_404_NOT_FOUND)
        except Kabupaten.DoesNotExist:
            return Response({"status": "error", "message": "Kabupaten not found"}, status=status.HTTP_404_NOT_FOUND)
        except Link.DoesNotExist:
            return Response({"status": "error", "message": "Link not found"}, status=status.HTTP_404_NOT_FOUND)
        except DRP.DoesNotExist:
            return Response({"status": "error", "message": "DRP not found"}, status=status.HTTP_404_NOT_FOUND)
        
# view to retrive link class data in order to get data for linkclass and length in kilometers 
class LinkClassListView(generics.GenericAPIView):
    """
    Handle CRUD operations for LinkClass objects filtered by province and kabupaten.
    """
    serializer_class = LinkClassSerializer

    def get_queryset(self):
        # Fetch province_id and kabupaten_id from kwargs
        province_id = self.kwargs.get('province_id')
        kabupaten_id = self.kwargs.get('kabupaten_id')

        # Debugging the IDs
        print(f"Filtering with province_id: {province_id}, kabupaten_id: {kabupaten_id}")

        # Query the database
        queryset = LinkClass.objects.filter(province_id=province_id, kabupaten_id=kabupaten_id)
        
        # Debugging: Print out the queryset to ensure data exists
        print(f"Queryset result: {queryset.values('id', 'total_length', 'unit', 'link_class')}")
        
        return queryset

    def get(self, request, *args, **kwargs):
        """
        Retrieve a list of LinkClass objects.
        """
        try:
            queryset = self.get_queryset()

            # Debugging: Ensure queryset is non-empty
            if not queryset.exists():
                print("No matching LinkClass objects found in database for given filters.")
            
            serializer = self.get_serializer(queryset, many=True)

            # Debugging: Log serializer data
            print(f"Serialized data: {serializer.data}")

            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        except Exception as e:
            print(f"Error during GET: {e}")  # Log exception
            return Response({"status": "error", "message": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, *args, **kwargs):
        """
        Create a new LinkClass object.
        """
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_201_CREATED)
        except Exception as e:
            print(f"Error during POST: {e}")
            return Response({"status": "error", "message": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, *args, **kwargs):
        """
        Update an existing LinkClass object.
        """
        try:
            instance = self.get_queryset().get(id=request.data.get('id'))
            serializer = self.get_serializer(instance, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        except LinkClass.DoesNotExist:
            print("Instance does not exist for patch operation.")
            return Response({"status": "error", "message": "Object not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print(f"Error during PATCH: {e}")
            return Response({"status": "error", "message": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        """
        Delete a LinkClass object.
        """
        try:
            instance = self.get_queryset().get(id=request.data.get('id'))
            instance.delete()
            print("Object deleted successfully.")
            return Response({"status": "success", "message": "Object deleted"}, status=status.HTTP_200_OK)
        except LinkClass.DoesNotExist:
            print("Instance does not exist for delete operation.")
            return Response({"status": "error", "message": "Object not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print(f"Error during DELETE: {e}")
            return Response({"status": "error", "message": str(e)}, status=status.HTTP_400_BAD_REQUEST)







def link_selection_view(request):
    """
    Handles rendering all links, showing the corridor links, and saving selected links.
    """
    if request.method == "POST":
        # Handle form submission
        selected_links = request.POST.getlist('selected_links')
        
        # Save selected links into CorridorLink model
        for link_id in selected_links:
            link_instance = Link.objects.get(id=link_id)
            CorridorLink.objects.get_or_create(link=link_instance)

        # Redirect back to the same page after submission
        return redirect("link_selection")

    # Fetch all links from the database
    all_links = Link.objects.all()

    # Fetch selected/corridor links
    corridor_links = CorridorLink.objects.all()

    context = {
        'all_links': all_links,
        'corridor_links': corridor_links,
    }

    return render(request, 'link_selection.html', context)






def link_selection_view(request):
    """
    Handles rendering the selection forms and processing submissions.
    """
    # Handle if this is the POST for saving links
    if request.method == "POST":
        # Save the selected links
        selected_links = request.POST.getlist('selected_links')
        for link_id in selected_links:
            link_instance = Link.objects.get(id=link_id)
            CorridorLink.objects.get_or_create(link=link_instance)
        return redirect("link_selection")

    # Handle form rendering
    # Fetch priority areas and corridors for dropdown options
    priority_areas = PriorityArea.objects.all()
    corridor_names = CorridorName.objects.all()

    # Handle filtering logic if form submission is made with selected priority/corridor
    selected_priority_id = request.GET.get("priority_area")
    selected_corridor_id = request.GET.get("corridor_name")
    
    if selected_priority_id and selected_corridor_id:
        # Filter only links based on the selection
        links = Link.objects.filter(
            priority_area_id=selected_priority_id,
            corridor_name_id=selected_corridor_id,
        )
    else:
        # Render all links by default
        links = Link.objects.none()

    # Fetch already saved Corridor Links
    corridor_links = CorridorLink.objects.all()

    context = {
        "priority_areas": priority_areas,
        "corridor_names": corridor_names,
        "links": links,
        "corridor_links": corridor_links,
    }

    return render(request, 'link_selection.html', context)

# LinkKabupaten Views
class LinkKabupatenListCreateView(generics.ListCreateAPIView):
    """
    GET: List all LinkKabupaten entries.
    POST: Create a new LinkKabupaten entry.
    """
    queryset = LinkKabupaten.objects.all()
    serializer_class = LinkKabupatenSerializer


class LinkKabupatenDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET: Retrieve a specific LinkKabupaten entry by ID.
    PUT: Update a specific LinkKabupaten entry by ID.
    PATCH: Partially update a specific LinkKabupaten entry by ID.
    DELETE: Delete a specific LinkKabupaten entry by ID.
    """
    queryset = LinkKabupaten.objects.all()
    serializer_class = LinkKabupatenSerializer


# LinkKacematan Views
class LinkKacematanListCreateView(generics.ListCreateAPIView):
    """
    GET: List all LinkKacematan entries.
    POST: Create a new LinkKacematan entry.
    """
    queryset = LinkKacematan.objects.all()
    serializer_class = LinkKacematanSerializer


class LinkKacematanDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET: Retrieve a specific LinkKacematan entry by ID.
    PUT: Update a specific LinkKacematan entry by ID.
    PATCH: Partially update a specific LinkKacematan entry by ID.
    DELETE: Delete a specific LinkKacematan entry by ID.
    """
    queryset = LinkKacematan.objects.all()
    serializer_class = LinkKacematanSerializer
# API logic for Road Inventory section by the use of generics views

class RoadInventoryListCreateView(generics.ListCreateAPIView):
    queryset = RoadInventory.objects.all()
    serializer_class = RoadInventorySerializer
class RoadInventoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = RoadInventory.objects.all()
    serializer_class = RoadInventorySerializer

from .serializers import ConditionYearSerializer, RoadConditionSerializer

# API section for Road condition .
# CRUD for ConditionYear
class ConditionYearListCreateView(generics.ListCreateAPIView):
    queryset = ConditionYear.objects.all()
    serializer_class = ConditionYearSerializer


class ConditionYearRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ConditionYear.objects.all()
    serializer_class = ConditionYearSerializer


# CRUD for RoadCondition
class RoadConditionListCreateView(generics.ListCreateAPIView):
    queryset = RoadCondition.objects.all()
    serializer_class = RoadConditionSerializer


class RoadConditionRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = RoadCondition.objects.all()
    serializer_class = RoadConditionSerializer

# List and Create View
class MCAcriteriaListCreateView(generics.ListCreateAPIView):
    queryset = MCAcriteria.objects.all()
    serializer_class = MCAcriteriaSerializer

# Retrieve, Update, and Delete View
class MCAcriteriaRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = MCAcriteria.objects.all()
    serializer_class = MCAcriteriaSerializer



# Culvert inventory logic to save data 




def culvert_inventory_view(request):
    if request.method == 'POST':
        # Get data from the POST request
        link_id = request.POST.get('link')
        kabupaten_id = request.POST.get('kabupaten')
        province_id = request.POST.get('province')
        link_status = request.POST.get('link_status')
        chainage = request.POST.get('chainage')
        culvert_number = request.POST.get('culvert_number')
        culvert_length = request.POST.get('culvert_length')
        number_of_openings = request.POST.get('number_of_openings')
        culvert_type = request.POST.get('culvert_type')
        culvert_width = request.POST.get('culvert_width')
        culvert_height = request.POST.get('culvert_height')
        inlet_type = request.POST.get('inlet_type')
        outlet_type = request.POST.get('outlet_type')

        # Save the data to the database
        CulvertInventory.objects.create(
            link_id=link_id,
            kabupaten_id=kabupaten_id,
            province_id=province_id,
            link_status=link_status,
            chainage=chainage,
            culvert_number=culvert_number,
            culvert_length=culvert_length,
            number_of_openings=number_of_openings,
            culvert_type=culvert_type,
            culvert_width=culvert_width,
            culvert_height=culvert_height,
            inlet_type=inlet_type,
            outlet_type=outlet_type,
        )

          # Redirect to a success page

    # Fetch required data for dropdowns and list of existing inventories
    links = Link.objects.all()
    kabupatens = Kabupaten.objects.all()
    provinces = Province.objects.all()
    culvert_inventories = CulvertInventory.objects.all()

    return render(request, 'culvert_inventory.html', {
        'links': links,
        'kabupatens': kabupatens,
        'provinces': provinces,
        'culvert_inventories': culvert_inventories,
    })



# Culvert Condition form data 



def culvert_condition_form(request):
    if request.method == 'POST':
        # Create a new CulvertCondition instance
        CulvertCondition.objects.create(
            link_id=request.POST['link'],
            kabupaten_id=request.POST['kabupaten'],
            province_id=request.POST['province'],
            link_status=request.POST['link_status'],
            condition_year_id=request.POST['condition_year'],
            culvert_number_id=request.POST['culvert_number'],
            condition_barrel=request.POST['condition_barrel'],
            condition_inlet=request.POST['condition_inlet'],
            condition_outlet=request.POST['condition_outlet'],
            sitting=request.POST['sitting'],
            overtopping=request.POST['overtopping'] == 'true',
            surveyed_by=request.POST['surveyed_by']
        )
        return redirect('culvert_condition_list')

    # Provide data for dropdowns
    context = {
        'links': Link.objects.all(),
        'kabupatens': Kabupaten.objects.all(),
        'provinces': Province.objects.all(),
        'condition_years': ConditionYear.objects.all(),
        'culverts': CulvertInventory.objects.all(),
        'condition_choices': CulvertCondition.CONDITION_CHOICES,
        'sitting_choices': CulvertCondition.SITTING_CHOICES,
    }
    return render(request, 'culvert_form.html', context)

def culvert_condition_list(request):
    conditions = CulvertCondition.objects.all()
    return render(request, 'culvert_condition.html', {'conditions': conditions})
# Retaining walls logic 


def retaining_walls_view(request):
    retaining_walls = Retaining_walls.objects.all()
    links = Link.objects.all()
    kabupatens = Kabupaten.objects.all()
    provinces = Province.objects.all()  # Fetching all retaining wall entries
    return render(request, 'retaining_walls.html', {
        'retaining_walls': retaining_walls,
        'links': links,
        'kabupatens' : kabupatens, 
        'provinces': provinces,
    })

# View for handling the form submission (saving data)
@csrf_protect  # Using CSRF protection for POST requests
def save_retaining_wall(request):
    if request.method == 'POST':
        try:
            # Extracting form data from POST request
            link = request.POST.get('link')
            kabupaten = request.POST.get('kabupaten')
            province = request.POST.get('province')
            link_status = request.POST.get('link_status')
            wall_side = request.POST.get('wall_side')
            wall_material = request.POST.get('wall_material')
            wall_height = request.POST.get('wall_height')
            chainage_from = request.POST.get('chainage_from')
            wall_number = request.POST.get('wall_number')
            wall_type = request.POST.get('wall_type')
            
            # Saving the data to the database
            new_retaining_wall = Retaining_walls(
                link_id=link,
                kabupaten_id=kabupaten,
                province_id=province,
                link_status=link_status,
                wall_side=wall_side,
                wall_material=wall_material,
                wall_height=wall_height,
                chainage_from=chainage_from,
                wall_number=wall_number,
                wall_type=wall_type
            )
            new_retaining_wall.save()  # Save the instance to the database
            
            # Redirecting to the page where data is displayed
            return redirect('retaining_walls_view')  # Assuming the URL name for the view is 'retaining_walls_view'
        except Exception as e:
            return HttpResponse(f"Error: {e}")
    return HttpResponse("Invalid request method", status=400)




def save_wall_condition(request):
    if request.method == "POST":
        # Get data from the form
        link_id = request.POST.get('link')
        kabupaten_id = request.POST.get('kabupaten')
        province_id = request.POST.get('province')
        condition_year_id = request.POST.get('condition_year')
        wall_number_id = request.POST.get('wall_number')
        link_status = request.POST.get('link_status')
        wall_mortar_needed = request.POST.get('wall_mortar_needed')
        wall_repair_needed = request.POST.get('wall_repair_needed')
        wall_rebuilt_needed = request.POST.get('wall_rebuilt_needed')
        surveyed_by = request.POST.get('surveyed_by')

        # Save data
        Retaining_walls_Condition.objects.create(
            link_id=link_id,
            kabupaten_id=kabupaten_id,
            province_id=province_id,
            condition_year_id=condition_year_id,
            wall_number_id=wall_number_id,
            link_status=link_status,
            wall_Mortar_needed=wall_mortar_needed,
            wall_repair_needed=wall_repair_needed,
            wall_rebuiled_needed=wall_rebuilt_needed,
            surveyed_by=surveyed_by,
        )
        return redirect('display_wall_conditions')

    # Fetch data for dropdowns
    links = Link.objects.all()
    kabupatens = Kabupaten.objects.all()
    provinces = Province.objects.all()
    condition_years = ConditionYear.objects.all()
    walls = Retaining_walls.objects.all()

    return render(request, 'wall_condition.html', {
        'links': links,
        'kabupatens': kabupatens,
        'provinces': provinces,
        'condition_years': condition_years,
        'walls': walls,
    })


def display_wall_conditions(request):
    conditions = Retaining_walls_Condition.objects.all()
    return render(request, 'display_wall_conditions.html', {'conditions': conditions})


'''from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.cache import cache
from django.core.mail import send_mail
from django.conf import settings
from .models import User, Role, Balai, Province, Kabupaten
import random

def registrationview(request):
    balai = Balai.objects.all()
    province = Province.objects.all()
    kabupaten = Kabupaten.objects.all()
    role = Role.objects.all()
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        role_id = request.POST['role']  # Role ID from the form
        balai_id = request.POST.get('balai')  # Balai ID from the form
        province_id = request.POST.get('province')  # Province ID from the form
        kabupaten_id = request.POST.get('kabupaten')  # Kabupaten ID from the form
        
        password = request.POST['password']

        # Check if the username or email already exists in the User model
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
            return redirect('register')
        elif User.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered')
            return redirect('register')
        else:
            # Validate Role, Balai, Province, and Kabupaten before storing the OTP
            try:
                role = Role.objects.get(id=role_id)
                balai = Balai.objects.get(id=balai_id) if balai_id else None
                province = Province.objects.get(id=province_id) if province_id else None
                kabupaten = Kabupaten.objects.get(id=kabupaten_id) if kabupaten_id else None
            except (Role.DoesNotExist, Balai.DoesNotExist, Province.DoesNotExist, Kabupaten.DoesNotExist):
                messages.error(request, 'Invalid role or location data.')
                return redirect('register')

            # Generate OTP and cache it
            otp = random.randint(1000, 9999)
            cache.set(email, otp, timeout=300)  # Cache the OTP for 5 minutes
            send_mail(
                'Your OTP Code',
                f'Your OTP code is {otp}',
                settings.DEFAULT_FROM_EMAIL,
                [email],
                fail_silently=False,
            )

            # Store user data in session
            request.session['user_data'] = {
                'username': username,
                'email': email,
                'role': role.id,  # Storing role ID
                'balai': balai.id if balai else None,
                'province': province.id if province else None,
                'kabupaten': kabupaten.id if kabupaten else None,
                
                'password': password,
            }
            return redirect('verify_otp')
        
    context = {
        'balai': balai,
        'province': province,
        'kabupaten': kabupaten,
        'role': role,
    }
    return render(request, 'register.html', context )


from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.cache import cache
from .models import User, Role, Balai, Province, Kabupaten


    
def verify_otp(request):
    if request.method == 'POST':
        otp = request.POST['otp']
        user_data = request.session.get('user_data')

        if not user_data:
            messages.error(request, 'Session expired. Please register again.')
            return redirect('register')

        cached_otp = cache.get(user_data['email'])
        if str(otp) == str(cached_otp):
            approver = None
            if user_data['role'] == 'province_lg' and user_data.get('balai'):
                approver = User.objects.filter(balai_id=user_data['balai'], role__name='balai_lg').first()
            elif user_data['role'] == 'kabupaten_lg' and user_data.get('province'):
                approver = User.objects.filter(province_id=user_data['province'], role__name='province_lg').first()

            user = User.objects.create_user(
                email=user_data['email'],
                username=user_data['username'],
                password=user_data['password'],
                role_id=user_data['role'],
                balai_id=user_data.get('balai'),
                province_id=user_data.get('province'),
                Kabupaten_id=user_data.get('kabupaten'),
                approved=(user_data['role'] == 'balai_lg'),  # Auto-approve Balai LG users
            )

            if approver:
                ApprovalRequest.objects.create(user=user, approver=approver)

            # Clear session and cache
            cache.delete(user_data['email'])
            del request.session['user_data']

            messages.success(
                request,
                'Registration successful. Awaiting approval.' if approver else 'Account registered successfully.'
            )
            return redirect('login')
        else:
            messages.error(request, 'Invalid OTP. Please try again.')
            return redirect('verify_otp')

    return render(request, 'verify_otp.html')

from django.contrib.auth import authenticate, login as auth_login
from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils.timezone import now

from django.contrib.auth import authenticate, login as auth_login

def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)

        if user is not None:
            if user.is_active and (user.approved or user.is_superuser):
                auth_login(request, user)
                print(f"User {user.email} logged in successfully.")
                print(f"User is_authenticated: {request.user.is_authenticated}")
                print(f"User role: {user.role}")
                if user.role:
                    role_name = user.role.role_name
                    print(f"Role name: {role_name}")

                    # Role-based redirection
                    if role_name == Role.BALAI_LG:
                        return redirect('balai_dashboard')
                    elif role_name == Role.PROVINCIAL_LG:
                        return redirect('province_dashboard')
                    elif role_name == Role.KABUPATEN_LG:
                        return redirect('kabupaten_dashboard')
                    else:
                        messages.error(request, 'Invalid role assigned.')
                        return redirect('login')
                else:
                    messages.error(request, 'User does not have an assigned role.')
                    return redirect('login')
            else:
                if not user.is_active:
                    messages.error(request, 'Your account is not active.')
                else:
                    messages.error(request, 'Your account is not approved yet. Please wait for approval.')
        else:
            messages.error(request, 'Invalid email or password.')

    return render(request, 'login.html')




from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect


@login_required
def approve_request(request, request_id):
    # Get the approval request that the Balai LG needs to approve/reject
    approval_request = get_object_or_404(ApprovalRequest, id=request_id, approver=request.user)
    
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'approve':
            approval_request.status = 'Approved'
            approval_request.user.approved = True  # Set user as approved
            approval_request.user.save()  # Save user to apply approval
        elif action == 'reject':
            approval_request.status = 'Rejected'
        approval_request.save()  # Save the approval request status

        messages.success(request, f"Request has been {approval_request.status.lower()}.")
        return redirect('balai_dashboard')  # Redirect to the balai dashboard
    
    # If not a POST request, render the approval request page
    return render(request, 'approve_request.html', {'approval_request': approval_request})


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import User, Role

@login_required
def balai_dashboard(request):
    logged_in_user = request.user
    # Fetch the users who are awaiting approval for Balai LG
    province_users_pending_approval = User.objects.filter(
        role__role_name=Role.PROVINCIAL_LG, 
        approved=False
    )
    province_links = Link.objects.filter(province=logged_in_user.province)
    kabupaten_links = Link.objects.filter(kabupaten=logged_in_user.Kabupaten)
    if request.method == 'POST':
        # Get the user_id and action (approve or reject) from the POST request
        user_id = request.POST.get('user_id')
        action = request.POST.get('action')
        
        if user_id:
            user = get_object_or_404(User, id=user_id)
            
            if action == 'approve':
                # Mark user as approved
                user.approved = True
                user.save()
                messages.success(request, f"User {user.email} has been approved.")
            
            elif action == 'reject':
                # Mark user as rejected
                user.approved = False  # You can also create a 'rejected' field if needed
                user.is_active = False  # Disable the user from logging in
                user.save()
                messages.warning(request, f"User {user.email} has been rejected and will not be able to log in.")

        # Redirect back to the dashboard to reflect changes
        return redirect('balai_dashboard')

    # Pass the pending approval users to the template
    return render(request, 'balai_dashboard.html', {
        'province_users_pending_approval': province_users_pending_approval, 'province_links' : province_links ,
        'kabupaten_links' : kabupaten_links
    })


    

@login_required
def province_dashboard(request):
    logged_in_user = request.user
    if request.user.role.role_name != Role.PROVINCIAL_LG:
        messages.error(request, "Unauthorized access.")
          # Redirect to a default dashboard
    province_links = Link.objects.filter(province=logged_in_user.province)
    kabupaten_links = Link.objects.filter(kabupaten=logged_in_user.Kabupaten)
    # Get pending approval requests for Kabupaten users
    kabupaten_users_pending_approval = ApprovalRequest.objects.filter(
        user__role__role_name=Role.KABUPATEN_LG, 
        status='Pending',
        approver=request.user
    )

    if request.method == 'POST':
        # Handle approval or rejection
        request_id = request.POST.get('request_id')
        action = request.POST.get('action')

        if request_id:
            approval_request = get_object_or_404(ApprovalRequest, id=request_id, approver=request.user)

            if action == 'approve':
                approval_request.status = 'Approved'
                approval_request.user.approved = True
                approval_request.user.save()
                approval_request.save()
                messages.success(request, f"User {approval_request.user.email} has been approved.")

            elif action == 'reject':
                approval_request.status = 'Rejected'
                approval_request.user.is_active = False
                approval_request.user.save()
                approval_request.save()
                messages.warning(request, f"User {approval_request.user.email} has been rejected.")

            return redirect('province_dashboard')  # Redirect to refresh the list

    return render(request, 'province_dashboard.html', {
        'kabupaten_users_pending_approval': kabupaten_users_pending_approval, 'province_links':province_links , 
        'kabupaten_links': kabupaten_links
    })


@login_required
def kabupaten_dashboard(request):
    logged_in_user = request.user

    # Ensure the user has the appropriate role
    if logged_in_user.role.role_name != Role.KABUPATEN_LG:
        messages.error(request, "Unauthorized access.")
        return redirect('default_dashboard')  # Redirect to a default dashboard or error page

    # Filter links belonging to the user's kabupaten
    kabupaten_links = Link.objects.filter(kabupaten=logged_in_user.Kabupaten)

    # Fetch pending approval requests for users under this kabupaten
    if request.method == 'POST':
        # Handle approval or rejection of user requests
        request_id = request.POST.get('request_id')
        action = request.POST.get('action')

        if request_id:
            approval_request = get_object_or_404(ApprovalRequest, id=request_id, approver=request.user)

            if action == 'approve':
                approval_request.status = 'Approved'
                approval_request.user.approved = True
                approval_request.user.save()
                approval_request.save()
                messages.success(request, f"User {approval_request.user.email} has been approved.")

            elif action == 'reject':
                approval_request.status = 'Rejected'
                approval_request.user.is_active = False
                approval_request.user.save()
                approval_request.save()
                messages.warning(request, f"User {approval_request.user.email} has been rejected.")

            return redirect('kabupaten_dashboard')  # Redirect to refresh the list

    # Prepare the context for rendering the dashboard
    context = {
        'kabupaten_links': kabupaten_links,
    }

    return render(request, 'kabupaten_dashboard.html', context)








def super_admin_dashboard(request):
    user = User.objects.get(id=request.session['user_id'])

    # Super Admin should have access to all data (Provinces, Balai, Kabupaten)
    if user.user_level == 'super_admin':
        provinces = Province.objects.all()
        balais = balais.objects.all()
        kabupatens = Kabupaten.objects.all()
        context = {
            'user': user,
            'provinces': provinces,
            'balais': balais,
            'kabupatens': kabupatens,
        }
        return render(request, 'super_admin_dashboard.html', context)
    else:
        return HttpResponse("You are not authorized to view this page.")'''

from rest_framework.permissions import AllowAny
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, permission_classes



@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    """
    Registers a user and sends OTP to the user's email.
    """
    if request.method == 'POST':
        serializer = UserRegistrationSerializer(data=request.data)
        
        if serializer.is_valid():
            username = serializer.validated_data['username']
            email = serializer.validated_data['email']
            role_id = serializer.validated_data['role']
            balai_id = serializer.validated_data.get('balai')
            province_id = serializer.validated_data.get('province')
            kabupaten_id = serializer.validated_data.get('kabupaten')
            password = serializer.validated_data['password']

            # Check if the username or email already exists
            if User.objects.filter(username=username).exists():
                return Response({'detail': 'Username already exists.'}, status=status.HTTP_400_BAD_REQUEST)
            elif User.objects.filter(email=email).exists():
                return Response({'detail': 'Email already registered.'}, status=status.HTTP_400_BAD_REQUEST)
            
            # Validate Role, Balai, Province, and Kabupaten
            try:
                role = Role.objects.get(id=role_id)
                balai = Balai.objects.get(id=balai_id) if balai_id else None
                province = Province.objects.get(id=province_id) if province_id else None
                kabupaten = Kabupaten.objects.get(id=kabupaten_id) if kabupaten_id else None
            except (Role.DoesNotExist, Balai.DoesNotExist, Province.DoesNotExist, Kabupaten.DoesNotExist):
                return Response({'detail': 'Invalid role or location data.'}, status=status.HTTP_400_BAD_REQUEST)
            
            # Check if OTP is already sent to this email
            cached_otp = cache.get(email)
            if cached_otp:
                return Response({'detail': 'OTP already sent. Please verify it.'}, status=status.HTTP_400_BAD_REQUEST)
            # Generate OTP and cache it for 5 minutes
            otp = random.randint(1000, 9999)
            cache.set(email, otp, timeout=300)

            # Send OTP email
            send_mail(
                'Your OTP Code',
                f'Your OTP code is {otp}',
                settings.DEFAULT_FROM_EMAIL,
                [email],
                fail_silently=False,
            )

            # Store user data in session (we will store it in the request data for simplicity in the API)
            request.session['user_data'] = {
                'username': username,
                'email': email,
                'role': role.id,
                'balai': balai.id if balai else None,
                'province': province.id if province else None,
                'kabupaten': kabupaten.id if kabupaten else None,
                'password': password,
            }

            return Response({'detail': 'OTP sent successfully. Please verify it.'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def verify_otp(request):
    """
    Verifies OTP and completes user registration if OTP is correct.
    """
    if request.method == 'POST':
        serializer = OTPVerificationSerializer(data=request.data)

        if serializer.is_valid():
            otp = serializer.validated_data['otp']
            user_data = request.session.get('user_data')

            if not user_data:
                return Response({'detail': 'Session expired. Please register again.'}, status=status.HTTP_400_BAD_REQUEST)

            cached_otp = cache.get(user_data['email'])

            if str(otp) == str(cached_otp):
                # Create the user
                user = User.objects.create_user(
                    email=user_data['email'],
                    username=user_data['username'],
                    password=user_data['password'],
                    role_id=user_data['role'],
                    balai_id=user_data.get('balai'),
                    province_id=user_data.get('province'),
                    Kabupaten_id=user_data.get('kabupaten'),
                    approved=(user_data['role'] == 'balai_lg'),  # Auto-approve Balai LG users
                )

                # Clear session and cache
                cache.delete(user_data['email'])
                del request.session['user_data']

                return Response({'detail': 'Registration successful.'}, status=status.HTTP_201_CREATED)
            else:
                return Response({'detail': 'Invalid OTP. Please try again.'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





'''@api_view(['POST'])
@permission_classes([AllowAny])
def api_login(request):
    """
    API Login endpoint to authenticate a user and return a JWT token.
    """
    # Deserialize the request data using the LoginSerializer
    serializer = LoginSerializer(data=request.data)

    # Validate the data using the serializer
    if serializer.is_valid():
        email = serializer.validated_data['email']
        password = serializer.validated_data['password']

        # Authenticate the user
        user = authenticate(request, email=email, password=password)

        # Debugging: print user
        print(f"Authenticated User: {user}")

        if user is not None:
            if user.is_active and (user.approved or user.is_superuser):
                # If user is authenticated and active, generate a JWT token
                refresh = RefreshToken.for_user(user)
                access_token = refresh.access_token

                response_data = {
                    'refresh_token': str(refresh),
                    'access_token': str(access_token),
                    'user_id': user.id,
                    'email': user.email,
                    'role': user.role.role_name if user.role else None,
                    'message': f'User {user.email} logged in successfully.'
                }
                
                # Return a successful response with JWT tokens
                return Response(response_data, status=status.HTTP_200_OK)
            else:
                # If user is inactive or not approved
                if not user.is_active:
                    return Response({'detail': 'Your account is not active.'}, status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response({'detail': 'Your account is not approved yet. Please wait for approval.'}, 
                                    status=status.HTTP_400_BAD_REQUEST)
        else:
            # If authentication fails
            return Response({'detail': 'Invalid email or password.'}, status=status.HTTP_400_BAD_REQUEST)
    else:
        # If serializer validation fails
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)'''
@api_view(['POST'])
@permission_classes([AllowAny])
def api_login(request):
    """
    API Login endpoint to authenticate a user and return a JWT token.
    """
    serializer = LoginSerializer(data=request.data)

    if serializer.is_valid():
        email = serializer.validated_data['email']
        password = serializer.validated_data['password']

        user = authenticate(request, email=email, password=password)

        if user is not None:
            # Check if user is active
            if not user.is_active:
                return Response({'detail': 'Your account is not active.'}, status=status.HTTP_400_BAD_REQUEST)

            # Specific check for Provincial LG users
            if user.role.role_name == Role.PROVINCIAL_LG:
                if not user.approved:
                    return Response({
                        'detail': 'Your account is pending approval from a Balai LG user.'
                    }, status=status.HTTP_400_BAD_REQUEST)

            # General approval check
            if not user.approved and not user.is_superuser:
                return Response({'detail': 'Your account is not approved yet. Please wait for approval.'}, 
                                status=status.HTTP_400_BAD_REQUEST)

            # Generate JWT token for authenticated users
            refresh = RefreshToken.for_user(user)
            access_token = refresh.access_token

            response_data = {
                'refresh_token': str(refresh),
                'access_token': str(access_token),
                'user_id': user.id,
                'email': user.email,
                'role': user.role.role_name if user.role else None,
                'message': f'User {user.email} logged in successfully.'
            }

            return Response(response_data, status=status.HTTP_200_OK)
        else:
            return Response({'detail': 'Invalid email or password.'}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import User, ApprovalRequest, Link, Role
from .serializers import UserSerializer, ApprovalRequestSerializer
from django.shortcuts import get_object_or_404

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def balai_dashboard(request):
    logged_in_user = request.user

    if request.method == 'GET':
        # Fetching users pending approval for BALAI_LG role
        users_pending_approval = User.objects.filter(role__role_name=Role.BALAI_LG, approved=False)
        approval_requests = ApprovalRequest.objects.filter(status='Pending', approver=logged_in_user)
        
        # Fetching links for the logged-in user's province and kabupaten
        province_links = Link.objects.filter(province=logged_in_user.province)
        kabupaten_links = Link.objects.filter(kabupaten=logged_in_user.Kabupaten)
        
        # Serializing the data
        user_serializer = UserSerializer(users_pending_approval, many=True)
        approval_request_serializer = ApprovalRequestSerializer(approval_requests, many=True)
        
        # Adding the province and kabupaten links to the response data
        return Response({
            'users_pending_approval': user_serializer.data,
            'approval_requests': approval_request_serializer.data,
            'province_links': province_links.values(),  # Optionally serialize links
            'kabupaten_links': kabupaten_links.values()  # Optionally serialize links
        })

    elif request.method == 'POST':
        # Handling approval or rejection of users
        user_id = request.data.get('user_id')
        action = request.data.get('action')

        if user_id:
            user = get_object_or_404(User, id=user_id)

            if action == 'approve':
                user.approved = True
                user.save()
                return Response({'detail': f'User {user.email} has been approved.'}, status=200)
            elif action == 'reject':
                user.approved = False
                user.is_active = False
                user.save()
                return Response({'detail': f'User {user.email} has been rejected.'}, status=200)

        return Response({'detail': 'Invalid data'}, status=400)


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def province_dashboard(request):
    logged_in_user = request.user
    
    if request.user.role.role_name != Role.PROVINCIAL_LG:
        return Response({"detail": "Unauthorized access."}, status=status.HTTP_403_FORBIDDEN)

    if request.method == 'GET':
        # Fetching the province and kabupaten links
        province_links = Link.objects.filter(province=logged_in_user.province)
        kabupaten_links = Link.objects.filter(kabupaten=logged_in_user.Kabupaten)
        
        # Fetching pending approval requests for Kabupaten users
        kabupaten_users_pending_approval = ApprovalRequest.objects.filter(
            user__role__role_name=Role.KABUPATEN_LG, 
            status='Pending',
            approver=request.user
        )
        
        # Serializing the approval requests
        approval_request_serializer = ApprovalRequestSerializer(kabupaten_users_pending_approval, many=True)
        
        return Response({
            'kabupaten_users_pending_approval': approval_request_serializer.data,
            'province_links': province_links.values(),
            'kabupaten_links': kabupaten_links.values()
        })

    elif request.method == 'POST':
        # Handling approval or rejection of users
        request_id = request.data.get('request_id')
        action = request.data.get('action')

        if request_id and action:
            approval_request = get_object_or_404(ApprovalRequest, id=request_id, approver=request.user)

            if action == 'approve':
                approval_request.status = 'Approved'
                approval_request.user.approved = True
                approval_request.user.save()
                approval_request.save()
                return Response({'detail': f'User {approval_request.user.email} has been approved.'}, status=status.HTTP_200_OK)

            elif action == 'reject':
                approval_request.status = 'Rejected'
                approval_request.user.is_active = False
                approval_request.user.save()
                approval_request.save()
                return Response({'detail': f'User {approval_request.user.email} has been rejected.'}, status=status.HTTP_200_OK)

        return Response({'detail': 'Invalid data or missing request_id/action'}, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def kabupaten_dashboard(request):
    logged_in_user = request.user

    # Ensure the user has the appropriate role (Kabupaten LG role)
    if logged_in_user.role.role_name != Role.KABUPATEN_LG:
        return Response({"detail": "Unauthorized access."}, status=status.HTTP_403_FORBIDDEN)

    # Fetching the links associated with the logged-in user's kabupaten
    kabupaten_links = Link.objects.filter(kabupaten=logged_in_user.Kabupaten)

    # Return the kabupaten links in the response
    return Response({
        'kabupaten_links': kabupaten_links.values('id', 'link_name', 'official_length_km', 'actual_length_km', 'highest_access', 'link_function')
    })
