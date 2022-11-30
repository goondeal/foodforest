from django.urls.converters import SlugConverter


class CustomSlugConverter(SlugConverter):
    regex = '[-\w]+' # new regex pattern
