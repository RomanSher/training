from telebot.handler_backends import State, StatesGroup


class UserState(StatesGroup):

  """ Класс для сохранения пользовательского состояния """

  city = State()
  hotel = State()
  date_1 = State()
  date_2 = State()
  photo = State()
  minPrice = State()
  maxPrice = State()
  minDist = State()
  maxDist = State()
  sending = State()
  filter = [hotel, minPrice, maxPrice, minDist, maxDist]



