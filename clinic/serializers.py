from rest_framework.serializers import ModelSerializer
from clinic.models import DoctorDb,AppointmentsDb


class Doctor_Serializer(ModelSerializer):
    class Meta:
        model = DoctorDb
        fields = '__all__'
        read_only_fields = ['id']

class Appointment_Serializer(ModelSerializer):
    class Meta:
        model = AppointmentsDb
        fields = "__all__"
        read_only_fields = ["id"]