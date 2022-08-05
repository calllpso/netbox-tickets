from extras.plugins import PluginMenuItem, PluginMenuButton
from utilities.choices import ButtonColorChoices

ticketlist_buttons = [
    PluginMenuButton(
        link='plugins:tickets_plugin:ticketlist_add',
        title='Add',
        icon_class='mdi mdi-plus-thick',
        color=ButtonColorChoices.GREEN
    )
]

# accesslistrule_butons = [
#     PluginMenuButton(
#         link='plugins:tickets_plugin:accesslistrule_add',
#         title='Add',
#         icon_class='mdi mdi-plus-thick',
#         color=ButtonColorChoices.GREEN
#     )
# ]

menu_items = (
    PluginMenuItem(
        link='plugins:tickets_plugin:ticketlist_list',
        link_text='Tickets',
        buttons=ticketlist_buttons
    ),
    PluginMenuItem(
        link='plugins:tickets_plugin:rule_list',
        link_text='Ticket Rules',
        # buttons=accesslistrule_butons
    ),
)

