# from construct import *

from hci_protocol import *

# AttCommandPacket.sizeof(Container(opcode='ATT_OP_READ_BY_TYPE_RESPONSE')(payload=Container(length=4)(attribute_data_list=[Container(handle=1)(value=2), Container(handle=1)(value=2)])))

L2CapPacket.sizeof(
    dict(
        cid=4,
        payload=dict(
            opcode='ATT_OP_READ_BY_TYPE_RESPONSE',
            payload=dict(
                length=4,
                attribute_data_list=[dict(handle=1, value=2), dict(handle=3, value=4)]
            )
        )
    )
)

# class _AttributeHandleValuePair(Struct):
#     def _sizeof(self, context, path):
#         path_list = path.split(' -> ')
#         #remove sizeof and the first ancestor of the path
#         path_to_grandparent = path_list[2:-2]
#         path_to_length = path_to_grandparent
#         path_to_length.append('length')
#         length = context
#         for x in path_to_length:
#             length = length[x]
#         print(length)
#         return length
#
# AttributeHandleValuePair = "attribute_handle_value_pair" / _AttributeHandleValuePair(
#     "handle" / Int16ul,
#     "value" / Bytes(this._.length - 2)
# )
#
# AttReadByTypeResponse = "read_by_type_response" / Struct(
#     "length" / Int8ul,  # The size in bytes of each handle/value pair
#     "attribute_data_list" / Array(2, AttributeHandleValuePair)
# )
#
# AttReadByTypeResponse.sizeof(
#     Container(length=4)(attribute_data_list=[Container(handle=1)(value=2), Container(handle=1)(value=2)])
# )


# Tmp = "tmp" / Struct(
#     "a" / Int8ul,
#     Embedded(Array(2, Int8ul)),
#     "b" / Int8ul
# )


# AttributeHandleValuePair = "attribute_handle_value_pair" / Struct(
#     "handle" / Int16ul,
#     "value" / Bytes(this._.length - 2)
# )
#
# AttReadByTypeResponse = "read_by_type_response" / Struct(
#     "length" / Int8ul,  # The size in bytes of each handle/value pair
#     "attribute_data_list" / AttributeHandleValuePair
# )
#
# AttReadByTypeResponse.sizeof(Container(length=4)(attribute_data_list=Container(handle=1)(value=2)))
