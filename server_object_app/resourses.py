from import_export import resources
from .models import Division,District,Upazila
class DivisionResourse(resources.ModelResource):
    class Meta:
        model = Division
    
class DistrictResourse(resources.ModelResource):
    class Meta:
        model = District

class UpazilaResourse(resources.ModelResource):
    class Meta:
        model = Upazila