from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import *
import requests
from django.contrib.auth.models import Group, User
from rest_framework import status
from .models import Project
from rest_framework import generics
from .models import Project
from .serializers import ProjectSerializer
from datetime import date
from rest_framework import generics, serializers
from django.db.models import Q
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.auth.hashers import check_password
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from datetime import timedelta




def response_func(status: bool ,msg: str, data: dict):
    res = {
        'status': status,
        'message': msg,
        'data': data
    }
    return res 


class RemotePost:
    def __init__(self, username, password):
        self.UserName = username
        self.Password = password


    def Sendsms(self, Number, message, rec, sms):
        url = "http://smspanel.Trez.ir/SendMessageWithPost.ashx"
        payload = {
            'Username': self.UserName,
            'Password': self.Password,
            'PhoneNumber': Number,
            'MessageBody': message,
            'RecNumber': rec,
            'Smsclass': sms
        }
        response = requests.post(url, data=payload)
        
        if response.status_code == 200:
            # SMS sent successfully
            return response.text
        else:
            # SMS sending failed
            return "SMS sending failed. Status code: {}".format(response.status_code)

            
# print(group)

# # print(group.id, group.name)
# user =User.objects.get(username='hb')
# user.groups.add(group.id)

# #getting all users in specific group

class Authentication(APIView):

    def post(self, request):
        try:
            user = User.objects.get(username__exact=request.data['userName'])
            if check_password(request.data['password'], user.password):

                refresh = RefreshToken.for_user(request.user)
                print(refresh.payload['exp'])
                

                access_exp = refresh.access_token.lifetime/60
                refresh_exp = refresh.lifetime/60

                return Response(response_func(
                        True,
                        "",
                        {
                        'refresh': str(refresh),
                        'access': str(refresh.access_token),
                        'exp': access_exp,
                        'expRefresh': refresh_exp,
                    }
                    ), status=status.HTTP_200_OK
                    ) 
            
            return Response(response_func(
                False,
                "",
                None
            ), status=status.HTTP_200_OK
            )
            

        except Exception as e:
            return Response(response_func(
                False,
                "",
                None
            ), status=status.HTTP_401_UNAUTHORIZED
            )



class Refresh(APIView):
    def post(self, request):

        s = requests.post('http://localhost:8000/api/v1/panel/refresh-token/', 
                          data={"refresh": request.data['refresh']})
        
        
        
        return Response(response_func(
            True,
            "",
            {
                'access': s.json()['access'],
                'exp': timedelta(minutes=15)
            }
        ), status=status.HTTP_200_OK
        ) 




        

class Sms(generics.GenericAPIView):
    queryset = Group.objects.filter(id=3)
    serializer_class = SmsSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Retrieve the message from the serializer data
        message = serializer.validated_data['message']

        # Rest of your code

        try:
            users_phone = []
            group = Group.objects.get(id=4) 
            users = group.user_set.all()
            
            for user in users:
                users_phone.append(user.username)

            remotePost = RemotePost("Sadegh888", "3726201254")
            state = remotePost.Sendsms("5000248725", message, users_phone , 1)

            return Response(
                response_func(True, "پیام شما پس از تایید سامانه پیامکی برای کاربران ارسال خواهد شد", {'code': state}),  
                status=status.HTTP_200_OK
            )
        
        except Exception as e:
            return Response(
                response_func(True, "ارسال پیام با مشکل مواجه شده است", {'error': str(e)}),  
                status=status.HTTP_400_BAD_REQUEST
            )
        

        
class Statistics(generics.GenericAPIView):

    def get(self, request):
        try:
            state_counts = {
                'ongoing': Project.objects.filter(state=0).count(),
                'canceled': Project.objects.filter(state=1).count(),
                'deal': Project.objects.filter(state=2).count(),
            }
        
            return Response(
                    response_func(True, "درخواست موفق", {'data': state_counts}),  
                    status=status.HTTP_200_OK
                )
        
        except Exception as e:
            return Response(
                    response_func(True, "درخواست ناموفق", {'error': str(e)}),  
                    status=status.HTTP_400_BAD_REQUEST
                )
        



class TodayProjectListAPI(generics.ListAPIView):
    serializer_class = PartialProjectSerializer

    def get_queryset(self):
        today = date.today()
        return Project.objects.filter(registered_date=today)


class NotTrackedProjectListAPI(generics.ListAPIView):
    serializer_class = ProjectsSerializer

    def get_queryset(self):
        today = date.today()
        queryset = Project.objects.filter(state=0, registered_date__lte=today)
        return queryset
    

class ProjectCreateAPI(generics.GenericAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        employee_username = serializer.validated_data.get('employeeUsername')
        employer_username = serializer.validated_data.get('employerUsername')
        employee_sms = serializer.validated_data.get('employeeSms', False)
        employer_sms = serializer.validated_data.get('employerSms', False)

        try:
            employee_obj, employee_bool = User.objects.get_or_create(username=employee_username)
            if not employee_sms:
                employee_obj.groups.add(4)
        
            employer_obj, employer_bool = User.objects.get_or_create(username=employer_username)
            if not employer_sms:
                employer_obj.groups.add(4)

        except Exception as e:
            print(str(e))

        try:
            project = Project.objects.get_or_create(
                employee = employee_obj,
                employer = employer_obj,
                connection = serializer.validated_data.get('connection'),
                check_date = serializer.validated_data.get('checkDate'),
                how_meet = serializer.validated_data.get('howMeet'),
                state = serializer.validated_data.get('state'),
                level = serializer.validated_data.get('level'),
                address = serializer.validated_data.get('address'),
                floor = serializer.validated_data.get('floor'),
                region = serializer.validated_data.get('region'),
                partner = serializer.validated_data.get('partner'),
                visit = serializer.validated_data.get('visit'),
                in_person = serializer.validated_data.get('inPerson'),
                checkout = serializer.validated_data.get('checkout'),
                immediate = serializer.validated_data.get('immediate'),
            )
            return Response(
                    response_func(True, "درخواست موفق", {'projectId': str(project[0])}),  
                    status=status.HTTP_200_OK
                )
        except Exception as e:
            return Response(
                    response_func(True, "درخواست ناموفق", {'error': str(e)}),  
                    status=status.HTTP_400_BAD_REQUEST
                )


class ProjectRetrieveAPI(generics.RetrieveAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    lookup_field = 'id'
    lookup_url_kwarg = 'projectId'


class ProjectUpdateAPI(generics.GenericAPIView):
    serializer_class = PartialSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        id = serializer.validated_data.get("id")
        check_date = serializer.validated_data.get("checkDate")

        try:
            project = Project.objects.get(id=id)
            print(project, check_date)
            project.check_date = check_date
            project.save()

            return Response(
                    response_func(True, "ویرایش با موفقیت انجام شد", {}), 
                    status=status.HTTP_200_OK
                )
        except Exception as e:
            return Response(
                    response_func(True, "ویرایش انجام نشد", {'error': str(e)}), 
                    status=status.HTTP_404_NOT_FOUND
                )


from rest_framework.generics import ListAPIView
from django.db.models import Q
from rest_framework.generics import ListAPIView
from .models import Project
from .serializers import ProjectSerializer
from django.contrib.auth.models import User

class ProjectSearch(APIView):
    serializer_class = ProjectSearchSerializer

    def get(self, request):
        project_type = request.GET.get('type')
        search_text = request.GET.get('text')
        if project_type == 'user':
            projects = Project.objects.filter(Q(employee__username=search_text) | Q(employer__username=search_text))
        elif project_type == 'name':
            if len(search_text.split(' ')) == 1:
                projects = Project.objects.filter(
                    Q(employee__first_name__icontains=search_text) | Q(employee__last_name__icontains=search_text) |
                    Q(employer__first_name__icontains=search_text) | Q(employer__last_name__icontains=search_text)
                )
            else:
                projects = Project.objects.filter(
                    Q(employee__first_name__icontains=search_text[0]) | Q(employee__last_name__icontains=search_text[1]) |
                    Q(employer__first_name__icontains=search_text[0]) | Q(employer__last_name__icontains=search_text[1])
                )
        else:
            projects = Project.objects.none()
        
        serialized_projects = self.serializer_class(projects, many=True)
        
        return Response({'projects': serialized_projects.data})

