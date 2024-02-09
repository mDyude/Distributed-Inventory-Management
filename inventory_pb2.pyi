from google.protobuf import empty_pb2 as _empty_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class Product(_message.Message):
    __slots__ = ("product_identifier", "product_name", "product_quantity", "product_price")
    PRODUCT_IDENTIFIER_FIELD_NUMBER: _ClassVar[int]
    PRODUCT_NAME_FIELD_NUMBER: _ClassVar[int]
    PRODUCT_QUANTITY_FIELD_NUMBER: _ClassVar[int]
    PRODUCT_PRICE_FIELD_NUMBER: _ClassVar[int]
    product_identifier: int
    product_name: str
    product_quantity: int
    product_price: float
    def __init__(self, product_identifier: _Optional[int] = ..., product_name: _Optional[str] = ..., product_quantity: _Optional[int] = ..., product_price: _Optional[float] = ...) -> None: ...

class Status(_message.Message):
    __slots__ = ("status",)
    STATUS_FIELD_NUMBER: _ClassVar[int]
    status: str
    def __init__(self, status: _Optional[str] = ...) -> None: ...

class ProductIdentifier(_message.Message):
    __slots__ = ("product_identifier",)
    PRODUCT_IDENTIFIER_FIELD_NUMBER: _ClassVar[int]
    product_identifier: int
    def __init__(self, product_identifier: _Optional[int] = ...) -> None: ...

class Quantity(_message.Message):
    __slots__ = ("product_identifier", "product_quantity")
    PRODUCT_IDENTIFIER_FIELD_NUMBER: _ClassVar[int]
    PRODUCT_QUANTITY_FIELD_NUMBER: _ClassVar[int]
    product_identifier: int
    product_quantity: int
    def __init__(self, product_identifier: _Optional[int] = ..., product_quantity: _Optional[int] = ...) -> None: ...
