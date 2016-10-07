from wtforms import SelectMultipleField


class TagsField(SelectMultipleField):

	def pre_validate(self, form):
		pass
