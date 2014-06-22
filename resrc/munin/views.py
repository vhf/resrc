from munin.helpers import muninview
from resrc.link.models import Link
from resrc.list.models import List


@muninview(config="""graph_title Total Links graph_vlabel links""")
def total_links(request):
    return [("links",Link.objects.all().count())]


@muninview(config="""graph_title Total Lists graph_vlabel lists""")
def total_lists(request):
    return [("lists",List.objects.all().count()),
            ("private",List.objects.all().filter(is_public=False).count()),
            ("public",List.objects.all().filter(is_public=True).count())]
