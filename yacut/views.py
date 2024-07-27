from flask import flash, redirect, render_template

from . import app, db
from .forms import URLForm
from .models import URLMap
from .utils import generate_random_string


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = URLForm()
    generated_short_url = None
    if form.validate_on_submit():
        original_url = form.original.data
        short_url = form.short.data

        if short_url:
            url_map = URLMap.query.filter_by(short=short_url).first()
            if url_map:
                flash('Предложенный вариант короткой ссылки уже существует.')
                return render_template('index.html', form=form, generated_short_url=None)

            url_map = URLMap(original=original_url, short=short_url)
            db.session.add(url_map)
            db.session.commit()
            generated_short_url = short_url
        else:
            short_url = generate_random_string()
            while URLMap.query.filter_by(short=short_url).first():
                short_url = generate_random_string()
            url_map = URLMap(original=original_url, short=short_url)
            db.session.add(url_map)
            db.session.commit()
            generated_short_url = short_url
        #
        # flash(f'Короткая ссылка: {generated_short_url}')
        return render_template('index.html', form=form, generated_short_url=generated_short_url)
    return render_template('index.html', form=form, generated_short_url=None)

@app.route('/<short_id>')
def redirect_to_original(short_id):
    url_map_object = URLMap.query.filter_by(short=short_id).first_or_404()
    return redirect(url_map_object.original, code=302)
