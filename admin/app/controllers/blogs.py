from typing import List, Optional

from app import db
from app.models.blog import Blog, BlogCategory, BlogTag
from app.utils.error import handle_exception


def create_blog(
    title: str,
    description: str,
    content: str,
    category_id: int,
    tags: List[int],
) -> Optional[Blog]:
    try:
        blog = Blog.create_instance(
            title=title,
            description=description,
            content=content,
            category_id=category_id,
            tag_ids=tags,
        )
        db.session.add(blog)
        db.session.commit()
        return blog.to_dict()
    except Exception as e:
        handle_exception(e, "Blog already exists")


def update_blog(
    blog_id: int,
    title: Optional[str] = None,
    description: Optional[str] = None,
    content: Optional[str] = None,
    category_id: Optional[int] = None,
    tags: Optional[List[int]] = None,
) -> Optional[Blog]:
    try:
        blog = Blog.get_by_id(blog_id=blog_id)
        if title:
            blog.title = title
        if description:
            blog.description = description
        if content:
            blog.content = content
        if category_id:
            blog.category_id = category_id
        if tags:
            blog.tags = [BlogTag.get_by_id(tag_id) for tag_id in tags]
        db.session.commit()
        return blog.to_dict()
    except Exception as e:
        handle_exception(e, "Blog does not exist")


def delete_blog(blog_id: int):
    try:
        blog = Blog.get_by_id(blog_id=blog_id)
        db.session.delete(blog)
        db.session.commit()
    except Exception as e:
        handle_exception(e, "Blog does not exist")


def get_blog(blog_id: int) -> Optional[Blog]:
    try:
        return Blog.get_by_id(blog_id=blog_id).to_dict()
    except Exception as e:
        handle_exception(e, "Blog does not exist")


def get_all_blogs(
    limit: Optional[int] = None,
    offset: Optional[int] = None,
) -> Optional[List[Blog]]:
    try:
        return [blog.to_dict() for blog in Blog.get_all(limit=limit, offset=offset)]
    except Exception as e:
        handle_exception(e, "Blog does not exist")


def get_all_blogs_by_category(
    category_id: int,
    limit: Optional[int] = None,
    offset: Optional[int] = None,
) -> Optional[List[Blog]]:
    try:
        blogs = Blog.get_all_by_category(
            category_id=category_id,
            limit=limit,
            offset=offset,
        )
        return [blog.to_dict() for blog in blogs]
    except Exception as e:
        handle_exception(e, "Blog does not exist")


def get_all_blogs_by_tag(
    tag_id: int,
    limit: Optional[int] = None,
    offset: Optional[int] = None,
) -> Optional[List[Blog]]:
    try:
        blogs = Blog.get_all_by_tag(
            tag_id=tag_id,
            limit=limit,
            offset=offset,
        )
        return [blog.to_dict() for blog in blogs]
    except Exception as e:
        handle_exception(e, "Blog does not exist")


def create_blog_category(
    name: str,
    description: str,
) -> Optional[BlogCategory]:
    try:
        category = BlogCategory.create_instance(
            name=name,
            description=description,
        )
        db.session.add(category)
        db.session.commit()
        return category.to_dict()
    except Exception as e:
        handle_exception(e, "Category already exists")


def update_blog_category(
    id: int,
    name: Optional[str] = None,
    description: Optional[str] = None,
) -> Optional[BlogCategory]:
    try:
        category = BlogCategory.get_by_id(category_id=id)
        if name:
            category.name = name
        if description:
            category.description = description
        db.session.commit()
        return category.to_dict()
    except Exception as e:
        handle_exception(e, "Category does not exist")


def delete_blog_category(id: int):
    try:
        category = BlogCategory.get_by_id(category_id=id)
        db.session.delete(category)
        db.session.commit()
    except Exception as e:
        handle_exception(e, "Category does not exist")


def get_all_categories(
    limit: Optional[int] = None,
    offset: Optional[int] = None,
) -> Optional[List[BlogCategory]]:
    try:
        categories = BlogCategory.get_all(limit=limit, offset=offset)
        return [category.to_dict() for category in categories]
    except Exception as e:
        handle_exception(e, "Categories do not exist")


def create_blog_tag(
    name: str,
    description: str,
) -> Optional[BlogTag]:
    try:
        tag = BlogTag.create_instance(
            name=name,
            description=description,
        )
        db.session.add(tag)
        db.session.commit()
        return tag.to_dict()
    except Exception as e:
        handle_exception(e, "Tag already exists")


def update_blog_tag(
    id: int,
    name: Optional[str] = None,
    description: Optional[str] = None,
) -> Optional[BlogTag]:
    try:
        tag = BlogTag.get_by_id(tag_id=id)
        if name:
            tag.name = name
        if description:
            tag.description = description
        db.session.commit()
        return tag.to_dict()
    except Exception as e:
        handle_exception(e, "Tag does not exist")


def delete_blog_tag(id: int):
    try:
        tag = BlogTag.get_by_id(tag_id=id)
        db.session.delete(tag)
        db.session.commit()
    except Exception as e:
        handle_exception(e, "Tag does not exist")


def get_all_tags(
    limit: Optional[int] = None,
    offset: Optional[int] = None,
) -> Optional[List[BlogTag]]:
    try:
        tags = BlogTag.get_all(limit=limit, offset=offset)
        return [tag.to_dict() for tag in tags]
    except Exception as e:
        handle_exception(e, "Tags do not exist")
