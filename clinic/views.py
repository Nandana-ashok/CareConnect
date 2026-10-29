from django.shortcuts import render,get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from clinic.models import DoctorDb,AppointmentsDb
from clinic.serializers import Doctor_Serializer,Appointment_Serializer
from datetime import time,datetime,timedelta

# Create your views here.

class DoctorCreateViewListView(APIView):
    def get(self,request):
        qs = DoctorDb.objects.all()
        serializer_instance = Doctor_Serializer(qs,many=True)
        return Response(data=serializer_instance.data)

    def post(self,request):

        form_data = request.data
        serializer_instance = Doctor_Serializer(data=form_data)
        if serializer_instance.is_valid():
            serializer_instance.save()
            return Response(data=serializer_instance.data)
        else:
            return Response(data=serializer_instance.errors)

class DoctorRetrievalUpdateDelteView(APIView):
    def get(self,request,pk):

        qs = get_object_or_404(DoctorDb,id=pk)
        serializer_instance = Doctor_Serializer(qs)
        return Response(data=serializer_instance.data)

    def put(self,request,pk):

        form_data = request.data
        doctor_object = get_object_or_404(DoctorDb,id=pk)
        serializer_instance = Doctor_Serializer(data=form_data,instance=doctor_object)

        if serializer_instance.is_valid():
            serializer_instance.save()
            return Response(data=serializer_instance.data)
        else:
            return Response(data=serializer_instance.errors)

    def delete(self,request,pk):

        doctor_obj = get_object_or_404(DoctorDb,id=pk)
        doctor_obj.delete()
        return Response({
            "Message":"Doctor deleted successfully...."
        })

class AppointmentListCreateView(APIView):
    def get(self,request):

        qs = AppointmentsDb.objects.all()
        serializer_instance = Appointment_Serializer(qs,many=True)
        return Response(data=serializer_instance.data)

    def post(self,request):

        form_data = request.data
        serializer_instance = Appointment_Serializer(data=form_data)

        if serializer_instance.is_valid():

            appointment_date = serializer_instance.validated_data.get("appointment_date")
            doctor_id = serializer_instance.validated_data.get("doctor_id")

            last_appointment = AppointmentsDb.objects.filter(
                appointment_date = appointment_date,
                doctor_id = doctor_id
            ).order_by("-token_number").first()

            if last_appointment is None:

                form_data["token_number"] = 1
                form_data["appointment_time"] = time(10,0)

            else:

                form_data["token_number"] = last_appointment.token_number + 1
                current_time = datetime.combine(appointment_date,last_appointment.appointment_time) 
                form_data ["appointment_time"] = current_time + timedelta(minutes=15)

            qs = AppointmentsDb.objects.create(**form_data)
            serializer_instance = Appointment_Serializer(qs)
            return Response(data={
                            "Status" : "Booked successfully",
                            "Token": form_data["token_number"],
                            "Appointment Time": form_data["appointment_time"].strftime(" %I:%M %p")
            }
            )
        else:
            return Response(data=serializer_instance.errors)

        