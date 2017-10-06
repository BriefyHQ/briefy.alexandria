"""briefy.alexandria config."""
from prettyconf import config

DATABASE_URL = config('DATABASE_URL',)

# aws assets base
AWS_ASSETS_SOURCE = config('AWS_ASSETS_SOURCE', default='source/assets')
