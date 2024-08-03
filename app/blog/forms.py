from flask_wtf import FlaskForm
from wtforms import HiddenField, StringField, SubmitField, TextAreaField
from wtforms.validators import InputRequired, Length

from config import Config


class AddCommentForm(FlaskForm):
    author = StringField(
        "Name",
        validators=[InputRequired(), Length(max=Config.DB_CONFIGS["LENMAX_COMMENT_AUTHOR"])]
    )
    parent = HiddenField(
        default=None
    )
    content = TextAreaField(
        "Comment",
        validators=[InputRequired(), Length(max=Config.DB_CONFIGS["LENMAX_COMMENT_CONTENT"])]
    )
    add_comment_form_submit = SubmitField(
        "Submit"
    )


class ReplyCommentButton(FlaskForm):
    reply_comment_button_submit = SubmitField(
        "Reply"
    )


class DeleteCommentButton(FlaskForm):
    delete = SubmitField(
        "Delete",
        render_kw={"data-confirm-submit": ""}
    )
