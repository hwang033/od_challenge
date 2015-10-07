from geojson import Point, FeatureCollection, Feature, dumps
from django.http import HttpResponse
from django.views.decorators.gzip import gzip_page
from django.views.decorators.http import require_http_methods
from listings.models import Listings
from utils.custom_decorators import add_header
from utils.tools import custom_pagination

PARAM_DIC = {
    'min_price': 'price__gte',
    'max_price': 'price__lte',
    'min_bed': 'bedrooms__gte',
    'max_bed': 'bedrooms__lte',
    'min_bath': 'bathrooms__gte',
    'max_bath': 'bathrooms__lte',
}

@gzip_page
@require_http_methods(["GET"])
@add_header('Content-Type', 'application/json')
def get_listings(request):

    # processing parameters
    pdic = {}
    for key, sql_filter in PARAM_DIC.items():
        param = request.GET.get(key, None)
        if param is not None and param.isdigit():
            pdic[sql_filter] = int(param)

    # construct queryset
    records = Listings.objects.filter(**pdic)
    paged_records, link_header = custom_pagination(request, records)

    # transform to geojson
    features = []
    for rcd in paged_records:
        feature = Feature(geometry=Point(rcd.get_geom()),
                          properties=rcd.get_properties())
        features.append(feature)

    rst_geojson = dumps(FeatureCollection(features))
    res = HttpResponse(rst_geojson)

    # add header for prev/next links
    res['Link'] = link_header
    return res
