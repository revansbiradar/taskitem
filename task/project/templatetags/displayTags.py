from django import template
register = template.Library()


def grouped(l, n):
    # Yield successive n-sized chunks from l.
    for i in xrange(0, len(l), n):
        yield l[i:i+n]


@register.filter(name='group_by')
def group_by(value, arg):
    return grouped(value, arg)


