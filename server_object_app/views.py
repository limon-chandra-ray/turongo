from django.shortcuts import render
from django.http import JsonResponse
from .models import District,Upazila,Division
# Create your views here.
def district_get(request):
    if request.method == 'POST':
        division_id = int(request.POST['division'])
        division = Division.objects.get(id = division_id)
        districts = District.objects.filter(division = division).order_by('district_name').values('id','district_name')
        return JsonResponse({'status':"success",'districts':list(districts)})
    else:
        return JsonResponse({'status':"error"})
    
def upazila_get(request):
    if request.method == 'POST':
        district_id = int(request.POST['district'])
        district = District.objects.get(id = district_id)
        upazilas = Upazila.objects.filter(district = district).order_by('upazila_name').values('id','upazila_name')
        return JsonResponse({'status':"success",'upazilas':list(upazilas)})
    else:
        return JsonResponse({'status':"error"})