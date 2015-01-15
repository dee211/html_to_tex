# -*- coding: utf-8 -*-
updating_values = {
    'text-decoration',
    'table-parent',
}


class StyleStorage(object):
    def __init__(self, style_dict, config):
        self.values = style_dict
        self.changes = []
        self.config = config

    def less_priority_update_item(self, item, value):
        item = item if item in self.config.value_updaters else 'other'
        self.values[item] = self.config.value_updaters[item].merge_styles(value, self.values.get(item, None))

    def merge_parent(self, parent_storage):
        inherited_items = [item for item in parent_storage.values.iterkeys() if item in self.config.inherited_styles]
        self.merge(parent_storage, inherited_items)

    def merge(self, storage, keys=None):
        for item in (storage.values.iterkeys() if keys is None else keys):
            self.less_priority_update_item(item, storage.values[item])