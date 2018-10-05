from django_airavata.app_config import AiravataAppConfig


class MapToolConfig(AiravataAppConfig):
    name = 'django_airavata.apps.maptool'
    label = 'django_airavata_maptool'
    verbose_name = 'Map Tool'
    url_app_name = label
    app_order = 20
    url_home = url_app_name + ':home'
    fa_icon_class = 'fa-map'
    app_description = """
        SimCCS Map Tool.
    """
