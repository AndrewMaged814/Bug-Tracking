from flask import Blueprint, render_template, request, flash, jsonify, url_for, redirect
from flask_login import login_required, current_user
from werkzeug.exceptions import abort
from .models import User, Project, Bug
from . import db
import json

views = Blueprint('views', __name__)\


@views.route('/')
@login_required
def dashboard():
    issues = Bug.query.all()

    users = User.query.all()

    projects = current_user.projects

    return render_template("dashboard.html", user=current_user, issues=issues, users=users, project=projects)

@views.route('/tickets/<int:project_id>')
@login_required
def project_tickets(project_id):
    # Get the project from the database based on the project_id
    project = Project.query.get(project_id)

    if not project:
        abort(404)

    # Get the tickets associated with the project
    tickets = Bug.query.filter_by(project_id=project.id).all()

    # Filter tickets for each status
    open_tickets = [ticket for ticket in tickets if ticket.status == 'Open']
    in_progress_tickets = [ticket for ticket in tickets if ticket.status == 'In Progress']
    closed_tickets = [ticket for ticket in tickets if ticket.status == 'Closed']

    return render_template('project_tickets.html', user=current_user, project=project,
                            tickets=tickets, open_tickets=open_tickets, 
                            in_progress_tickets=in_progress_tickets, closed_tickets=closed_tickets)

@views.route('/create_issue', methods=['GET', 'POST'])
@login_required
def create_issue():
    if request.method == 'POST':
        # Get the form data submitted by the user
        issue_name = request.form['issueName']
        description = request.form['description']
        status = request.form['status']
        assignee_id = int(request.form['assignee'])
        project_id = int(request.form['project'])

        user = current_user  # Current logged-in user (creator of the issue)
        assignee = User.query.get(assignee_id)
        project = Project.query.get(project_id)


        new_issue = Bug(title=issue_name, description=description, status=status, user=user, project=project)
        new_issue.assignee = assignee  # Set the assignee for the new issue


        db.session.add(new_issue)
        db.session.commit()

        return redirect(url_for('views.dashboard'))

    else:
        #  GET request
        #  pass the necessary data (users and projects) to populate the dropdowns
        users = User.query.all()  
        projects = Project.query.all() 
        issues = Bug.query.all()
        return render_template("create_issue.html", user=current_user, users=users, projects=projects, issue=issues)



@views.route('/update_issue/<int:issue_id>', methods=['GET', 'POST'])
@login_required
def update_issue(issue_id):
    issue = Bug.query.get_or_404(issue_id)

    if request.method == 'POST':
        issue.title = request.form['title']
        issue.description = request.form['description']
        issue.status = request.form['status']

        db.session.commit()

        return redirect(url_for('views.dashboard'))


@views.route('/create_project', methods=['GET', 'POST'])
@login_required
def create_project():
    if request.method == 'POST':
        project_name = request.form['projectName']
        description = request.form['description']

        new_project = Project(name=project_name, description=description, user=current_user)

        db.session.add(new_project)
        db.session.commit()

        return redirect(url_for('views.create_issue'))

    else:
        return render_template("create_project.html", user=current_user)


