from aioli.config import PackageConfigSchema, fields


class ConfigSchema(PackageConfigSchema):
    path = fields.String(missing="/scorebored")
