from extras.plugins import PluginMenuItem, PluginMenuButton
from utilities.choices import ButtonColorChoices

from extras.plugins import PluginMenuItem, PluginMenuButton
# from netbox.navigation_menu import Menu, MENUS

ticketlist_buttons = [
    PluginMenuButton(
        link='plugins:ticket_firewall:ticket_add',
        title='Add',
        icon_class='mdi mdi-plus-thick',
        color=ButtonColorChoices.GREEN
    )
]

menu_items = (
    PluginMenuItem(
        link='plugins:ticket_firewall:ticket_list',
        link_text='Tickets',
        buttons=ticketlist_buttons
    ),
    PluginMenuItem(
        link='plugins:ticket_firewall:rule_list',
        link_text='Ticket Rules',
    ),
)

# n = Menu(
#         label="Firewall tickets",
#         icon_class="mdi mdi-lock-open-check",
#         groups=menu_items
#     )

# MENUS.append(n)