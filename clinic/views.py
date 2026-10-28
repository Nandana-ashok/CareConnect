from django.shortcuts import render,get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from clinic.models import DoctorDb,AppointmentsDb
from clinic.serializers import Doctor_Serializer,Appointment_Serializer

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