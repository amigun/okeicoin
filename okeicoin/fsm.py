from aiogram.dispatcher.filters.state import State, StatesGroup

class AllStates(StatesGroup):
    main_menu = State()
    get_name = State()
    get_group = State()
    enter_count_of_coins = State()
