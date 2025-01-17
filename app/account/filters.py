from datetime import datetime, time
import django_filters as filters

import django_filters
from dateutil.relativedelta import relativedelta

from account.models import VendorReviewRating


class DateFilter(django_filters.FilterSet):
    start_date = django_filters.DateFilter(field_name="updated_at", lookup_expr="gte")
    end_date = django_filters.DateFilter(field_name="updated_at", method='filter_end')

    def __init__(self, start_field="updated_at", end_field="updated_at", **kwargs):
        super().__init__(**kwargs)
        self.start_date = django_filters.DateFilter(field_name=start_field, lookup_expr="gte")
        self.end_date = django_filters.DateFilter(field_name=end_field, method='filter_end')

    def filter_end(self, queryset, name, value):
        end_date = datetime.combine(value, time.max)
        f = {f"{name}__lte": end_date}
        return queryset.filter(**f)


class VendorReviewRatingFilter(DateFilter):
    meal_type = filters.CharFilter(lookup_expr="iexact", field_name="transaction__meal_type__name")
    class Meta:
        model = VendorReviewRating
        fields = ['vendor', 'meal_type']

