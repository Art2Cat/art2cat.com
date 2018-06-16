import json

from flask import render_template, session, url_for, flash, request
from flask_login import login_required, login_user, logout_user, current_user
from werkzeug.exceptions import abort
from werkzeug.utils import redirect

from app import db
from app.email import send_email
from app.admin.forms import LoginForm, RegistrationForm, PasswordResetRequestForm, PasswordResetForm, ChangeEmailForm, \
    ChangePasswordForm, PostForm
from app.models import Post, User, Permission
from app.admin import admin


@admin.route('/', methods=['GET'])
@login_required
def admin_view():
    return


@admin.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            return redirect(request.args.get('next') or url_for('main.index'))
        flash('Invalid username or password.')
    return render_template('admin/login.html', form=form)


@admin.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User()
        user.email = form.email.data,
        user.username = form.username.data,
        user.password = form.password.data
        db.session.add(user)
        flash('You can now login.')
        return redirect(url_for('admin.login'))
    return render_template('admin/register.html', form=form)


@admin.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('main.index'))


@admin.route('/create-post', methods=['GET', 'POST'])
@login_required
def create_post():
    post = Post()
    form = PostForm()
    # form.set_tag_list(['test', 'test'])

    if form.validate_on_submit():
        print("done")
        post.body = form.body.data
        db.session.add(post)
        db.session.commit()
        flash('The post has been created.')
        return redirect(url_for('main.post', id=post.id))
        # post.tags = form.tags
        # posts = json.dumps(post)
        # session['posts'] = posts
        # return redirect(url_for('/post', posts=posts))

    else:
        return render_template('admin/create_post.html', form=form)


@admin.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    post = Post.query.get_or_404(id)
    if current_user != post.author and not current_user.can(Permission.ADMIN) and \
            not current_user.can(Permission.MODERATE):
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.body = form.body.data
        db.session.add(post)
        db.session.commit()
        flash('The post has been updated.')
        return redirect(url_for('.post', id=post.id))
    form.body.data = post.body
    return render_template('admin/edit_post.html', form=form)


@admin.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.old_password.data):
            current_user.password = form.password.data
            db.session.add(current_user)
            db.session.commit()
            flash('Your password has been updated.')
            return redirect(url_for('main.index'))
        else:
            flash('Invalid password.')
    return render_template("admin/change_password.html", form=form)


@admin.route('/reset', methods=['GET', 'POST'])
def password_reset_request():
    if not current_user.is_anonymous:
        return redirect(url_for('main.index'))
    form = PasswordResetRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            token = user.generate_reset_token()
            send_email(user.email, 'Reset Your Password',
                       'admin/email/reset_password',
                       user=user, token=token,
                       next=request.args.get('next'))
        flash('An email with instructions to reset your password has been '
              'sent to you.')
        return redirect(url_for('admin.login'))
    return render_template('admin/reset_password.html', form=form)


@admin.route('/reset/<token>', methods=['GET', 'POST'])
def password_reset(token):
    if not current_user.is_anonymous:
        return redirect(url_for('main.index'))
    form = PasswordResetForm()
    if form.validate_on_submit():
        if User.reset_password(token, form.password.data):
            db.session.commit()
            flash('Your password has been updated.')
            return redirect(url_for('admin.login'))
        else:
            return redirect(url_for('main.index'))
    return render_template('admin/reset_password.html', form=form)


@admin.route('/change_email', methods=['GET', 'POST'])
@login_required
def change_email_request():
    form = ChangeEmailForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.password.data):
            new_email = form.email.data
            token = current_user.generate_email_change_token(new_email)
            send_email(new_email, 'Confirm your email address',
                       'admin/email/change_email',
                       user=current_user, token=token)
            flash('An email with instructions to confirm your new email '
                  'address has been sent to you.')
            return redirect(url_for('main.index'))
        else:
            flash('Invalid email or password.')
    return render_template("admin/change_email.html", form=form)


@admin.route('/change_email/<token>')
@login_required
def change_email(token):
    if current_user.change_email(token):
        db.session.commit()
        flash('Your email address has been updated.')
    else:
        flash('Invalid request.')
    return redirect(url_for('main.index'))
