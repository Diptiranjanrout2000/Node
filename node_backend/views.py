
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
import openpyxl
from openpyxl import Workbook
import os
from datetime import datetime

@api_view(['GET'])
def get_node(request):
    if request.method == 'GET':
        Node_objs = Node.objects.all()
        serializer = NodeSerializer(Node_objs, many=True)
        return Response({'status': 200, 'payload': serializer.data})

@api_view(['POST'])
def post_node(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        nodeid = data.get("node_id")
        print(nodeid)
        try:
            node_exist = Node.objects.filter(nodeid=nodeid)
            if node_exist.exists():
                return JsonResponse({"message": "id already exists"})
            else:
                node = Node(nodeid=nodeid)
                node.save()
                return JsonResponse({'message': 'node data post Successful'})
        except:
            return JsonResponse({'message': 'Error'})

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
def node_data_get_all(request):
    if request.method == 'GET':
        NodeModel_objs = NodeModel.objects.all()
        serializer = NodeDataSerializer(NodeModel_objs, many=True)
        return JsonResponse({'status': 200, 'payload': serializer.data})

@api_view(['GET'])
def node_data_get(request):
    if request.method == 'GET':
        NodeModel_obj = NodeModel.objects.last()
        if NodeModel_obj is None:
            return JsonResponse({'status': 404, 'message': 'No data found'}, status=404)

        serializer = NodeDataSerializer(NodeModel_obj)
        return JsonResponse({'status': 200, 'payload': serializer.data}, status=200)
    


# @api_view(['GET'])
# def node_data_multiple(request):
#     if request.method == 'GET':
#         NodeModel_objs = NodeModel.objects.order_by('-id')[:100]
#         if not NodeModel_objs.exists():
#             return JsonResponse({'status': 404, 'message': 'No data found'}, status=404)

#         serializer = NodeDataSerializer(NodeModel_objs, many=True)
#         return JsonResponse({'status': 200, 'payload': serializer.data}, status=200)

@api_view(['GET'])
def node_data_multiple(request):
    if request.method == 'GET':
        count = request.GET.get('count')  # Get the 'count' parameter from the query string
        if not count or not count.isdigit():
            return JsonResponse({'status': 400, 'message': 'Please specify how many records you want to retrieve using the "count" query parameter.'}, status=400)

        count = int(count)
        NodeModel_objs = NodeModel.objects.order_by('-id')[:count]
        if not NodeModel_objs.exists():
            return JsonResponse({'status': 404, 'message': 'No data found'}, status=404)

        serializer = NodeDataSerializer(NodeModel_objs, many=True)
        return JsonResponse({'status': 200, 'payload': serializer.data}, status=200)
    
    
# @api_view(['POST'])
# def node_data_post(request):
#     if request.method == 'POST':
#         data1 = JSONParser().parse(request)
#         nodedata = data1.get('node_id')
#         gateway_id = data1.get("gateway_id")
#         data = data1.get("data_field")

#         # Check if data is None or not a dict
#         if data is None or not isinstance(data, dict):
#             return JsonResponse({"error": "Invalid or missing data_field"}, status=400)
        
#         try:
#             node = Node.objects.get(nodeid=nodedata)
#             if node:
#                 node_model = NodeModel.objects.create(
#                     node_id=node,
#                     gateway_id=gateway_id,
#                     data_field=data
#                 )
#                 node_model.save()

#                 return JsonResponse({"message": "Node post created"}, status=201)
#             else:
#                 return JsonResponse({"error": "Node not found"}, status=404)
#         except Exception as e:
#             return JsonResponse({"error": str(e)}, status=400)


@api_view(['POST'])
def node_data_post(request):
    if request.method == 'POST':
        data1 = JSONParser().parse(request)
        nodedata = data1.get('node_id')
        gateway_id = data1.get("gateway_id")
        data = data1.get("data_field")

        # Check if data is None or not a dict
        if data is None or not isinstance(data, dict):
            return JsonResponse({"error": "Invalid or missing data_field"}, status=400)

        try:
            node = Node.objects.get(nodeid=nodedata)
            if node:
                try:
                    # Create and save NodeModel instance
                    node_model = NodeModel.objects.create(
                        node_id=node,
                        gateway_id=gateway_id,
                        data_field=data
                    )
                    node_model.save()
                    print(f"Data successfully saved to NodeModel: {node_model.id}")

                except Exception as e:
                    print(f"Error saving to NodeModel: {e}")
                    return JsonResponse({"error": "Failed to save data to the database"}, status=500)

                # File path to save the Excel file
                file_path = 'nodedatabase/node_data.xlsx'

                try:
                    if os.path.exists(file_path):
                        # Load existing workbook
                        wb = openpyxl.load_workbook(file_path)
                        ws = wb.active
                    else:
                        # Create a new workbook if file does not exist
                        wb = Workbook()
                        ws = wb.active
                        ws.title = "Node Data"
                        # Write the headers
                        ws.append(["node_id", "gateway_id", "data_field", "timestamp"])

                    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    ws.append([nodedata, gateway_id, str(data), timestamp])
                    wb.save(file_path)

                except Exception as e:
                    print(f"Error appending data to Excel: {e}")
                
                return JsonResponse({"message": "Node post created and data saved to Excel and database"}, status=201)
            else:
                return JsonResponse({"error": "Node not found"}, status=404)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)


    

@api_view(['PUT'])
def update_node_data(request, node_id):
    if request.method == 'PUT':
        try:
            data = JSONParser().parse(request)
            new_gateway_id = data.get('gateway_id')
            new_data_field = data.get('data_field')

            if not new_gateway_id or not new_data_field:
                return JsonResponse({"message": "gateway_id and data_field are required"}, status=status.HTTP_400_BAD_REQUEST)

            if not isinstance(new_data_field,dict):
                return JsonResponse({"error": "Invalid data_field format. Must be a dictionary."}, status=status.HTTP_400_BAD_REQUEST)

            try:
                node = Node.objects.get(nodeid=node_id)
            except Node.DoesNotExist:
                return JsonResponse({"message": "Node not found"}, status=status.HTTP_404_NOT_FOUND)

            node_models = NodeModel.objects.filter(node_id=node, gateway_id=new_gateway_id)

            if not node_models.exists():
                return JsonResponse({"message": "NodeModel with the given node_id and gateway_id not found"}, status=status.HTTP_404_NOT_FOUND)

            for node_model in node_models:
                node_model.data_field = new_data_field
                node_model.save()

            return JsonResponse({"message": "NodeModel updated successfully"}, status=status.HTTP_200_OK)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def delete_node_data(request, node_id):
    try:
        node_model = NodeModel.objects.get(node_id=node_id)
    except NodeModel.DoesNotExist:
        return JsonResponse({"message": "NodeModel not found"}, status=status.HTTP_404_NOT_FOUND)

    node_model.delete()
    return JsonResponse({"message": "NodeModel deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
