from api import dbo, auth, logger
from api.mutations import mutation
from api.queries import query
from bson import ObjectId
from datetime import datetime    


class CRUD:
    def __init__(self, collection, auth_level):
        self.collection = collection
        self.auth_level = auth_level

        self.create = (auth(self.auth_level))(self.create)
        mutation.set_field(f"create_{self.collection}", self.create)

        self.update = (auth(self.auth_level))(self.update)
        mutation.set_field(f"update_{self.collection}", self.update)

        self.delete = (auth(self.auth_level))(self.delete)
        mutation.set_field(f"delete_{self.collection}", self.delete)

        self.get_list = (auth(self.auth_level))(self.get_list)
        query.set_field(f"get_{self.collection}_list", self.get_list)

        self.get_item = (auth(self.auth_level))(self.get_item)
        query.set_field(f"get_{self.collection}_item", self.get_item)

    def create(self, *args, **kwargs):
        _id = ObjectId(kwargs.get("_id"))
        kwargs["input"].update(
            {
                "created_by": kwargs["user"].dbref,
                "created_at": datetime.utcnow().timestamp(),
                "_id": _id
            }
        )

        dbo.insert_one(kwargs.get('collection', self.collection), kwargs.get("input", {}))
        return _id

    def update(self, *args, **kwargs):
        _id = ObjectId(kwargs.get("_id"))
        kwargs["input"].update(
            {
                "edited_by": kwargs["user"].dbref,
                "updated_at": datetime.utcnow().timestamp(),
            }
        )
        dbo.update_one(
            kwargs.get('collection', self.collection),
            {"_id": _id},
            {"$set": kwargs.get("input", {})},
        )
        # return _id

    def delete(self, *args, **kwargs):
        dbo.delete_one(kwargs.get('collection', self.collection), {"_id": ObjectId(kwargs.get("_id"))})

    def get_list(self, *args, **kwargs):
        return dbo.find_many(kwargs.get('collection', self.collection), ref=True)

    def get_item(self, *args, **kwargs):
        return dbo.find_one(kwargs.get('collection', self.collection), {"_id": ObjectId(kwargs.get("_id"))}, ref=True)


class SSPR(CRUD):
    """
    # Base class for mutations pattern
    S[tart], S[top], P[ause] and R[esume].

    All the mutations are defined as (function_{alias}), and need has the same authenticate level
    """

    def __init__(self, alias, auth_level, **kwargs):
        if kwargs.get("collection"):
            super().__init__(**kwargs, auth_level=auth_level)
        self.alias = alias
        self.auth_level = auth_level

        self.start = (auth(self.auth_level))(self.start)
        mutation.set_field(f"start_{self.alias}", self.start)

        self.stop = (auth(self.auth_level))(self.stop)
        mutation.set_field(f"stop_{self.alias}", self.stop)

        self.pause = (auth(self.auth_level))(self.pause)
        mutation.set_field(f"pause_{self.alias}", self.pause)

        self.resume = (auth(self.auth_level))(self.resume)
        mutation.set_field(f"resume_{self.alias}", self.resume)

        self.select = (auth(self.auth_level))(self.select)
        mutation.set_field(f"select_{self.alias}", self.select)

    def start(self, *args, **kwargs):
        raise TypeError("start not implemented")

    def stop(self, *args, **kwargs):
        raise TypeError("stop not implemented")

    def pause(self, *args, **kwargs):
        raise TypeError("pause not implemented")

    def resume(self, *args, **kwargs):
        raise TypeError("resume not implemented")

    def select(self, *args, **kwargs):
        raise TypeError("resume not implemented")
