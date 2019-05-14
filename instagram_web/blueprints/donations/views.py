from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.profile_page import ProfilePage
from models.donation import Donation
from flask_login import current_user, login_required
from instagram_web.util.braintree import generate_client_token, complete_transaction
# from instagram_web.util.sendgrid import send_notify_message

donations_blueprint = Blueprint('donations',
                                __name__,
                                template_folder='templates')


@donations_blueprint.route('/<profile_page_id>/new', methods=['GET'])
@login_required
def new(profile_page_id):
    profile_page = ProfilePage.get_or_none(ProfilePage.id == profile_page_id)
    client_token = generate_client_token()
    if not profile_page:
        flash('Unable to find profile_page with the provided id!', 'warning')
        return redirect(url_for('home'))

    return render_template('new.html', profile_page=profile_page, client_token=client_token)


@donations_blueprint.route('/<profile_page_id>/checkout', methods=['POST'])
@login_required
def create(profile_page_id):
    payment_nonce = request.form.get('payment_method_nonce')
    amount = request.form.get('donation_amount')
    profile_page = ProfilePage.get_or_none(ProfilePage.id == profile_page_id)

    if not profile_page:
        flash('No profile_page found!', 'warning')
        return redirect(url_for('home'))

    if not amount or not round(int(amount)) > 0:
        flash('You did not specify an amount!', 'warning')
        return redirect(url_for('donations.new', profile_page_id=profile_page.id))

    if not payment_nonce:
        flash('Error with payment system. Please try again!', 'warning')
        return redirect(url_for('users.show', username=profile_page.user.username))

    if not complete_transaction(payment_nonce, amount):
        flash('Oops, something went wrong!', 'warning')
        return redirect(url_for('donations.new', profile_page_id=profile_page.id))
    new_donation = Donation(
        user_id=current_user.id,
        amount=amount,
        image_id=profile_page.id
    )

    if not new_donation.save():
        flash('Unable to complete donation!', 'warning')
        return redirect(url_for('donations.new', profile_page_id=profile_page.id))

    # if not send_notify_message(profile_page.user.email, current_user.username, amount, profile_page):
    #     flash('Donation received but unable to notify user!', 'warning')

    flash(
        f'Donation to {profile_page.user.username} of USD {amount} is successful!', 'success')
    return redirect(url_for('users.show', username=profile_page.user.username))