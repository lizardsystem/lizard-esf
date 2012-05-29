# (c) Nelen & Schuurmans.  GPL licensed, see LICENSE.txt.

# Create your views here.
from django.shortcuts import get_object_or_404, render_to_response

from lizard_map.views import AppView

from lizard_esf.models import (
    AreaConfiguration,
    get_data_main_esf,
)

from lizard_area.models import Area

from lizard_history.utils import (
    get_specific_history,
    get_history,
)


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


class EsfConfigurationHistoryView(AppView):
    """
    Show esf history
    """
    template_name='lizard_esf/esf_history.html'

    def area(self):
        """
        Return an area.
        """
        if not hasattr(self, '_area'):
            self._area = Area.objects.get(
                ident=self.area_ident)
        return self._area

    def history(self):
        """
        Return history.
        """
        if not hasattr(self, '_history'):
            self._history = get_specific_history(
                [AreaConfiguration],
                self.area(),
            )
        return self._history
    
    def get(self, request, *args, **kwargs):
        self.area_ident = request.GET.get('object_id')
        return super(EsfConfigurationHistoryView, self).get(
            request, *args, **kwargs)


class EsfConfigurationArchiveView(AppView):
    """
    Readonly esf tree.
    """
    def history(self):
        """
        Return history.
        """
        if not hasattr(self, '_history'):
            self._history = get_history(
                log_entry_id=self.log_entry_id,
                include_data=True,
            )
        return self._history
    
    def area(self):
        """
        Return an area.
        """
        if not hasattr(self, '_area'):
            self._area = Area.objects.get(
                ident=self.area_ident)
        return self._area

    def get(self, request, *args, **kwargs):
        """
        Return read only form for esf configuration corresponding to
        specific log_entry.
        """
        if request.user.is_authenticated():
            self.template_name = 'lizard_esf/read_only_tree.js'
            self.log_entry_id = kwargs.get('log_entry_id')
            # For the special case of esf trees, the area_ident is
            # stored in the object_repr field of the log_entry.
            self.area_ident = self.history()['object_repr']
        else:
            self.template_name = 'portals/geen_toegang.js'
        return super(
            EsfConfigurationArchiveView,
            self
        ).get(request, *args, **kwargs)
