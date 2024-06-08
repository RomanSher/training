from django.db.models import Count, F, QuerySet


def product_sorting(queryset: QuerySet, sort_field: str, sort_type: str) -> QuerySet:
    """
    Сортирует QuerySet в соответствии с указанными параметрами и типом сортировки.
    :param queryset: QuerySet.
    :param sort_field: Поле сортировки.
    :param sort_type: Тип сортировки.
    :return: QuerySet.
    """
    if sort_field == 'reviews':
        if sort_type == 'dec':
            return queryset.annotate(reviews_count=Count('review')).order_by('reviews_count')
        else:
            return queryset.annotate(reviews_count=Count('review')).order_by('-reviews_count')
    else:
        if sort_type == 'dec':
            sort_field = F(sort_field).asc(nulls_last=True)
        else:
            sort_field = F(sort_field).desc(nulls_last=True)
        return queryset.order_by(sort_field)
