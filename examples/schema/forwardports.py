import jsl


PORT_RANGE = dict(minimum=1, maximum=65535)


class ForwardPorts(jsl.Document):
    mapping = jsl.ArrayField(
                jsl.ArrayField(
                    jsl.NumberField(**PORT_RANGE),
                    jsl.NumberField(**PORT_RANGE),
                )
              )
