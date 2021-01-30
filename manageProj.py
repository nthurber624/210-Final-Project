from flask import render_template, redirect, request, url_for, Blueprint, flash
from flask_login import login_required, current_user
from app import db
from forms import GoalForm, UpdateForm, EditGoal, EditUpdate

proj = Blueprint('proj', __name__)

@proj.route('/goals', methods=['POST', 'GET'])
@login_required
def viewGoals():
    from tables import Goal, User
    form = GoalForm()
    if request.method == 'POST' and form.validate_on_submit():
        goalContent = form.content.data
        newGoal = Goal(content=goalContent, contributorID=current_user.id)
        db.session.add(newGoal)
        db.session.commit()
        form.content.data = ''
        return redirect(url_for('proj.viewGoals'))
    goals = Goal.query.filter(Goal.completed == False)
    completed = Goal.query.filter(Goal.completed == True)
    users = User.query.order_by(User.dateCreated)
    return render_template('project/goals.html', goals=goals, completed=completed, goalForm=form, users=users)

@proj.route('/delete/goal/<int:id>')
@login_required
def deleteGoal(id):
    from tables import Goal
    deleteGoal = Goal.query.get_or_404(id)
    try:
        db.session.delete(deleteGoal)
        db.session.commit()
        return redirect(url_for('proj.viewGoals'))
    except:
        return "Couldn't delete the goal"

@proj.route('/edit/goal/<int:id>', methods=['POST', 'GET'])
@login_required
def editGoal(id):
    from tables import Goal
    goal = Goal.query.get_or_404(id)
    form = EditGoal(newContent=goal.content)
    if request.method == 'POST' and form.validate_on_submit():
        goal.content = form.newContent.data
        try:
            db.session.commit()
            return redirect(url_for('proj.viewGoals'))
        except:
            return "Couldn't edit the goal"
    return render_template('project/edit_goal.html', form=form)

@proj.route('/complete/goal/<int:id>')
@login_required
def completeGoal(id):
    from tables import Goal
    goal = Goal.query.get_or_404(id)
    try:
        status = goal.completed
        goal.completed =  not status
        db.session.commit()
        return redirect(url_for('proj.viewGoals'))
    except:
        return "Couldn't complete the goal"

@proj.route('/updates', methods=['POST', 'GET'])
@login_required
def viewUpdates():
    from tables import Update, User
    form = UpdateForm()
    if request.method == 'POST' and form.validate_on_submit():
        updateContent = form.content.data
        newUpdate = Update(content=updateContent, contributorID=current_user.id)
        db.session.add(newUpdate)
        db.session.commit()
        form.content.data = ''
        return redirect(url_for('proj.viewUpdates'))
    updates = Update.query.order_by(Update.dateCreated)
    users = User.query.order_by(User.dateCreated)
    return render_template('project/updates.html', updates=updates, updateForm=form, users=users)

@proj.route('/delete/update/<int:id>')
@login_required
def deleteUpdate(id):
    from tables import Update
    deleteUpdate = Update.query.get_or_404(id)
    try:
        db.session.delete(deleteUpdate)
        db.session.commit()
        return redirect(url_for('proj.viewUpdates'))
    except:
        return "Couldn't delete the update"

@proj.route('/edit/update/<int:id>', methods=['POST', 'GET'])
@login_required
def editUpdate(id):
    from tables import Update
    update = Update.query.get_or_404(id)
    form = EditUpdate(newContent=update.content)
    if request.method == 'POST' and form.validate_on_submit():
        update.content = form.newContent.data
        try:
            db.session.commit()
            return redirect(url_for('proj.viewUpdates'))
        except:
            return "Couldn't edit the update"
    return render_template('project/edit_update.html', form=form)