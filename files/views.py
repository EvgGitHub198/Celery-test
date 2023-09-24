from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import File
from .serializers import FileSerializer
from .tasks import process_uploaded_file


class FileViewSet(viewsets.ModelViewSet):
    queryset = File.objects.all()
    serializer_class = FileSerializer

    def create(self, request, *args, **kwargs):
        file_obj = request.data.get('file')

        if file_obj:
            file = File(file=file_obj)
            file.save()
            process_uploaded_file.apply_async(args=(file.id,))
            serializer = self.get_serializer(file)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response({'error': 'No file provided'}, status=status.HTTP_400_BAD_REQUEST)
