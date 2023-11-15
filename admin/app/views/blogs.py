from flask import (
    blueprints,
    request,
    jsonify,
)

from app.utils.auth import token_required
from app.controllers.blogs import (
    create_blog,
    get_all_blogs,
    get_blog,
    update_blog,
    delete_blog,
    create_blog_category,
    get_all_categories,
    update_blog_category,
    delete_blog_category,
    create_blog_tag,
    get_all_tags,
    update_blog_tag,
    delete_blog_tag,
)


blog = blueprints.Blueprint("blog", __name__, url_prefix="/api/blog")


@blog.route("/all", methods=["GET"])
def get_all():
    return jsonify(get_all_blogs())


@blog.route("/<int:blog_id>", methods=["GET"])
def get(blog_id: int):
    return jsonify(get_blog(blog_id=blog_id))


@blog.route("/", methods=["POST"])
@token_required
def create():
    data = request.get_json()
    title = data.get("title")
    description = data.get("description")
    content = data.get("content")
    category_id = data.get("category_id")
    tags = data.get("tags")
    blog = create_blog(
        title,
        description,
        content,
        category_id,
        tags,
    )
    return jsonify(blog)


@blog.route("/<int:blog_id>", methods=["PUT"])
@token_required
def update(blog_id: int):
    data = request.get_json()
    title = data.get("title")
    description = data.get("description")
    content = data.get("content")
    category_id = data.get("category_id")
    tags = data.get("tags")
    updated_blog_dict = update_blog(
        blog_id=blog_id,
        title=title,
        description=description,
        content=content,
        category_id=category_id,
        tags=tags,
    )
    return jsonify(updated_blog_dict)


@blog.route("/<int:blog_id>", methods=["DELETE"])
@token_required
def delete(blog_id: int):
    delete_blog(blog_id)
    return jsonify({"message": "Blog deleted successfully"})


@blog.route("/category/all", methods=["GET"])
def get_all_categories_route():
    return jsonify(get_all_categories())


@blog.route("/category", methods=["POST"])
@token_required
def create_category():
    data = request.get_json()
    name = data.get("name")
    description = data.get("description")
    category = create_blog_category(name, description)
    return jsonify(category)


@blog.route("/category/<int:category_id>", methods=["PUT"])
@token_required
def update_category(category_id: int):
    data = request.get_json()
    name = data.get("name")
    description = data.get("description")
    updated_category_dict = update_blog_category(
        category_id=category_id,
        name=name,
        description=description,
    )
    return jsonify(updated_category_dict)


@blog.route("/category/<int:category_id>", methods=["DELETE"])
@token_required
def delete_category(category_id: int):
    delete_blog_category(category_id)
    return jsonify({"message": "Category deleted successfully"})


@blog.route("/tag/all", methods=["GET"])
def get_all_tags_route():
    return jsonify(get_all_tags())


@blog.route("/tag", methods=["POST"])
@token_required
def create_tag():
    data = request.get_json()
    name = data.get("name")
    description = data.get("description")
    tag = create_blog_tag(name, description)
    return jsonify(tag)


@blog.route("/tag/<int:tag_id>", methods=["PUT"])
@token_required
def update_tag(tag_id: int):
    data = request.get_json()
    name = data.get("name")
    description = data.get("description")
    updated_tag_dict = update_blog_tag(
        tag_id=tag_id,
        name=name,
        description=description,
    )
    return jsonify(updated_tag_dict)


@blog.route("/tag/<int:tag_id>", methods=["DELETE"])
@token_required
def delete_tag(tag_id: int):
    delete_blog_tag(tag_id)
    return jsonify({"message": "Tag deleted successfully"})
