from extras.plugins import PluginConfig

class NetBox_TicketsListsConfig(PluginConfig):
    name = 'ticket_firewall'
    verbose_name = 'Ticket Firewall'
    description = 'this description'
    version = '0.00000001'
    base_url = 'tickets-plug'

#устанавливает
config = NetBox_TicketsListsConfig
