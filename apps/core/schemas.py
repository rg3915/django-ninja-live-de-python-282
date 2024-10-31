from ninja import FilterSchema, Field, ModelSchema, Schema
from ninja.orm import create_schema
from typing import Optional

from django.contrib.auth.models import User

from .models import Task


class StatusSchema(Schema):
    status: str


class UserSchema(ModelSchema):
    full_name: str = Field(None, alias='get_full_name')
    username: str = Field(None)

    class Meta:
        model = User
        exclude = ['password', 'last_login', 'date_joined', 'user_permissions', 'groups']


UserSimpleSchema = create_schema(
    User,
    fields=['id', 'username', 'first_name', 'last_name']
)


UserWithGroupSchema = create_schema(
    User,
    depth=1,
    fields=['id', 'username', 'first_name', 'last_name', 'groups'],
    custom_fields=[
        ('get_full_name', str, None)
    ]
)


class TaskSchema(ModelSchema):
    user: UserSchema
    status_display: str

    class Meta:
        model = Task
        fields = ['id', 'title', 'is_completed', 'status']

    @staticmethod
    def resolve_status_display(obj):
        return obj.get_status_display()


class TaskFilterSchema(FilterSchema):
    title: Optional[str] = Field(None, q='title__icontains')
