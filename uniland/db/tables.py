"""
This module contains the definition of the database tables used in the UniLand system.

The module includes the following classes:
- User: Represents a user in the system.
- Submission: Represents a submission in the system.
- Document: Represents a document submission in the database.

Each class has its own attributes and methods, which are documented in their respective docstrings.
"""

from datetime import datetime

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Enum,
    ForeignKey,
    Integer,
    String,
    Table,
)
from sqlalchemy.orm import declarative_base, relationship

from uniland.utils.enums import DocType, UserLevel

BASE = declarative_base()

bookmarks_association = Table(
    "bookmarks_association",
    BASE.metadata,
    Column("user_id", Integer, ForeignKey("users.user_id")),
    Column("submission_id", Integer, ForeignKey("submissions.id")),
    Column("timestamp", DateTime, default=datetime.utcnow),
)


# TODO! handle ON DELETE cascade in relationships
# When a user is deleted, not null constraint for submissions.owner_id
# will raise error
class User(BASE):
    """
    Represents a user in the system.

    Attributes:
        user_id (int): The ID of the user in Telegram.
        access_level (UserLevel): The access level of the user.
        last_step (str): The last step the user performed.
        signup_date (datetime): The date and time when the user signed up.
        last_active (datetime): The date and time when the user was last active.
        bookmarks (list): The submissions that the user has bookmarked.
    """

    __tablename__ = "users"

    user_id = Column(Integer, nullable=False, primary_key=True)  # user_id in telegram
    access_level = Column(Enum(UserLevel), nullable=False, default=UserLevel.Ordinary)
    last_step = Column(String(50), default="")

    signup_date = Column(DateTime, default=datetime.utcnow)
    last_active = Column(DateTime, default=datetime.utcnow)

    # user_submissions : list -> one-to-many with Submission.owner

    # confirmations : list -> one-to-many with Submission.admin

    # many-to-many with Submission.liked_users
    bookmarks = relationship(
        "Submission",
        secondary=bookmarks_association,
        back_populates="liked_users",
        order_by="bookmarks_association.c.timestamp",
    )

    def __init__(self, user_id, last_step=""):
        self.user_id = user_id
        self.last_step = last_step
        self.access_level = UserLevel.Ordinary

    def __repr__(self):
        return f"User {self.user_id} has access level {self.access_level}"


# ---------------------------------------------------------------------


class Submission(BASE):
    """
    Represents a submission in the system.

    Attributes:
        id (int): The unique identifier of the submission.
        submission_date (datetime): The date and time when the submission was made.
        is_confirmed (bool): Indicates whether the submission has been confirmed.
        owner_id (int): The ID of the user who owns the submission.
        owner (User): The user who owns the submission.
        admin_id (int): The ID of the admin who confirmed the submission.
        admin (User): The admin who confirmed the submission.
        liked_users (list): The list of users who have liked the submission.
        university (str): The university associated with the submission.
        faculty (str): The faculty associated with the submission.
        owner_title (str): The title of the owner of the submission.
        search_text (str): The search text associated with the submission.
        description (str): The description of the submission.
        search_times (int): The number of times the submission has been searched.
        submission_type (str): The type of the submission.

    Methods:
        __init__(owner, is_confirmed, correspondent_admin, university,
            faculty, owner_title, description):
            Initializes a new instance of the Submission class.
        update_search_text():
            Updates the search text of the submission.
        confirm(user):
            Confirms the submission with the specified user as the admin.

    """

    __tablename__ = "submissions"

    id = Column(Integer, nullable=False, primary_key=True, autoincrement=True)
    submission_date = Column(DateTime, default=datetime.utcnow)
    is_confirmed = Column(Boolean, default=False)

    # many-to-one with User.user_submissions
    owner_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    owner = relationship(
        "User",
        backref="user_submissions",
        order_by="Submission.submission_date",
        foreign_keys=[owner_id],
    )

    # many-to-one with User.confirmations
    admin_id = Column(Integer, ForeignKey("users.user_id"), default=None)
    admin = relationship("User", backref="confirmations", foreign_keys=[admin_id])

    # many-to-many with User.bookmarks
    liked_users = relationship(
        "User", secondary=bookmarks_association, back_populates="bookmarks"
    )

    university = Column(String(30))
    faculty = Column(String(30))
    owner_title = Column(String(20))
    search_text = Column(String(200))
    description = Column(String(500))
    search_times = Column(Integer, default=0)

    submission_type = Column(String(20))

    __mapper_args__ = {
        "polymorphic_identity": "submission",
        "polymorphic_on": submission_type,
    }

    def __init__(
        self,
        owner,
        is_confirmed=False,
        correspondent_admin=None,
        university="نامشخص",
        faculty="نامشخص",
        owner_title="ناشناس",
        description="توضیحاتی برای این فایل ثبت نشده است.",
    ):
        self.owner = owner
        self.is_confirmed = is_confirmed
        self.correspondent_admin = correspondent_admin
        self.university = university
        self.faculty = faculty
        self.owner_title = owner_title
        self.description = description

    def update_search_text(self):
        """
        Update the search text for the submission.

        This method is implemented in each subclass of Submission.
        It should not be called from the Submission class directly.
        """
        raise NotImplementedError(
            "This method should not be called from Submission class"
        )

    def confirm(self, user: User):
        """
        Confirms the submission by updating the admin, confirmation status, and search text.

        Args:
            user (User): The user confirming the submission.

        Raises:
            RuntimeError: If the user doesn't have permission to confirm the submission.
        """
        if user is None or user.access_level.value < 2:  # 2 is Editor access
            raise RuntimeError(
                "User doesn't have permission to confirm this submission"
            )
        self.admin = user
        self.is_confirmed = True
        self.update_search_text()


# ---------------------------------------------------------------------


class Document(Submission):
    """
    Represents a document submission in the database.

    Attributes:
        id (int): The unique identifier of the document.
        file_id (str): The ID of the file associated with the document.
        unique_id (str): The unique identifier of the document.
        file_type (DocType): The type of the document.
        course (str): The course associated with the document.
        professor (str): The professor associated with the document.
        writer (str): The writer of the document.
        semester_year (int): The semester year of the document.
    """

    __tablename__ = "documents"

    id = Column(Integer, ForeignKey("submissions.id"), primary_key=True)
    file_id = Column(String(50), nullable=False)
    unique_id = Column(String(50), nullable=False)
    file_type = Column(Enum(DocType), nullable=False)  # Necessary field
    course = Column(String(30), nullable=False)  # Necessary field
    professor = Column(String(30), default="نامشخص")
    writer = Column(String(30), default="نامشخص")
    semester_year = Column(Integer, default=0)

    def __init__(
        self,
        owner,
        file_id,
        unique_id,
        is_confirmed=False,
        correspondent_admin=None,
        university="نامشخص",
        faculty="نامشخص",
        owner_title="ناشناس",
        description="توضیحاتی برای این فایل ثبت نشده است.",
        file_type=DocType.Pamphlet,
        course="نامشخص",
        professor="نامشخص",
        writer="نامشخص",
        semester_year=0,
    ):
        self.owner = owner
        self.is_confirmed = is_confirmed
        self.correspondent_admin = correspondent_admin
        self.university = university
        self.faculty = faculty
        self.owner_title = owner_title
        self.description = description

        self.file_id = file_id
        self.unique_id = unique_id
        self.file_type = file_type
        self.course = course
        self.professor = professor
        self.writer = writer
        self.semester_year = semester_year

    def update_search_text(self) -> None:
        """
        Updates the search_text attribute based on the values of the object's properties.

        The search_text attribute is a string that represents the searchable text
            for the object.
        It includes information about the file type, course, professor,
            writer, semester year, faculty, and university.

        Returns:
            None
        """
        self.search_text = f"{self.file_type.value}"
        if self.course != "نامشخص":
            self.search_text += f" درس {self.course}"
        if self.professor != "نامشخص":
            self.search_text += f" استاد {self.professor}"
        if self.writer != "نامشخص":
            self.search_text += f" نویسنده {self.writer}"
        if self.semester_year != 0:
            self.search_text += f" سال {self.semester_year}"
        if self.faculty != "نامشخص":
            self.search_text += f" دانشکده {self.faculty}"
        if self.university != "نامشخص":
            self.search_text += f" دانشگاه {self.university}"

    def user_display(self) -> str:
        """
        Returns a formatted string representation of the object.

        Returns:
            str: The formatted string representation of the object.
        """
        out = f"نوع فایل: {self.file_type.value}\n"
        if self.course != "نامشخص":
            out += f"درس: {self.course}\n"
        if self.professor != "نامشخص":
            out += f"استاد: {self.professor}\n"
        if self.faculty != "نامشخص":
            out += f"دانشکده: {self.faculty}\n"
        if self.university != "نامشخص":
            out += f"دانشگاه: {self.university}\n"
        if self.writer != "نامشخص":
            out += f"نویسنده: {self.writer}\n"
        if self.semester_year != 0:
            out += f"سال: {self.semester_year}\n"
        if self.owner_title != "ناشناس":
            out += f"نام ثبت کننده: {self.owner_title}\n"
        out += f"توضیحات:\n {self.description}\n"
        out += f"شماره فایل: {self.id}\n"
        return out

    def __repr__(self) -> str:
        """
        Returns a string representation of the object.

        Returns:
            str: A string representation of the object.
        """
        out = f"نوع فایل: {self.file_type.value}\n"
        out += f"درس: {self.course}\n"
        out += f"استاد: {self.professor}\n"
        out += f"دانشکده: {self.faculty}\n"
        out += f"دانشگاه: {self.university}\n"
        out += f"نویسنده: {self.writer}\n"
        out += f"نام ثبت کننده: {self.owner_title}\n"
        out += f"سال: {self.semester_year}\n"
        out += f"توضیحات:\n {self.description}\n"
        return out

    __mapper_args__ = {
        "polymorphic_identity": "document",
    }


# ---------------------------------------------------------------------


class Profile(Submission):
    """
    Represents a user profile.

    Attributes:
        id (int): The unique identifier of the profile.
        title (str): The title of the profile.
        email (str): The email address associated with the profile.
        phone_number (str): The phone number associated with the profile.
        image_id (str): The ID of the profile image.
        is_confirmed (bool): Indicates whether the profile is confirmed.
        correspondent_admin: The correspondent admin for the profile.
        university (str): The university associated with the profile.
        faculty (str): The faculty associated with the profile.
        owner_title (str): The title of the profile owner.
        description (str): The description of the profile.

    Methods:
        __init__: Initializes a new instance of the Profile class.
        update_search_text: Updates the search text for the profile.
        user_display: Returns a formatted string for displaying the profile information.
        __repr__: Returns a string representation of the profile.
    """

    __tablename__ = "profiles"

    id = Column(Integer, ForeignKey("submissions.id"), primary_key=True)
    title = Column(String(200), nullable=False)
    email = Column(String(50), default="")
    phone_number = Column(String(25), default="")
    image_id = Column(String(50), default="")

    def __init__(
        self,
        owner,
        title="",
        email="",
        phone_number="",
        image_id="",
        is_confirmed=False,
        correspondent_admin=None,
        university="نامشخص",
        faculty="نامشخص",
        owner_title="ناشناس",
        description="توضیحاتی برای این مورد ثبت نشده است.",
    ):
        self.is_confirmed = is_confirmed
        self.correspondent_admin = correspondent_admin
        self.university = university
        self.faculty = faculty
        self.owner_title = owner_title
        self.description = description

        self.owner = owner
        self.title = title
        self.email = email
        self.phone_number = phone_number
        self.image_id = image_id

    def update_search_text(self) -> None:
        """
        Updates the search_text attribute based on the title, faculty, and university attributes.

        The search_text attribute is a string that represents the searchable text for the object.
        It is constructed by concatenating the title, faculty, and university attributes with appropriate labels.

        Example:
        If the title is "Computer Science", faculty is "Engineering", and university is "ABC University",
        the search_text will be "اطلاعات Computer Science دانشکده Engineering دانشگاه ABC University".

        Returns:
        None
        """
        self.search_text = f"اطلاعات {self.title}"
        if self.faculty != "نامشخص":
            self.search_text += f" دانشکده {self.faculty}"
        if self.university != "نامشخص":
            self.search_text += f" دانشگاه {self.university}"

    def user_display(self) -> str:
        """
        Returns a formatted string representing the user's information.

        Returns:
            str: Formatted string containing the user's information.
        """
        out = f"عنوان: {self.title}\n"
        if self.email != "":
            out += f"ایمیل: {self.email}\n"
        if self.phone_number != "":

            def f(s):
                return "".join([*s[1:], "+"]) if s[0] == "+" else s

            pretty_phone_number = list(map(f, self.phone_number.split()[::-1]))
            out += f"شماره تماس: {' '.join(pretty_phone_number)}\n"
        if self.faculty != "نامشخص":
            out += f"دانشکده: {self.faculty}\n"
        if self.university != "نامشخص":
            out += f"دانشگاه: {self.university}\n"
        # if self.owner_title != "ناشناس":
        #   out += f'نام ثبت کننده: {self.owner_title}\n'
        out += f"توضیحات:\n {self.description}\n"
        out += f"شماره پروفایل: {self.id}\n"
        return out

    def __repr__(self) -> str:
        """
        Returns a string representation of the object.

        Returns:
            str: A string representation of the object.
        """
        out = f"عنوان: {self.title}\n"
        out += f"ایمیل: {self.email}\n"
        out += f"شماره تماس: {self.phone_number}\n"
        out += f"دانشکده: {self.faculty}\n"
        out += f"دانشگاه: {self.university}\n"
        out += f"نام ثبت کننده: {self.owner_title}\n"
        out += f"توضیحات:\n {self.description}\n"
        return out

    __mapper_args__ = {
        "polymorphic_identity": "profile",
    }


class Media(Submission):
    __tablename__ = "medias"

    id = Column(Integer, ForeignKey("submissions.id"), primary_key=True)
    url = Column(String, nullable=False)
    media_type = Column(String(20), default=None)
    course = Column(String(30), nullable=False)  # Necessary field
    professor = Column(String(30), nullable=False)  # Necessary field
    semester_year = Column(Integer, default=0)

    def __init__(
        self,
        owner,
        url,
        media_type="",
        course="نامشخص",
        professor="نامشخص",
        semester_year=0,
        is_confirmed=False,
        correspondent_admin=None,
        university="نامشخص",
        faculty="نامشخص",
        owner_title="ناشناس",
        description="توضیحاتی برای این فایل ثبت نشده است.",
    ):
        self.owner = owner
        self.is_confirmed = is_confirmed
        self.correspondent_admin = correspondent_admin
        self.university = university
        self.faculty = faculty
        self.owner_title = owner_title
        self.description = description

        self.url = url
        self.media_type = media_type
        self.course = course
        self.professor = professor
        self.semester_year = semester_year

    def update_search_text(self) -> None:
        """
        Updates the search text based on the course, professor, faculty, semester year, and university.
        """
        self.search_text = f"فیلم درس {self.course} استاد {self.professor}"
        if self.faculty != "نامشخص":
            self.search_text += f" دانشکده {self.faculty}"
        if self.semester_year != 0:
            self.search_text += f" سال {self.semester_year}"
        if self.university != "نامشخص":
            self.search_text += f" دانشگاه {self.university}"

    def user_display(self) -> str:
        """
        Returns a formatted string representation of the user's information.

        Returns:
            str: A formatted string containing the user's course, professor, semester year,
                 faculty, university, owner title, description, and ID.
        """
        out = f"عنوان: {self.course} استاد {self.professor}\n"
        if self.semester_year != 0:
            out += f"سال: {self.semester_year}\n"
        if self.faculty != "نامشخص":
            out += f"دانشکده: {self.faculty}\n"
        if self.university != "نامشخص":
            out += f"دانشگاه: {self.university}\n"
        if self.owner_title != "ناشناس":
            out += f"نام ثبت کننده: {self.owner_title}\n"
        out += f"توضیحات:\n {self.description}\n"
        out += f"شماره رسانه: {self.id}\n"
        return out

    def __repr__(self) -> str:
        """
        Returns a string representation of the object.

        Returns:
            str: A string representation of the object.
        """
        out = f"لینک: {self.url}\n"
        out += f"نوع: {self.media_type}\n"
        out += f"درس: {self.course}\n"
        out += f"استاد: {self.professor}\n"
        out += f"سال: {self.semester_year}\n"
        out += f"نام ثبت کننده: {self.owner_title}\n"
        out += f"توضیحات:\n {self.description}\n"
        return out

    __mapper_args__ = {
        "polymorphic_identity": "media",
    }


def create_tables(engine) -> None:
    """
    Create database tables.

    Args:
        engine: SQLAlchemy engine object.

    Returns:
        None
    """
    BASE.metadata.bind = engine
    BASE.metadata.create_all(engine, checkfirst=True)
