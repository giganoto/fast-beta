from datetime import datetime
from typing import Any, Dict, List, Optional

from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    DateTime,
    Table,
    ForeignKey,
)
from sqlalchemy.orm import relationship, validates, Mapped
from slugify import slugify

from app import db
from app.utils.error import GiganotoException


NAME_MAX_LENGTH = 80
TITLE_MAX_LENGTH = 80
DESCRIPTION_MAX_LENGTH = 160

length_mapping = {
    "name": NAME_MAX_LENGTH,
    "title": TITLE_MAX_LENGTH,
    "description": DESCRIPTION_MAX_LENGTH,
}


class BlogCategory(db.Model):
    """
    Represents a category for a blog in the database.

    Attributes:
        id (int): The unique identifier for the blog category.
        name (str): The name of the category.
        description (str): A brief description of what the category entails.
        created_at (datetime): The date and time when the category was created.

    Methods:
        get_by_id: Fetch a single blog category by its unique identifier.
        get_all: Retrieve all categories, optionally with limits and offsets.
        create_instance: Create a new instance of BlogCategory.
    """

    __tablename__ = "blog_categories"

    id: int = Column(Integer, autoincrement=True, primary_key=True)
    name: str = Column(String(NAME_MAX_LENGTH), nullable=False, unique=True)
    description: str = Column(String(DESCRIPTION_MAX_LENGTH), nullable=False)
    created_at: datetime = Column(DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        """Provide a string representation of the BlogCategory instance."""
        return f"<BlogCategory(name={self.name}, " f"description={self.description})>"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "created_at": self.created_at.strftime('%a, %d %b %Y %H:%M:%S GMT'),
        }

    @validates("name", "description")
    def validates_required(self, key, value):
        if not value:
            raise GiganotoException(f"Category {key} cannot be empty")
        if len(value) > length_mapping[key]:
            raise GiganotoException(f"Category {key} cannot be longer than {length_mapping[key]} characters")
        elif len(value) == 0:
            raise GiganotoException(f"Category {key} cannot be empty")
        return value

    @classmethod
    def get_by_id(cls, id: int) -> "BlogCategory":
        """
        Fetch a single blog category by its ID.

        Args:
            id (int): The unique identifier of the category.

        Returns:
            BlogCategory: The category corresponding to the given id.
        """
        return cls.query.filter_by(id=id).first()

    @classmethod
    def get_all(
        cls, limit: Optional[int] = None, offset: Optional[int] = None
    ) -> List["BlogCategory"]:
        """
        Retrieve all blog categories with optional pagination.

        Args:
            limit (Optional[int]): The maximum number of categories to return.
            offset (Optional[int]): The offset at which to start the query.

        Returns:
            List[BlogCategory]: A list of BlogCategory instances.
        """
        query = cls.query
        if limit is not None:
            query = query.limit(limit)
        if offset is not None:
            query = query.offset(offset)
        return query.all()

    @classmethod
    def create_instance(cls, name: str, description: str) -> "BlogCategory":
        """
        Create a new blog category instance.

        Args:
            name (str): The name of the new category.
            description (str): A brief description of the new category.

        Returns:
            BlogCategory: A new instance of BlogCategory.
        """
        instance = cls(name=name, description=description)
        return instance


class BlogTag(db.Model):
    """
    Represents a tag associated with blog posts in the database.

    Attributes:
        id (int): The unique identifier for the blog tag.
        name (str): The name of the tag.
        description (str): A brief description of what the tag represents.
        created_at (datetime): The date and time when the tag was created.

    Methods:
        get_by_id: Fetches a single tag based on its ID.
        get_all: Retrieves all tags, suports pagination using limit and offset.
        create_instance: Creates a new instance of BlogTag.
    """

    __tablename__ = "blog_tags"

    id: int = Column(Integer, autoincrement=True, primary_key=True)
    name: str = Column(String(NAME_MAX_LENGTH), nullable=False, unique=True)
    description: str = Column(String(DESCRIPTION_MAX_LENGTH), nullable=False)
    created_at: datetime = Column(DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        """Represent the BlogTag instance as a string."""
        return f"<BlogTag(name={self.name}, description={self.description})>"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "created_at": self.created_at.strftime('%a, %d %b %Y %H:%M:%S GMT'),
        }

    @validates("name", "description")
    def validates_required(self, key, value):
        if not value:
            raise GiganotoException(f"Tag {key} cannot be empty")
        if len(value) > length_mapping[key]:
            raise GiganotoException(f"Tag {key} cannot be longer than 80 characters")
        elif len(value) == 0:
            raise GiganotoException(f"Tag {key} cannot be empty")
        return value

    @classmethod
    def get_by_id(cls, id: int) -> "BlogTag":
        """
        Fetch a single blog tag by its unique ID.

        Args:
            id (int): The ID of the blog tag to be retrieved.

        Returns:
            BlogTag: The blog tag object if found, else None.
        """
        return cls.query.filter_by(id=id).first()

    @classmethod
    def get_all(
        cls, limit: Optional[int] = None, offset: Optional[int] = None
    ) -> List["BlogTag"]:
        """
        Fetch all blog tags, with options for pagination.

        Args:
            limit (Optional[int]): The maximum number of tags to return.
            offset (Optional[int]): The starting point for the query results.

        Returns:
            List[BlogTag]: A list of blog tags.
        """
        query = cls.query
        if limit is not None:
            query = query.limit(limit)
        if offset is not None:
            query = query.offset(offset)
        return query.all()

    @classmethod
    def create_instance(cls, name: str, description: str) -> "BlogTag":
        """
        Create and return a new instance of BlogTag.

        Args:
            name (str): The name of the tag.
            description (str): The description of the tag.

        Returns:
            BlogTag: A new instance of BlogTag.
        """
        return cls(name=name, description=description)


# Association table for many-to-many relationship between Blog and BlogTag
blog_tags_association = Table(
    "blog_tags_association",
    db.metadata,
    Column("blog_id", Integer, ForeignKey("blogs.id")),
    Column("tag_id", Integer, ForeignKey("blog_tags.id")),
)


class Blog(db.Model):
    """Represents a blog post in the database.

    Attributes:
        id (int): The unique identifier for the blog post.
        title (str): The title of the blog post.
        description (str): A brief description or summary of the blog post.
        content (str): The full content of the blog post.
        category_id (int): The foreign key linking to the blog post's category.
        category (BlogCategory): The category of the blog post.
        tags (List[BlogTag]): A list of tags associated with the blog post.
        created_at (datetime): The date and time when the blog was created.

    Methods:
        url_from_title: Returns a URL-friendly version of the blog title.
        get_by_id: Fetches a single blog post by its ID.
        get_all: Retrieves all blog posts, supports pagination.
        get_by_category: Fetches blog posts by category, supports pagination.
        get_by_tag: Fetches blog posts filtered by tag, supports pagination.
        create_instance: Creates a new instance of Blog with given details.
    """

    __tablename__ = "blogs"

    id: int = Column(Integer, autoincrement=True, primary_key=True)
    title: str = Column(String(TITLE_MAX_LENGTH), nullable=False)
    description: str = Column(String(DESCRIPTION_MAX_LENGTH), nullable=False)
    content: str = Column(Text, nullable=False)
    is_draft: bool = Column(db.Boolean, default=True)
    category_id: int = Column(Integer, ForeignKey("blog_categories.id"))
    category: Mapped[BlogCategory] = relationship("BlogCategory")
    tags: Mapped[BlogTag] = relationship("BlogTag", secondary=blog_tags_association)
    created_at: datetime = Column(DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        """Represent the Blog instance as a string."""
        return f"<Blog(title={self.title}, description={self.description})>"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "content": self.content,
            "is_draft": self.is_draft,
            "category": self.category.to_dict(),
            "tags": [tag.to_dict() for tag in self.tags],
            "created_at": self.created_at.strftime('%a, %d %b %Y %H:%M:%S GMT'),
        }

    @validates("title", "description", "content", "is_draft", "category", "tags")
    def validates_required(self, key, value):
        if value is None or value == "":
            raise GiganotoException(f"Blog {key} cannot be empty")
        if key in length_mapping and len(value) > length_mapping[key]:
            raise GiganotoException(f"Blog {key} cannot be longer than {length_mapping[key]} characters")
        elif key in length_mapping and len(value) == 0:
            raise GiganotoException(f"Blog {key} cannot be empty")
        return value

    def url_from_title(self) -> str:
        """Generate a URL-friendly version of the blog title.

        Returns:
            str: A slugified version of the blog title suitable for URLs.
        """
        return slugify(self.title)

    @classmethod
    def get_by_id(cls, id: int) -> Optional["Blog"]:
        """Fetch a single blog post by its ID.

        Args:
            id (int): The ID of the blog post.

        Returns:
            Optional[Blog]: The blog post with the ID, or None if not found.
        """
        return cls.query.filter_by(id=id).first()

    @classmethod
    def get_all(
        cls, limit: Optional[int] = None, offset: Optional[int] = None
    ) -> List["Blog"]:
        """Fetch all blog posts, with optional pagination.

        Args:
            limit (Optional[int]): The maximum number of blog posts to return.
            offset (Optional[int]): The offset from where to start.

        Returns:
            List[Blog]: A list of blog posts.
        """
        query = cls.query
        if limit is not None:
            query = query.limit(limit)
        if offset is not None:
            query = query.offset(offset)
        return query.all()

    @classmethod
    def get_all_by_category(
        cls,
        category_id: int,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
    ) -> List["Blog"]:
        """Fetch blog posts filtered by category, with optional pagination.

        Args:
            category_id (int): The ID of the category to filter by.
            limit (Optional[int]): The maximum number of blog posts to return.
            offset (Optional[int]): The offset from where to start.

        Returns:
            List[Blog]: A list of blog posts in the specified category.
        """
        query = cls.query.filter_by(category_id=category_id)
        if limit is not None:
            query = query.limit(limit)
        if offset is not None:
            query = query.offset(offset)
        return query.all()

    @classmethod
    def get_all_by_tag(
        cls,
        tag_id: int,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
    ) -> List["Blog"]:
        """Fetch blog posts filtered by tag, with optional pagination.

        Args:
            tag_id (int): The ID of the tag to filter by.
            limit (Optional[int]): The maximum number of blog posts to return.
            offset (Optional[int]): The offset from where to start.

        Returns:
            List[Blog]: A list of blog posts associated with the specified tag.
        """
        query = cls.query.join(BlogTag, Blog.tags).filter(BlogTag.id == tag_id)
        if limit is not None:
            query = query.limit(limit)
        if offset is not None:
            query = query.offset(offset)
        return query.all()

    @classmethod
    def create_instance(
        cls,
        title: str,
        description: str,
        content: str,
        is_draft: bool,
        category_id: int,
        tag_ids: List[int],
    ) -> "Blog":
        """Create a new blog post instance.

        Args:
            title (str): The title of the blog post.
            description (str): A brief description of the blog post.
            content (str): The full content of the blog post.
            category_id (int): The ID of the category for this blog post.
            tag_ids (List[int]): A list of tag IDs associated with the blog.

        Returns:
            Blog: A new instance of Blog with the specified details.
        """
        tags = BlogTag.query.filter(BlogTag.id.in_(tag_ids)).all()
        blog_instance = cls(
            title=title,
            description=description,
            content=content,
            is_draft=is_draft,
            category_id=category_id,
            tags=tags,
        )
        return blog_instance
