from  rest_framework import serializers

from note.models import Note


class GetNoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = '__all__'


class AddNoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = ['title', 'description']

    def save(self, **kwargs):
        note = Note(user=self.context.get('user'),
                    title=self.validated_data['title'],
                    description=self.validated_data['description'])
        note.save()
        return note