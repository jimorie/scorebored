from aioli.exceptions import NoMatchFound
from aioli.service import BaseService
from aioli_rdbms import DatabaseService
from pymysql.err import IntegrityError

from ..exceptions import ConflictException


class DatabaseModelService(BaseService):
    db = None
    db_model = None
    db_model_name = None

    async def set_db_model(self, db_model):
        """
        Register database model.
        """
        self.db_model = db_model
        self.db_model_name = self.db_model.__tablename__.split("__")[-1]
        self.db = self.integrate(DatabaseService).use_model(self.db_model)

    async def get_one(self, pk):
        """
        Return a single entry of the used model or raise an exception.

        :param pk: Primary key of the Model entry to get
        :return: Single Model object
        """

        return await self.db.get_one(pk=pk)

    async def find_one(self, **query):
        """
        Return a single entry of the used model that matches the query, or raise an exception.

        :param query: Query parameters
        :return: Single Model object
        """

        return await self.db.get_one(**query)

    async def get_many(self, **query):
        """
        Return a list of zero or more entries of the used model.

        :param query: Query parameters
        :return: List of zero or more Model objects
        """

        return await self.db.get_many(**query)

    async def delete(self, pk):
        """
        Delete an entry of the used model.

        :param pk: Primary key of the Model entry to delete
        """

        try:
            return await self.db.delete(pk)
        except IntegrityError:
            raise ConflictException(
                f"That {self.db_model_name} cannot be deleted since it is actively used"
            )

    async def delete_many(self, **query):
        """
        Deletes all matching entries of the used model.

        :param query: Query parameters
        """

        self.log.info(f"Query is: {query}")
        try:
            for result in await self.db.get_many(**query):
                await result.delete()
        except IntegrityError:
            raise ConflictException(
                f"At least one {self.db_model_name} cannot be deleted since it is actively used"
            )

    async def update(self, pk, payload):
        """
        Update an entry of the used model.

        :param pk: Primary key of the Model entry to update
        :param payload: Updated entry data
        :return: The updated Model object
        """

        return await self.db.update(pk, payload)

    async def create(self, payload):
        """
        Create a new entry of the used model.

        :param payload: Entry data
        :return: The created Model object
        """

        async with self.db.manager.database.transaction():
            obj = await self.db.create(**payload)
            self.log.info(f"New {self.db_model_name}: {obj}")
            return obj


class NamedDatabaseModelService(DatabaseModelService):
    db_name_field = None

    async def set_db_name_field(self, db_name_field):
        """
        Register db model name field
        """
        self.db_name_field = db_name_field

    async def get_or_create(self, payload):
        """
        Get an existing entry of the used model with a `db_name_field` matching that
        of the payload, otherwise create it.

        :param payload: Entry data
        :return: The found or created Model object
        """
        self.log.info(f"Creating {self.db_model_name}")
        self.log.info(payload)

        try:
            return await self.db.get_one(
                **{self.db_name_field: payload[self.db_name_field]}
            )
        except NoMatchFound:
            return await self.create(payload)
