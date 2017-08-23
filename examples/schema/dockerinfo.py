import jsl


class DockerInfo(jsl.Document):
    path = jsl.OneOfField([
        jsl.IntField(),
        jsl.StringField()
    ])
    systemd_state = jsl.OneOfField([
        jsl.IntField(),
        jsl.StringField()
    ])
    info = jsl.OneOfField([
        jsl.IntField(),
        jsl.StringField()
    ])
