from .db import fetch_reports, insert_report, update_report_status, get_reports_for_digest
from .services.digest_service import generate_digest
from flask import Blueprint, render_template, request, redirect, url_for, flash
from .db import fetch_reports, insert_report, update_report_status
from datetime import datetime

routes_bp = Blueprint('routes', __name__)

CATEGORIES = ['phishing', 'phone_scam', 'data_breach', 'fraud', 'physical_safety', 'utility_scam']
SEVERITIES = ['low', 'medium', 'high']
STATUSES = ['new', 'reviewed', 'resolved']

@routes_bp.route('/')
def index():
    search = request.args.get('search', '').strip()
    category = request.args.get('category', '')
    severity = request.args.get('severity', '')
    status = request.args.get('status', '')
    reports = fetch_reports(
        search=search or None,
        category=category or None,
        severity=severity or None,
        status=status or None
    )
    return render_template('index.html',
        reports=reports,
        search=search,
        category=category,
        severity=severity,
        status=status,
        categories=CATEGORIES,
        severities=SEVERITIES,
        statuses=STATUSES
    )

@routes_bp.route('/reports/new')
def new_report():
    return render_template('create_report.html',
        categories=CATEGORIES,
        severities=SEVERITIES
    )

@routes_bp.route('/reports', methods=['POST'])
def create_report():
    title = request.form.get('title', '').strip()
    description = request.form.get('description', '').strip()
    category = request.form.get('category', '').strip()
    severity = request.form.get('severity', '').strip()
    location = request.form.get('location', '').strip()
    verified = request.form.get('verified') == 'on'

    errors = []
    if not title:
        errors.append('Title is required.')
    if not description:
        errors.append('Description is required.')
    if category not in CATEGORIES:
        errors.append(f'Category must be one of: {", ".join(CATEGORIES)}.')
    if severity not in SEVERITIES:
        errors.append(f'Severity must be one of: {", ".join(SEVERITIES)}.')
    if not location:
        errors.append('Location is required.')

    if errors:
        for e in errors:
            flash(e, 'error')
        return render_template('create_report.html',
            categories=CATEGORIES,
            severities=SEVERITIES,
            form_data=request.form
        )

    insert_report({
        'title': title,
        'description': description,
        'category': category,
        'severity': severity,
        'location': location,
        'status': 'new',
        'created_at': datetime.now().isoformat(),
        'verified': verified
    })
    flash('Report submitted successfully.', 'success')
    return redirect(url_for('routes.index'))

@routes_bp.route('/reports/<int:report_id>/status', methods=['POST'])
def update_status(report_id):
    new_status = request.form.get('status', '').strip()
    if new_status not in STATUSES:
        flash('Status update failed because the selected value is invalid.', 'error')
        return redirect(url_for('routes.index'))
    update_report_status(report_id, new_status)
    flash('Status updated successfully.', 'success')
    return redirect(url_for('routes.index'))

@routes_bp.route('/digest')
def digest():
    search = request.args.get('search', '').strip()
    category = request.args.get('category', '')
    severity = request.args.get('severity', '')
    status = request.args.get('status', '')
    reports = get_reports_for_digest(
        search=search or None,
        category=category or None,
        severity=severity or None,
        status=status or None
    )
    digest_data = generate_digest(reports)
    return render_template('digest.html', digest=digest_data)
