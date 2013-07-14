from .models import Tag

import djadmin2

from mptt.admin import MPTTModelAdmin


djadmin2.default.register(Tag, MPTTModelAdmin)
