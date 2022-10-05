import re


def parse_point(post: {}) -> dict: # return {'pk': 'changed_point'}
    points = {}

    for p in post:
        pk = re.search(r'\d+', p)

        if pk is not None:
            pk = pk[0]
            points.update({int(pk): post[p]})
    return points

