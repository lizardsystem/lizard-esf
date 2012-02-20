# (c) Nelen & Schuurmans.  GPL licensed, see LICENSE.txt.

# Create your views here.
from django.shortcuts import get_object_or_404, render_to_response

from lizard_esf.models import AreaConfiguration
from lizard_area.models import Area
from lizard_esf.models import get_data_main_esf


def esf_overview(request, area_ident):
    """

    """
    area = get_object_or_404(Area, ident=area_ident)

    esf_data = get_data_main_esf(area)

    if request.GET.get('size', None) == 'small':
        template='esf_overview_small.html'
    else:
        template='esf_overview_large.html'


    return render_to_response(
        template,
        {'esfs': esf_data})
