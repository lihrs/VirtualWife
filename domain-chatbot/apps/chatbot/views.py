import time
import traceback
from django.shortcuts import render, get_object_or_404
import json
from .chat import chat_service
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .config import singleton_sys_config
from .memory.reflection.reflection_generation import ReflectionGeneration
from .customrole.custom_role_generation import singleton_custom_role_generation
from .models import CustomRoleModel
from .forms import CustomRoleForm
import logging
logging.basicConfig(level=logging.INFO)


@api_view(['POST'])
def chat(request):
    '''
      聊天
    :param request:
    :return:
    '''
    data = json.loads(request.body.decode('utf-8'))
    chat = None
    query = data["query"]
    you_name = data["you_name"]
    role_name = data["role_name"]
    try:
        chat = chat_service.chat(
            role_name=role_name, you_name=you_name, query=query).strip()
        if chat == "":
            print("chat is null")
            chat = "小蜜蜂告诉我,她刚刚在路上遇到一团奇怪的迷雾,导致消息晚点到达,请耐心等待!"
    except Exception as e:
        traceback.print_exc()
        print("chat error: %s" % str(e))
        chat = '哎呀,系统小哥哥突然打了个呵欠,估计是太辛苦了!需要补充能量!等他喝几口咖啡,打个盹儿,很快就会精神抖擞地回来工作的!'
    return Response({"response": chat, "code": "200"})


@api_view(['GET'])
def custom_role_list(request):
    '''
      获取角色列表
    :param request:
    :return:
    '''
    role_list = singleton_custom_role_generation.list()
    return Response({"response": role_list, "code": "200"})


@api_view(['GET'])
def vrm_model_list(request):
    '''
      获取角色模型列表
    :param request:
    :return:
    '''
    vrm_models = [
        {
            "id": "1",
            "name": "わたあめ_03.vrm",
        },
        {
            "id": "2",
            "name": "わたあめ_02.vrm",
        },
        {
            "id": "3",
            "name": "hailey.vrm",
        },
        {
            "id": "4",
            "name": "后藤仁.vrm",
        },
        {
            "id": "5",
            "name": "aili.vrm",
        }
    ]
    return Response({"response": vrm_models, "code": "200"})


@api_view(['POST'])
def save_config(request):
    '''
      保存系统配置
    :param request:
    :return:
    '''
    data = json.loads(request.body.decode('utf-8'))
    config = data["config"]
    singleton_sys_config.save(config)
    singleton_sys_config.load()
    return Response({"response": config, "code": "200"})


@api_view(['GET'])
def get_config(request):
    '''
      获取系统配置
    :param request:
    :return:
    '''
    return Response({"response": singleton_sys_config.get(), "code": "200"})


@api_view(['GET'])
def reflection_generation(request):
    '''
      生成新记忆
    :return:
    '''
    rg = ReflectionGeneration()
    rg.generation(role_name="Maiko")
    timestamp = time.time()
    expr = f'timestamp <= {timestamp}'
    result = singleton_sys_config.memory_storage_driver.pageQuery(
        1, 100, expr=expr)
    return Response({"response": result, "code": "200"})


@api_view(['GET'])
def clear_memory(request):
    '''
      删除测试记忆
    :return:
    '''
    result = singleton_sys_config.memory_storage_driver.clear("alan")
    return Response({"response": result, "code": "200"})


@api_view(['GET'])
def role_list(request):
    roles = CustomRoleModel.objects.all()
    return Response({"response": roles, "code": "200"})


@api_view(['GET'])
def role_detail(request, pk):
    role = get_object_or_404(CustomRoleModel, pk=pk)
    return Response({"response": role, "code": "200"})


@api_view(['POST'])
def role_create(request):
    form = CustomRoleForm(request.POST)
    if form.is_valid():
        form.save()
        return Response({"response": form, "code": "200"})

@api_view(['POST'])
def role_edit(request, pk):
    role = get_object_or_404(CustomRoleModel, pk=pk)
    form = CustomRoleForm(request.POST, instance=role)
    if form.is_valid():
        form.save()
        return Response({"response": form, "code": "200"})


@api_view(['POST'])
def role_delete(request, pk):
    role = get_object_or_404(CustomRoleModel, pk=pk)
    role.delete()
    return Response({"response": "", "code": "200"})
