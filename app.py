import toml

import aioli
import aioli_rdbms
import aioli_openapi

import scorebored


app = aioli.Application(
    config=toml.load("app.cfg"), packages=[aioli_rdbms, aioli_openapi, scorebored]
)
