from flask import Blueprint, render_template, request, flash, jsonify, url_for, redirect
from flask_login import login_required, current_user
from werkzeug.exceptions import abort
from .models import User, Project, Bug
from . import db
import json

views = Blueprint('views', __name__)


@views.route('/')
@login_required
def dashboard():
    issues = Bug.query.all()

    # Get all users from the database
    users = User.query.all()

    return render_template("dashboard.html", user=current_user, issues=issues, users=users)


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

        # Retrieve the user, assignee, and project objects from the database
        user = current_user  # Current logged-in user (creator of the issue)
        assignee = User.query.get(assignee_id)
        project = Project.query.get(project_id)

        # Create a new Bug object with the form data and relationships
        new_issue = Bug(title=issue_name, description=description, status=status, user=user, project=project)
        new_issue.assignee = assignee  # Set the assignee for the new issue

        # Save the new issue to the database
        db.session.add(new_issue)
        db.session.commit()

        # Redirect the user to the dashboard or any other appropriate page
        return redirect(url_for('views.dashboard'))

    else:
        # This is a GET request, so simply render the create_issue.html template
        # and pass the necessary data (users and projects) to populate the dropdowns
        users = User.query.all()  # Get all users from the database
        projects = Project.query.all()  # Get all projects from the database
        issues = Bug.query.all()
        return render_template("create_issue.html", user=current_user, users=users, projects=projects, issue=issues)



@views.route('/update_issue/<int:issue_id>', methods=['GET', 'POST'])
@login_required
def update_issue(issue_id):
    # Get the issue to update from the database
    issue = Bug.query.get_or_404(issue_id)

    if request.method == 'POST':
        # Get the form data submitted by the user
        issue.title = request.form['title']
        issue.description = request.form['description']
        issue.status = request.form['status']


        # Commit the changes to the database
        db.session.commit()

        # Redirect back to the dashboard after updating the issue
        return redirect(url_for('views.dashboard'))


@views.route('/delete_issue/<int:issue_id>', methods=['POST'])
@login_required
def delete_issue(issue_id):
    # Retrieve the issue from the database based on the issue_id
    issue = Bug.query.get_or_404(issue_id)

    # Delete the issue from the database
    db.session.delete(issue)
    db.session.commit()

    # Redirect the user back to the dashboard or any other appropriate page after deletion
    return redirect(url_for('views.dashboard'))


@views.route('/create_project', methods=['GET', 'POST'])
@login_required
def create_project():
    if request.method == 'POST':
        # Get the form data submitted by the user
        project_name = request.form['projectName']
        description = request.form['description']

        # Create a new Project object with the form data and the current user as the project owner
        new_project = Project(name=project_name, description=description)

        # Save the new project to the database
        db.session.add(new_project)
        db.session.commit()

        # Redirect the user to the "Create Issue" page
        return redirect(url_for('views.create_issue'))

    else:
        # This is a GET request, so simply render the create_project.html template
        return render_template("create_project.html", user=current_user)

@views.route('/delete-project', methods=['POST'])
def delete_project():  
    project = json.loads(request.data) # this function expects a JSON from the INDEX.js file 
    projectId = project['projectId']
    project = Project.query.get(projectId)
    if project:
        if project.user_id == current_user.id:
            db.session.delete(project)
            db.session.commit()

    return jsonify({})
