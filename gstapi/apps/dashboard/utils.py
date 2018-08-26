from django.shortcuts import reverse
from django.db.models.fields.reverse_related import ManyToOneRel
from apps.accounts.models import User
from apps.core.constants import database_keys as dk

class TableData:

    fields = []
    rows = []

    def __init__(self):
        self.meta = {}
        self.fields = []
        self.available_fields = []
        self.enabled_fields = []
        self.sortable_fields = []
        self.rows = []

    def addRow(self, id):
        self.rows.append({
            "id": id,
            "data": [],
            "actions": []
        })

    def addCellToRow(self, rowIndex, cell_type, text, subtext=None, meta=None):
        self.rows[rowIndex]['data'].append({
            "type": cell_type,
            "text": text,
            "subtext": subtext,
            "meta": meta
        })

    def addActionButtonToRow(self, rowIndex, url, label, btn_class):
        self.rows[rowIndex]['actions'].append({
            'url': url,
            'label': label,
            'btn_class': btn_class
        })

    def addField(self, field, label, field_class=None):
        self.fields.append({
            "name": field,
            "class": field_class,
            "label": label
        })
        self.enabled_fields.append(field)

    def addAvailableField(self, field, field_label):
        self.available_fields.append({
            "name": field,
            "label": field_label
        })
    
    def addSortableField(self, field, field_label):
        self.sortable_fields.append({
            "name": field,
            "label": field_label
        })
    
    def addMetaField(self, key, value):
        self.meta[key] = value

    def getObject(self):
        return {
            "fields": self.fields,
            "available_fields": self.available_fields,
            "enabled_fields": self.enabled_fields,
            "sortable_fields": self.sortable_fields,
            "rows": self.rows,
            "meta": self.meta
        }

def getTableDataForUsers(enabled_columns = None, search=None, sort_by = None, sort_order=None, start=-1, end=-1):
    t = TableData()
    users = User.filter_user_data(
        search = search, 
        sort_by = sort_by, 
        sort_order = sort_order,
        start = start,
        end = end)

    if search != None:
        t.addMetaField("search", search)

    if sort_by != None:
        t.addMetaField("sorted_by", sort_by)
        t.addMetaField("sort_order", sort_order)

    if enabled_columns == None:
        t.addField("avatar","...", "w-1")
        t.addField("first_name", "First Name")
        t.addField("last_name", "Last Name")
        t.addField("email", "Email")
    else:
        for col in enabled_columns:
            field = User._meta.get_field(col)
            if field.name == "avatar":
                label = "..."
            else:
                label = field.verbose_name
            t.addField(field.name, label)

    ignored_fields = ['password', 'groups', 'user_permissions', 'is_superuser']
    non_sortable_fields = ignored_fields + ['avatar']
    for field in User._meta.get_fields():
        if type(field) != ManyToOneRel:
            if field.name not in ignored_fields:
                t.addAvailableField(field.name, field.verbose_name)
            if field.name not in non_sortable_fields:
                t.addSortableField(field.name, field.verbose_name)
        

    counter = 0
    for user in users:
        t.addRow(user.id)

        if enabled_columns == None:

            t.addCellToRow(counter, "avatar", "", "", {"url": user.avatar.url if user.avatar else ""})
            t.addCellToRow(counter, 'text', user.first_name)
            t.addCellToRow(counter, 'text', user.last_name)
            t.addCellToRow(counter, "text-secondary", user.email)
        else:
            for col in enabled_columns:
                field = User._meta.get_field(col)
                param = {}
                cell_type = ""
                text = ""
                subtext = ""
                if field.name == "avatar":
                    param = { "url": user.avatar.url if user.avatar else ""}
                    cell_type = "avatar"
                else:
                    text = getattr(user, field.name)
                    cell_type = "text"

                t.addCellToRow(counter, cell_type, text, subtext, param)        

        t.addActionButtonToRow(counter, reverse('dashboard:edit-user', args=[user.id]), "Edit", "btn-secondary")
        
        if user.is_active:
            t.addActionButtonToRow(counter, reverse('dashboard:suspend-user', args=[user.id]), "Suspend", "btn-danger")
        else:
            t.addActionButtonToRow(counter, reverse('dashboard:enable-user', args=[user.id]), "Enable", "btn-primary")

        counter += 1

    return t.getObject()