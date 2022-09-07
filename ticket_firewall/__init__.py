from extras.plugins import PluginConfig

class NetBox_TicketsListsConfig(PluginConfig):
    name = 'ticket_firewall'
    verbose_name = 'Firewall Tickets'
    description = 'this description'
    version = '0.00000001'
    base_url = 'ticket-firewall'

#устанавливает
config = NetBox_TicketsListsConfig
