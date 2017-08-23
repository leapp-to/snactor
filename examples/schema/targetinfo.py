import jsl


class TargetInfo(jsl.Document):
    targetinfo = jsl.OneOfField([
        jsl.OneOfField([
            jsl.StringField(),
            jsl.StringField()
        ]),
        jsl.OneOfField([
            jsl.StringField(),
            jsl.StringField()
        ]),
        jsl.OneOfField([
            jsl.StringField(),
            jsl.ArrayField(jsl.StringField())
        ])
    ])
