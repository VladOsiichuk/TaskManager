from desk.api_comments.serializers import CommentSerializer
from desk.model import Desk, Comment


def get_columns_and_users(desk_id, data):
    """
    :param desk_id: id of the desk
    :param data: serialized data about task
    :return: attach users and columns to task data
    """

    desk = Desk.objects.prefetch_related("columns",
                                         "usersdesks_set__user").get(id=desk_id)
    user_data = []
    users = desk.usersdesks_set.all()
    for row in users:
        user_data.append({"user_id": row.user.id,
                     "username": row.user.username,
                     "email": row.user.email})

    column_data = [{"id": row.id, "name": row.name} for row in desk.columns.all()]
    data['columns'] = column_data
    data['users'] = user_data
    return data


def get_comments(data, task_id):
    """
    :param task_id: id of the desk
    :param data: serialized data about task
    :return: attach users and columns to task data
    """
    comments = Comment.objects.select_related("parent__parent__parent", "author").\
        prefetch_related("related_comment__related_comment__related_comment").filter(related_task_id=task_id,
                                                                                     is_child=False)
    data_ser = CommentSerializer(data=comments, many=True)
    data_ser.is_valid()
    data['comments'] = data_ser.data
    return data
