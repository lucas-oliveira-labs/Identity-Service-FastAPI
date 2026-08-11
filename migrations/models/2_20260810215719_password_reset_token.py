from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "passwordresettoken" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "token_hash" VARCHAR(128) NOT NULL UNIQUE,
    "expires_at" TIMESTAMPTZ NOT NULL,
    "used_at" TIMESTAMPTZ,
    "created_at" TIMESTAMPTZ NOT NULL,
    "user_id" INT NOT NULL REFERENCES "users" ("id") ON DELETE CASCADE
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP TABLE IF EXISTS "passwordresettoken";"""


MODELS_STATE = (
    "eJztWm1v2jAQ/isonzqpm0rWbmjfgFKNtYWJptvUabJMYsBqYrPEacs2/vvOTkLeGVS0W1"
    "g+Aec7+/zcOXmehJ+awy1ie6+uPeJq7xo/NYYdAl9S9sOGhufz2CoNAo9t5eiDh7LgsSdc"
    "bAowTrDtETBZxDNdOheUM7Ay37alkZvgSNk0NvmMfvcJEnxKxEwl8vUbmCmzyAPxop/zWz"
    "ShxLZSeVJLrq3sSCzmytZn4kw5ytXGyOS277DYeb4QM85W3pQJaZ0SRlwsiJxeuL5MX2YX"
    "bjPaUZBp7BKkmIixyAT7tkhsd4xim4bQYGigq56BkLYFQCZnElxI1VO7n8oUXurN47fHrd"
    "dvjlvgotJcWd4ug6VjYIJABc/A0JZqHAsceCiMY1AZh88crN0ZdotxjfwzyELKWWQjHNdB"
    "GxlibON+eg5wHfyAbMKmYgY/m0dHa6D81B5137dHB+D1Qi7J4QAEx2IQDunBmMQ7xpc4mN"
    "rbALwK2A3Cf7d5U/jqJycb4AtepfiqsTS+c+x599y10Ax7s21wzgXuYUc/CeKQFrY4Ik4e"
    "7VMASlCHFCOeCsygbYWRr6IvVcTeJdgaMnsRnrI10Bv9y96V0b78KJdzPO+7reBrGz05oi"
    "vrImM9eJOp0mqSxue+8b4hfzZuhoOegpd7YuqqFWM/40aTOWFfcMT4PcJW4oIQWSPUUjXH"
    "wsc2/fG4uueC69r/K7WPMEoUX2UvOdjkNkEYpGGMzdt7DFfM1EjcJC6ZwKoz4Ha3hHn5Lu"
    "mE8WfnI2JjhXC+GUIyOgrmMuRUFWyHZXQGImvcFgW3LtgpETuB7WM45UjOuHfgySbkOi9r"
    "y/yQoztZC2Z4qrYk15YrFTVcgTrKNmS5Ssofg1ou7Y1cElH9N6WZq4C9o/MnTX0Dcglepe"
    "RSjWXk0sOcwulBWGzLMtKRe0gxqksp8nzSBLoEwD+izOnIPSxzRZnkJirCJXdwNSy4LXU4"
    "twlmxRVPRGXKPYawp6rwyvK8J7kzHF6kqtnpG5nL5/Vlpzc6aKoyghMVJHnritGWT2vRVi"
    "QgEfFnJlCFo7QDMpBTQmmA8+iecZfQKTsnCwVyHzLCzCx6Zpp57l4xcMtYOphdfL/io8mm"
    "gr3DjknQsN32Vbd92tOW5dLyKfl+gVIqYP3Feqqc+0eSTim6FfWr+X+ljvwf+f/Wz5rTUX"
    "unBJp6a5MXJ3qr/MWJHKuVwH+oBOD28BgZkAjbQYHDo1PXt1Z6tdLbhdKrtUetPWrtUaY9"
    "2sSl5kwr0BvhyOE6jYFjn1pXVOk4H67RFXfE9cI3e5uKikRI/deVzf66Ig/VFgiH7nuI7p"
    "P81Q1WFIQV8LwPV8NBCceLQ7IEj5qi8athU6+Kd/814EowUiwuwvTgsv0lC3f3YtjJ0jM5"
    "QaeIHTznzWz5G+65Mf8="
)
