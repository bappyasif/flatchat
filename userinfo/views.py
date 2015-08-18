from django.shortcuts import render
from django.http import Http404, HttpResponse, HttpResponseRedirect, Http404, HttpResponseServerError
from django.core.cache import cache
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from userinfo.models import UserData, ApiKeys
from userinfo.serializer import UserProfileSerializer, UserSerializer
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from django.contrib.auth.models import User

# Create your views here.



class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)


@csrf_exempt
@login_required()
def index(request):

    return render(request, "", {})


@csrf_exempt
def rest_signup(request):
    """
        Excepted POST data format: {"username":"jyoti", "password":"js123", "key":"629db2d5c47848a8a7e182cc5494aae9"}
        Before sending POST, remember to fill Apikeys table with md5 keys and use that key.
    """
    if request.method == 'POST':
        try:
            data = JSONParser().parse(request)
            key = data['key']
            del data['key']
            check_key = ApiKeys.objects.filter(md5_key=key)
            if check_key:
                if not check_key[0].used_flag:
                    new_user = User.objects.create_user(**data)
                    ApiKeys.objects.filter(md5_key=key).update(used_flag=True, used_by=new_user)
                    return JSONResponse('Successfully Created.', status=200)
                else:
                    return JSONResponse('Key is already used', status=404)
            else:
                return JSONResponse('Key do not match our DB.', status=404)
        except Exception as e:
            return JSONResponse(str(e), status=404)


@csrf_exempt
def user_list(request):
    """Gives full list of users
    """
    if request.method == 'GET':
        user_info = UserData.objects.all()
        serializer = UserProfileSerializer(user_info, many=True)
        return JSONResponse(serializer.data)
    else:
        return JSONResponse('Using wrong api.', status=404)


@csrf_exempt
def user_detail(request, pk):
    """
    Retrieve, update or delete a code snippet.
    """
    try:
        user_ = UserData.objects.get(pk=pk)
        print (user_)
    except user_.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = UserProfileSerializer(user_)
        return JSONResponse(serializer.data)

    elif request.method =='PUT':
        data = JSONParser.parse(request)
        serializer = UserProfileSerializer(user_, data = data)
        if serializer.is_valid():
            serializer.save()
            return JSONResponse(serializer.data)
        return JSONResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        user_.delete()
        return HttpResponse(status=204)
