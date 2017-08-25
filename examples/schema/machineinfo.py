import jsl


class MachineInfo(jsl.Document):
    machineinfo = jsl.OneOfField([
        jsl.OneOfField([
            jsl.StringField(),
            jsl.StringField()
        ]),
        jsl.OneOfField([
            jsl.StringField(),
        ]),
        jsl.OneOfField([
            jsl.ArrayField(jsl.IPv4Field())
        ]),
        jsl.OneOfField([
            jsl.ArrayField(jsl.OneOfField([
                jsl.StringField(),
                jsl.StringField()
            ]))
        ]),
    ])
