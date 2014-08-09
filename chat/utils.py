from werkzeug.exceptions import NotFound


def get_object_or_404(model, **kwargs):
    instance = model.query.filter_by(**kwargs).first()
    if not instance:
        raise NotFound()
    return instance


def get_or_create(session, model, **kwargs):
    instance = model.query.filter_by(**kwargs).first()
    if instance:
        return instance, False
    else:
        instance = model(**kwargs)
        session.add(instance)
        session.commit()
        return instance, True


def init_db(app, db):
    db.create_all(app=app)
