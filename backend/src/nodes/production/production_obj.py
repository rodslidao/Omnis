from datetime import datetime, timedelta
from bson import ObjectId


class ProductionOBJ:
    """
    A class thats format a process execution time and status to be stored in an NoSQL database.]

    Properties:\n
    \t_id: Unique identifier for the process.\n
    \tcreateAt: Date and time when the process data was created.\n
    \texpireAt: Date and time when the process data will expire from database.\n
    \tmodel: Flag to group and identity different process.\n
    \tstatus: Flag to identify if the process was successful or not.\n
    \tprocess_seconds: Time in seconds that the process took to execute.\n
    \n
    methods:\n
    \tstart: Overwrite 'createAt' with actual utc timestamp.\n
    \tfinish: Calculate 'process_seconds' and 'expireAt'. Overwrite 'status' and 'model' flags.\n
    \n
    Notes:\n
    \t'process_seconds' is a float value calculated when 'finish' is called.\n
    \t'finish(model, status)' must be called to finish the process and is a magic method that returns a dict representation of the process.\n
    \t'expireAt': is calculated suming the 'expire_delay' keys with 'createAt'.\n
    \t'expire_delay' is a dict with the following keys:\n
    \t\t\tseconds: Number of seconds to add to 'createAt' to calculate 'expireAt'.\n
    \t\t\tminutes: Minutes to add to 'createAt' to calculate 'expireAt'.\n
    \t\t\thours: Hours to add to 'createAt' to calculate 'expireAt'.\n
    \t\t\tdays: Days to add to 'createAt' to calculate 'expireAt'.\n
    \t\t\tweeks: Weeks to add to 'createAt' to calculate 'expireAt'.\n
    \t\t\tmonths: Months to add to 'createAt' to calculate 'expireAt'.\n
    \t\t\tyears: Years to add to 'createAt' to calculate 'expireAt'.\n
    \t'createAt' is a datetime object created when a new instance of this class is created.\n

    """

    def __init__(self, expire_delay={"minutes": 0.5}) -> None:
        self.process_seconds = None
        self.date = datetime.utcnow()
        self._id = ObjectId()
        self.st = datetime.utcnow()
        self.delay = expire_delay

    def start(self):
        """
        Overwrite 'createAt' with actual utc timestamp.
        """
        self.st = datetime.utcnow()

    def finish(self, model=None, status=False):
        """
        Calculate: 'process_seconds' and 'expireAt'.
        Overwrite: 'status' and 'model' flags.
        Returns: a dict representation of the process.
        """
        self.model = model
        self.status = status
        self.expire = self.date + timedelta(**self.delay)
        return self()

    def __call__(self):
        return {
            "_id": self._id,
            "createAt": self.date,
            "expireAt": self.expire,
            "model": self.model,
            "status": self.status,
            "process_seconds": (datetime.utcnow() - self.st).total_seconds(),
        }
