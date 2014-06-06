''' A helper function for retrieving a specific item from the given model that
    will raise a 404 error if not found in the DB'''
def exist_or_404(Model, id):
    item = Model.query.get(id)
    if item:
        return item
    abort(404, 'Entry not found in %s with id: %s' % (Model.__tablename__, id))
