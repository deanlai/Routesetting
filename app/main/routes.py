from flask import render_template, flash, redirect, url_for, request, current_app
from app import db
from app.main import bp
from app.main.forms import EditProfileForm, ProblemForm
from flask_login import current_user, login_required
from app.models import User, Problem


@bp.route('/', methods=['GET', 'POST'])
@bp.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    form = ProblemForm()
    if form.validate_on_submit():
        problem = Problem(grade=form.grade.data,
                          color=form.color.data,
                          risk=form.risk.data,
                          intensity=form.intensity.data,
                          complexity=form.complexity.data,
                          setter=current_user)
        db.session.add(problem)
        db.session.commit()
        flash('Your problem has been recorded!')
        return redirect(url_for('main.index'))
    problems = current_user.followed_problems().all()
    return render_template('index.html', title='Index', problems=problems, form=form)


@bp.route('/explore')
@login_required
def explore():
    problems = Problem.query.order_by(Problem.timestamp.desc()).all()
    return render_template('index.html', title='Explore', problems=problems)


@bp.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    problems = Problem.query.filter_by(user_id=user.id)
    return render_template(
        'user.html', title=username, user=user, problems=problems)


@bp.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('main.edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='Edit Profile',
                           form=form)


@bp.route('/follow/<username>')
@login_required
def follow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('User {} not found.'.format(username))
        return redirect(url_for('main.index'))
    if user == current_user:
        flash('You cannot follow yourself!')
        return redirect(url_for('main.user', username=username))
    current_user.follow(user)
    db.session.commit()
    flash('You are following {}!'.format(username))
    return redirect(url_for('main.user', username=username))


@bp.route('/unfollow/<username>')
@login_required
def unfollow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('User {} not found.'.format(username))
        return redirect(url_for('main.index'))
    if user == current_user:
        flash('You cannot unfollow yourself!')
        return redirect(url_for('main.user', username=username))
    current_user.unfollow(user)
    db.session.commit()
    flash('You are not following {}.'.format(username))
    return redirect(url_for('main.user', username=username))
