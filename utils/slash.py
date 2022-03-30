from discord_slash.utils.manage_commands import create_choice, create_option

from utils import config


poll_options = [
    create_option(
        name='poll_title',
        description='poll title',
        required=True,
        option_type=3
    ),
    create_option(
        name='poll_description',
        description='description of the poll',
        required=True,
        option_type=3
    ),
    create_option(
        name='option_1',
        description='the first option for the poll',
        required=True,
        option_type=3
    ),
    create_option(
        name='option_2',
        description='the second option for the poll',
        required=True,
        option_type=3
    ),
    create_option(
        name='option_3',
        description='the third option for the poll',
        required=False,
        option_type=3
    ),
    create_option(
        name='option_4',
        description='the fourth option for the poll',
        required=False,
        option_type=3
    ),
    create_option(
        name='option_5',
        description='the fifth option for the poll',
        required=False,
        option_type=3
    ),
    create_option(
        name='option_6',
        description='the sixth option for the poll',
        required=False,
        option_type=3
    )]

scoreboard_options = create_option(
    name='stat',
    required=True,
    option_type=3,
    description='stat',
    choices=[
        create_choice(
            name='damage taken',
            value='damage taken'
        ),
        create_choice(
            name='damage dealt',
            value='damage dealt'
        ),
        create_choice(
            name='deaths',
            value='deaths'
        ),
        create_choice(
            name='kills',
            value='kills'
        )
    ]
)

scoreboard_show_all = create_option(
    name='show_all',
    required=False,
    option_type=5,
    description='show all players'
)

server_prefix = create_option(
    name='server_prefix',
    required=True,
    option_type=3,
    description='server prefix'
)

server_name = create_option(
    name='server_name',
    required=True,
    option_type=3,
    description='server name'
)

server_logo = create_option(
    name='server_logo',
    required=True,
    option_type=3,
    description='link to server logo'
)

server_colour = create_option(
    name='server_colour',
    required=True,
    option_type=3,
    description='in game colour',
    choices=[
        create_choice(
            name='Dark Red',
            value='dark_red',
        ),
        create_choice(
            name='red',
            value='red',
        ),
        create_choice(
            name='Gold',
            value='gold'
        ),
        create_choice(
            name='Yellow',
            value='yellow'
        ),
        create_choice(
            name='Dark Green',
            value='dark_green'
        ),
        create_choice(
            name='Green',
            value='green'
        ),
        create_choice(
            name='Aqua',
            value='aqua'
        ),
        create_choice(
            name='Dark Aqua',
            value='dark_aqua'
        ),
        create_choice(
            name='Dark Blue',
            value='dark_blue'
        ),
        create_choice(
            name='Blue',
            value='blue'
        ),
        create_choice(
            name='Light Purple',
            value='light_purple'
        ),
        create_choice(
            name='Dark Purple',
            value='dark_purple'
        ),
        create_choice(
            name='White',
            value='white'
        ),
        create_choice(
            name='Gray',
            value='gray'
        ),
        create_choice(
            name='Dark Gray',
            value='dark_gray'
        ),
        create_choice(
            name='Black',
            value='black'
        )
    ]
)

server_discord_colour = create_option(
    name='discord_colour',
    required=True,
    option_type=3,
    description='discord colour, please use hex'
)

servers = create_option(
    name='server',
    required=True,
    option_type=3,
    description='server',
    choices=[create_choice(name=team, value=team) for team in config.teams]
)

ign = create_option(
    name='ign',
    description='player\'s ign',
    required=True,
    option_type=3
)
