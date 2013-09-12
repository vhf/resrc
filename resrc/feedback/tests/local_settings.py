"""Settings that need to be set in order to run the tests."""
# email settings
ADMINS = (('Tobias Lorenz', 'beardedbearrecords@gmail.com'), )
FROM_EMAIL = ADMINS[0][1]

MAILER_EMAIL_BACKEND = 'django_libs.test_email_backend.EmailBackend'
TEST_EMAIL_BACKEND_RECIPIENTS = ADMINS

EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = FROM_EMAIL
EMAIL_HOST_PASSWORD = "R0bbe&google"
EMAIL_PORT = 587

DEFAULT_FROM_EMAIL = FROM_EMAIL
SERVER_EMAIL = FROM_EMAIL
EMAIL_USE_TLS = True

# Feedback settings
FEEDBACK_FORM_TEXT = """
<h3>Hi! Do you have feedback or questions?</h3>
<p>We'll answer as fast as possible.</p>
"""
