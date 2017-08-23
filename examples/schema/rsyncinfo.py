import jsl


class RSyncInfo(jsl.Document):
    path = jsl.OneOfField([
        jsl.IntField(),
        jsl.StringField()
    ])
    version = jsl.OneOfField([
        jsl.IntField(),
        jsl.StringField()
    ])
