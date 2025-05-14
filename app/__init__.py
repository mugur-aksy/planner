from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import re
import unicodedata

app = Flask(__name__)
app.config.from_object('config.Config')

db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Пользовательский фильтр для форматирования чисел
def format_currency(value):
    if value is None:
        return "0.00 Р"
    try:
        # Форматируем число с разделителями тысяч и двумя знаками после запятой
        formatted_value = "{:,.2f}".format(float(value)).replace(",", " ")
        return f"{formatted_value} Р"
    except (ValueError, TypeError):
        return "0.00 Р"

# Регистрируем фильтр в Jinja2
app.jinja_env.filters['format_currency'] = format_currency

# Фильтр для преобразования строк в "slug" формат
def slugify(text):
    text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('utf-8')
    text = re.sub(r'[^\w\s-]', '', text).strip().lower()
    return re.sub(r'[-\s]+', '-', text)

# Регистрируем фильтр в Jinja2
app.jinja_env.filters['slugify'] = slugify

from app import routes, models