#netbox_access_lists | tickets
#accesslist_list | tickets

from extras.plugins import PluginConfig

class NetBoxAccessListsConfig(PluginConfig):
    # name = 'tickets'
    name = 'tickets_plugin'
    verbose_name = ' NetBox Access Lists'
    description = 'Manage simple ACLs in NetBox'
    version = '0.1'
    base_url = 'access-lists'

config = NetBoxAccessListsConfig