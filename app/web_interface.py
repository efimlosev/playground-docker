from lru import *
from os import environ
from flask import Flask, render_template, flash, request
from wtforms import Form, StringField, validators, StringField, SubmitField
DEBUG = True
app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = environ['SECRET_KEY']

class ReusableForm(Form):
    name = StringField('Word:', validators=[validators.input_required()])

@app.route("/", methods=['GET', 'POST'])
def hello():
    dictionary = Dictionary()

    form = ReusableForm(request.form)


    if request.method == 'POST':
        word = request.form['name']

    if form.validate():
        # Save the comment here.
        try:
            entry, source, duration = dictionary.search(word)
            flash(entry)
            flash(f"Found in {source}")
            flash(f"Duration  {duration}")
        except Exception as e:
            flash(f"Error when searching: {str(e)}\n")
    else:
        flash('All the form fields are required. ')

    return render_template('hello.html', form=form)
if __name__ == '__main__':
    # main()
    app.run(host='0.0.0.0', port=5000)
    # d = OxfordDictionary()
    # d.search("cat")
