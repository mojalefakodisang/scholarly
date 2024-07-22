"""Module that have utils for content models
"""


def obj_create(obj, **kwargs):
    return obj.objects.create(**kwargs)


def obj_all(obj):
    return obj.objects.all()


def obj_by_subj(obj, val, **kwargs):
    args = val.split()

    if len(args) == 1:
        if args[0] == 'first':
            return obj.objects.filter(**kwargs).first()
        elif args[0] == 'all':
            return obj.objects.filter(**kwargs).all()
    elif len(args) > 1:
        first = args[0]
        last = args[1]
        if first == 'first' and last is not None:
            return obj.objects.filter(**kwargs).order_by(last).first()
        elif first == 'all' and last is not None:
            return obj.objects.filter(**kwargs).order_by(last).all()
    
    return None