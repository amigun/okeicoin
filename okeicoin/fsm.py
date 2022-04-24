from aiogram.dispatcher.filters.state import State, StatesGroup

class AllStates(StatesGroup):
    main_menu = State()
    get_name = State()
    get_group = State()
    enter_count_of_coins = State()
    enter_pay_account_to_transfer = State()
    enter_count_if_okeicoins = State()
    get_qr_for_getadmin = State()
    send_photo_with_qrc = State()
