# JngMkk
from finalproject.models import Plants, PlantRequest
from django import forms
import datetime

t = datetime.date.today

class PlantForm(forms.Form):
    plant_name = forms.CharField(required=False)
    plant_nickname = forms.CharField(required=False)
    plant_date = forms.DateField(initial=t, widget=forms.DateInput(format='%Y-%m-%d', attrs={"type": "date", "class": "today_date", "max": t}))
    water_date = forms.DateField(initial=t, widget=forms.DateInput(format='%Y-%m-%d', attrs={"type": "date", "class": "today_date", "max": t}))

    def clean(self):
        data = self.cleaned_data
        if data["plant_name"] == "":
            raise forms.ValidationError("식물 이름을 알려주세요!")
        elif Plants.objects.filter(name=data["plant_name"]).count() == 0:
            raise forms.ValidationError("아직 저희가 모르는 식물이에요 ㅠㅠ")
        elif data["plant_nickname"] == "":
            raise forms.ValidationError("식물에게 별명을 지어주세요!")
        elif len(data["plant_name"]) > 255:
            raise forms.ValidationError("식물 이름은 255자를 넘을 수 없어요!")
        elif len(data["plant_nickname"]) > 50:
            raise forms.ValidationError("식물 별명은 50자 이하로 입력해주세요!")
        return data

class PlantRequestForm(forms.ModelForm):
    class Meta:
        model = PlantRequest
        fields = ["requestname"]
        widgets = {
            "requestname": forms.TextInput(attrs={"placeholder": "요청할 식물 이름을 입력해주세요."})
        }