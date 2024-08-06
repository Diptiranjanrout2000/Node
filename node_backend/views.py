import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import JSONParser
from .models import *
from .serializers import *

@api_view(['GET'])
def get_node(request):
    if request.method =='GET':
          Node_objs=Node.objects.all()
    serializer = NodeSerializer(Node_objs,many=True)
    return Response({'status': 200, 'payload':serializer.data})

@api_view(['POST'])
def post_node(request):
    if request.method == 'POST':
        # try:
        data = JSONParser().parse(request)
        nodeid = data.get("node_id")
        print(nodeid)

        node_exist = Node.objects.filter(nodeid=nodeid)

        if node_exist:
            return JsonResponse({"message":"id already exists"})
        node = Node(nodeid=nodeid)
        node.save()
        return JsonResponse({"message":"node created"})
                
       


@api_view(['PUT'])
def update_node(request, nodeid):
    try:
        node = Node.objects.get(nodeid=nodeid)
    except Node.DoesNotExist:
        return JsonResponse({"message": "Node not found"}, status=status.HTTP_404_NOT_FOUND)

    try:
        data = JSONParser().parse(request)
        serializer = NodeSerializer(node, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({"message": "Node updated successfully"}, status=status.HTTP_200_OK)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def delete_node(request, nodeid):
    try:
        node = Node.objects.get(nodeid=nodeid)
    except Node.DoesNotExist:
        return JsonResponse({"message": "Node not found"}, status=status.HTTP_404_NOT_FOUND)

    node.delete()
    return JsonResponse({"message": "Node deleted successfully"}, status=status.HTTP_204_NO_CONTENT)



@api_view(['GET'])
def node_data_get(request):
    if request.method == 'GET':
           NodeModel_objs = NodeModel.objects.all()
    serializer = NodeDataSerializer(NodeModel_objs,many=True)
    return JsonResponse({'status': 200, 'payload':serializer.data})

@api_view(['POST'])
def node_data_post(request):
    if request.method == 'POST':
        data1 = JSONParser().parse(request)
        nodedata = data1.get('node_id')
        gateway_id = data1.get("gateway_id")
        data = data1.get("data_field")
        
        if data is None or not isinstance(data, dict):
            return JsonResponse({"error": "Invalid or missing data_field"}, status=400)
        try:
            node = Node.objects.get(nodeid=nodedata)  
        except Node.DoesNotExist:
            return JsonResponse({"error": "Node not found"}, status=404)
        
        node_model = NodeModel(
            node_id=node,
            gateway_id=gateway_id,
            data=data
        )
        node_model.save()

        return JsonResponse({"message": "node post created"}, status=201)
    

@api_view(['PUT'])
def update_node_data(request, node_id):
    if request.method == 'PUT':
        try:
            # Parse the request data
            data = JSONParser().parse(request)
            new_gateway_id = data.get('gateway_id')
            new_data_field = data.get('data_field')

            # Check for required parameters
            if not new_gateway_id or not new_data_field:
                return JsonResponse({"message": "gateway_id and data_field are required"}, status=status.HTTP_400_BAD_REQUEST)

            # Validate data_field
            if not isinstance(new_data_field, dict):
                return JsonResponse({"error": "Invalid data_field format. Must be a dictionary."}, status=status.HTTP_400_BAD_REQUEST)

            # Check if Node instance exists
            try:
                node = Node.objects.get(nodeid=node_id)
            except Node.DoesNotExist:
                return JsonResponse({"message": "Node not found"}, status=status.HTTP_404_NOT_FOUND)

            # Filter NodeModel instances
            node_models = NodeModel.objects.filter(node_id=node, gateway_id=new_gateway_id)

            if not node_models:
                return JsonResponse({"message": "NodeModel with the given node_id and gateway_id not found"}, status=status.HTTP_404_NOT_FOUND)

            # Update all matching NodeModel instances
            for node_model in node_models:
                node_model.data = new_data_field
                node_model.save()

            return JsonResponse({"message": "NodeModel updated successfully"}, status=status.HTTP_200_OK)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def delete_node_data(request, node_id):
    try:
        # Correct field name for query
        node_model = NodeModel.objects.get(node_id=node_id)
    except NodeModel.DoesNotExist:
        return JsonResponse({"message": "NodeModel not found"}, status=status.HTTP_404_NOT_FOUND)

    node_model.delete()
    return JsonResponse({"message": "NodeModel deleted successfully"}, status=status.HTTP_204_NO_CONTENT)