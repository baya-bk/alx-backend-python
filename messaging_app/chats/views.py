from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import User, Conversation, Message
from .serializers import UserSerializer, ConversationSerializer, MessageSerializer

class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer

    def create(self, request, *args, **kwargs):
        """
        Create a new conversation with participants.
        Expects a list of participant user_ids in request.data['participants'].
        """
        participants_ids = request.data.get('participants', [])
        if not participants_ids:
            return Response({"error": "Participants list required"}, status=status.HTTP_400_BAD_REQUEST)

        conversation = Conversation.objects.create()
        conversation.participants.set(participants_ids)
        conversation.save()

        serializer = self.get_serializer(conversation)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

    def create(self, request, *args, **kwargs):
        """
        Send a new message in a conversation.
        Expects 'sender' user_id, 'conversation' id, and 'message_body' in request.data.
        """
        sender_id = request.data.get('sender')
        conversation_id = request.data.get('conversation')
        message_body = request.data.get('message_body')

        if not all([sender_id, conversation_id, message_body]):
            return Response({"error": "sender, conversation, and message_body are required"},
                            status=status.HTTP_400_BAD_REQUEST)

        message = Message.objects.create(
            sender_id=sender_id,
            conversation_id=conversation_id,
            message_body=message_body
        )

        serializer = self.get_serializer(message)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
