# Django Signals

I haven't had my coffee yet :(

## Setup

1. Fork and clone [this repository](https://github.com/JoinCODED/TASK-Django-M13-Signals).
2. Install the requirements using `pip install -r requirements/dev.lock`.

## Signals Setup

1. Create a `signals.py` file inside of `coffeeshops`.
2. Go to `coffeeshops/apps.py` and add a ready method like so to `CoffeeshopsConfig`:

   ```python
   class CoffeeshopsConfig(AppConfig):
       default_auto_field = "django.db.models.BigAutoField"
       name = "coffeeshops"

       def ready(self) -> None:
           import coffeeshops.signals
   ```

   - This will allow our signals to work when the app starts. You can read about this method [here](https://docs.djangoproject.com/en/4.0/ref/applications/#django.apps.AppConfig.ready).

## Emails

We want to be notified every time a new cafe owner has joined our platform. To do that we need to send an email each time a `CafeOwner` has been created.

1. Go to `coffeeshops/signals.py` and import `send_mail` from `django.core.mail` (we will need this function later).
2. Create a function called `send_new_owner_email`, which takes in a `sender`, `instance`, `created`, and `**kwargs`.
   - Use the `send_mail` function (read about it [here](https://docs.djangoproject.com/en/4.0/topics/email/#quick-example)) if `created` is `True`.
   - Send an email with the subject as `New Cafe Owner` and the body of the email as `A new cafe owner has joined named <FULL_NAME_OF_CAFE_OWNER>`. For the `from_email` you can use `"sender@test.com"` and `recipient_list` can be `["receiver@test.com"]`.
3. Decorate your `send_new_owner_email` with `register`, which is imported from `django.dispatch` (read about decorators [here](https://www.programiz.com/python-programming/decorator)).
4. Add `post_save` (imported from `django.db.models.signals`) as the first argument to your `register` decorator and set the `sender` parameter equal to `CafeOwner` (imported from `coffeeshops.models`).
   - Read about the `post_save` signal [here](https://docs.djangoproject.com/en/4.0/ref/signals/#django.db.models.signals.post_save).
5. Test out your signal by creating an admin account (using `./manage.py createsuperuser`), starting the server, logging in to the admin site, and creating a new `CafeOwner`.

   - You should see a new log in `TASK-Django-M13-Signals/emails/TIMESTAMP.log` (where `timestamp` are hyphenated numbers) that should look something like this:

     ```text
     Content-Type: text/plain; charset="utf-8"
     MIME-Version: 1.0
     Content-Transfer-Encoding: 7bit
     Subject: New Cafe Owner
     From: sender@test.com
     To: receiver@test.com
     Date: Sat, 23 Jul 2022 22:26:35 -0000
     Message-ID: <165861519536.9692.1816094537173382016@YOUR_COMPUTER_USERNAME>

     A new cafe owner has joined named Guido van Rossum.
     -------------------------------------------------------------------------------
     ```
