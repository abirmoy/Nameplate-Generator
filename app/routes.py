# -*- coding: utf-8 -*-
"""
# Created on Wed Nov  6 09:50:24 2019

# @author: Abirmoy - qxz0ga0
# """
import os
from datetime import datetime
from flask import render_template, flash, redirect, url_for, request
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.urls import url_parse
from app import app, db
from app.forms import LoginForm, RegistrationForm, EditProfileForm
# from app.forms import DeviceRegistrationForm
# from app.forms import DeviceEditForm

from app.models import User
from app.models import Device

from flask_uploads import UploadSet, configure_uploads, IMAGES, patch_request_class
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, \
    TextAreaField, SelectField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, \
    Length
from app.models import User
from app.models import Device

from flask_uploads import UploadSet, configure_uploads, IMAGES, patch_request_class
from flask_wtf.file import FileField, FileRequired, FileAllowed
from app import app





background_dictionary = {'bg1id':'bg1_bj.jpg','bg2id':'bg2_sh.jpg','bg3id':'deffault.jpg'}





photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)
patch_request_class(app)  # set maximum file size, default is 16MB

class DeviceRegistrationForm(FlaskForm):
    deviceId = StringField('Device ID', validators=[DataRequired()])
    devicename = StringField('Device Name', validators=[DataRequired()])
    name = StringField('Name', validators=[DataRequired()])
    dept_code = StringField('Dept. Code', validators=[DataRequired()])
    device_function = StringField('Function', validators=[DataRequired()])
    device_bg=SelectField('Select Background', choices=[('bg3id', 'Default'), ('bg1id', 'Day'), ('bg2id', 'Night'), ])
    # device_image = # HAVE TO LET USER UPLOAD IMAGE OF THE DEVICE
    photo = FileField(validators=[FileAllowed(photos, 'Image only!')])
    submit = SubmitField('Save')

    def validate_deviceId(self, deviceId):
        deviceid = Device.query.filter_by(deviceId=deviceId.data).first()
        if deviceid is not None:
            raise ValidationError('Please use a different Device ID.')
class DeviceEditForm(FlaskForm):
    # deviceId = StringField('Device ID', validators=[DataRequired()])
    devicename = StringField('Device Name', validators=[DataRequired()])
    name = StringField('Name', validators=[DataRequired()])
    dept_code = StringField('Dept. Code', validators=[DataRequired()])
    device_function = StringField('Function', validators=[DataRequired()])
    device_bg=SelectField('Select Background', choices=[('bg1id', 'Day'), ('bg2id', 'Night'), ('bg3id', 'Default')])
    
    # device_image = # HAVE TO LET USER UPLOAD IMAGE OF THE DEVICE    
    submit = SubmitField('Update')

class ChangePhotoForm(FlaskForm):
    photo = FileField(validators=[FileAllowed(photos, 'Image only!')])
    submit = SubmitField('Update')













@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()


@app.route('/')
@app.route('/index')
# @login_required
def index():    
    return render_template('index.html', title='Home')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
# @login_required
def register():
    # if current_user.is_authenticated:
    #     return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you added a new registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/user/<username>')
# @login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    posts = [
        {'author': user, 'body': 'Test post #1'},
        {'author': user, 'body': 'Test post #2'}
    ]
    print(user)
    return render_template('user.html', user=user, posts=posts)


@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='Edit Profile',
                           form=form)


@app.route('/register_device', methods=['GET', 'POST'])
# @login_required
def register_device():
    form = DeviceRegistrationForm()
    if form.validate_on_submit():
        if form.photo.data == None:
            # photo_name = ''
            device = Device(deviceId=form.deviceId.data, 
            devicename=form.devicename.data, 
            name=form.name.data, dept_code=form.dept_code.data, 
            device_function=form.device_function.data, 
            device_bg=form.device_bg.data)  
        else:
            photo_name = photos.save(form.photo.data)
        # file_url = photos.url(photo_name)
            device = Device(deviceId=form.deviceId.data, 
            devicename=form.devicename.data, 
            name=form.name.data, dept_code=form.dept_code.data, 
            device_function=form.device_function.data, 
            device_bg=form.device_bg.data, photo=photo_name)        
        db.session.add(device)
        db.session.commit()
        flash('Congratulations, your Nameplate is in the system!\nThe URL of your nameplate: /device/'+str(form.deviceId.data))
        new_device_info = Device.query.filter_by(deviceId=form.deviceId.data).first_or_404()
        # bg_pic=background_dictionary[deviceId.device_bg]
        return render_template('new_device.html', deviceId=new_device_info) 
    return render_template('register_device.html', title='Add New Device', form=form)



@app.route('/device/<deviceId>')
def device(deviceId):
    deviceId = Device.query.filter_by(deviceId=deviceId).first_or_404()
    # print(deviceId.device_bg)
    bg_pic=background_dictionary[deviceId.device_bg]
    # print(bg_pic)
    print('current_user:',current_user)
    return render_template('device.html', deviceId=deviceId, bg_pic=bg_pic)



@app.route('/edit_device/<deviceId>', methods=['GET', 'POST'])
@login_required
def edit_device(deviceId):
    form = DeviceEditForm()
    device_query = Device.query.filter_by(deviceId = deviceId ).first()
    old_photo = device_query.photo
    if form.validate_on_submit():        
        device_query.devicename=form.devicename.data
        device_query.name=form.name.data
        device_query.dept_code=form.dept_code.data
        device_query.device_function=form.device_function.data
        device_query.device_bg = form.device_bg.data        
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('device',deviceId=deviceId))
    elif request.method == 'GET':        
        form.devicename.data=device_query.devicename
        form.name.data=device_query.name
        form.dept_code.data=device_query.dept_code
        form.device_function.data=device_query.device_function
        form.device_bg.data = device_query.device_bg
        
    return render_template('edit_device.html', form=form)


@app.route('/delete_device/<deviceId>')
@login_required
def device_delete(deviceId):
    device_query = Device.query.filter_by(deviceId = deviceId ).first()
    old_photo = device_query.photo
    if old_photo != "None" and old_photo != None and old_photo != '':
        os.remove('app/static/uploads/'+ str(old_photo))
    deviceId = Device.query.filter_by(deviceId=deviceId).delete()
    db.session.commit()
    flash('Sucessfully Deleted')
    return redirect(url_for('devices'))


@app.route('/edit_photo/<deviceId>', methods=['GET', 'POST'])
@login_required
def edit_photo(deviceId):
    form = ChangePhotoForm()
    
    device_query = Device.query.filter_by(deviceId = deviceId ).first()
    old_photo = device_query.photo
    
    print('old_photo:', old_photo)
    if form.validate_on_submit():
       
        try:
            device_query.photo = photos.save(form.photo.data)
            if form.photo.data != None and old_photo != None:
                os.remove('app/static/uploads/'+ str(old_photo))
            elif form.photo.data == None and old_photo != "None" and old_photo != None:
                os.remove('app/static/uploads/'+ str(old_photo))
        except TypeError:
            device_query.photo = form.photo.data
            if form.photo.data == None and old_photo != "None" and old_photo != None and old_photo != '':
                os.remove('app/static/uploads/'+ str(old_photo))
            print('form.photo.data', form.photo.data)
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('device',deviceId=deviceId))
    else:
        form.photo.data = device_query.photo
    return render_template('edit_photo.html', form=form)



@app.route('/devices')
def devices():
    all_devices = Device.query.all()
    return render_template('devices.html', devices=all_devices)

