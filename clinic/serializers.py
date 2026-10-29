from rest_framework.serializers import ModelSerializer
from clinic.models import DoctorDb,AppointmentsDb
from rest_framework import serializers

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
    
    def validate(self,validated_data):

        ph = validated_data.get("phone")
        date = validated_data.get("appointment_date")

        if AppointmentsDb.objects.filter(
            phone = ph,
            appointment_date = date
        ).exists():
            raise serializers.ValidationError("Already Booked...")
        else:
            return validated_data