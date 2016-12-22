#!/usr/bin/env python
# -*- coding: utf-8 -*-


#from flask.ext.login import LoginManager, login_required


## http://www.patricksoftwareblog.com/tag/flask-uploads/

#~ login_manager = LoginManager()
#~ login_manager.init_app(app)
#~ login_manager.login_view = "users.login"


############################################################
#~ from flask_wtf import Form
#~ from wtforms import StringField
#~ from wtforms.validators import DataRequired
#~ from flask_wtf.file import FileField, FileAllowed, FileRequired


#~ class LicenseRequestForm(Form):
    #~ username = StringField('User', validators=[DataRequired()])
    #~ description = StringField('Description', validators=[DataRequired()])
    #~ license_request = FileField(
        #~ 'License request file',
        #~ validators=[FileRequired(),
                    #~ FileAllowed(license_requests, 'request file (*.request)')])


############################################################

#~ def flash_errors(form):
    #~ for field, errors in form.errors.items():
        #~ for error in errors:
            #~ flash(u"Error in the %s field - %s" % (
                #~ getattr(form, field).label.text,
                #~ error
            #~ ))

#~ @app.route('/new', methods=['GET', 'POST'])
#~ #@login_required
#~ def new_request():
    #~ form = LicenseRequestForm()
    #~ if request.method == 'POST':
        #~ if form.validate_on_submit():
            #~ now = datetime.datetime.now()
            #~ filename = license_requests.save(
                #~ request.files['license_request'],
                #~ folder=now.strftime('%Y%m%d-%H-%M-%S.%f'))
            #~ url = license_requests.url(filename)
            #~ # save to db
            #~ #with open(url, 'rb') as fd:
            #~ #    req = fd.read()
            #~ #db.session.add(req)
            #~ #db.session.commit()
            #~ flash('New request, saved!', 'success')
            #~ return redirect(url_for('recipes.user_recipes'))
        #~ else:
            #~ flash_errors(form)
            #~ flash('ERROR! Request was not added.', 'error')

    #~ return render_template('requestform.html', form=form)
