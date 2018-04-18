from django_airavata.app_config import AiravataAppConfig

class DashboardConfig(AiravataAppConfig):
    name = 'django_airavata.apps.resourceallocation'
    label = 'django_airavata_resourceallocation'
    verbose_name = 'Resource Allocation'
    url_app_name = label
    app_order = 0
    url_home = 'dashboard:index'
    fa_icon_class = 'fa-flask'
    app_description = """
        Launch applications and manage your experiments and projects.
    """

