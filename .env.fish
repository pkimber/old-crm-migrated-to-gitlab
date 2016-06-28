# Set environment variables for this VE
source venv-crm/bin/activate.fish
set -x DEFAULT_FROM_EMAIL "web@pkimber.net"
set -x DJANGO_SETTINGS_MODULE "example_crm.dev_patrick"
set -x MAIL_TEMPLATE_TYPE "django"
set -x RECAPTCHA_PRIVATE_KEY "your private key"
set -x RECAPTCHA_PUBLIC_KEY "your public key"
set -x SECRET_KEY "the_secret_key"
set -x STRIPE_PUBLISH_KEY "your_stripe_publish_key"
set -x STRIPE_SECRET_KEY "your_stripe_secret_key"
source .private
