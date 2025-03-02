"""
Protocol objects to represent objects exposed by different pq implementations.
"""

# Copyright (C) 2020 The Psycopg Team

from typing import Any, Callable, List, Optional, Sequence, Tuple
from typing import Union, TYPE_CHECKING

from ._enums import Format, Trace
from .._compat import Protocol, TypeAlias

if TYPE_CHECKING:
    from .misc import PGnotify, ConninfoOption, PGresAttDesc

# An object implementing the buffer protocol (ish)
Buffer: TypeAlias = Union[bytes, bytearray, memoryview]


class PGconn(Protocol):

    notice_handler: Optional[Callable[["PGresult"], None]]
    notify_handler: Optional[Callable[["PGnotify"], None]]

    @classmethod
    def connect(cls, conninfo: bytes) -> "PGconn":
        ...

    @classmethod
    def connect_start(cls, conninfo: bytes) -> "PGconn":
        ...

    def connect_poll(self) -> int:
        ...

    def finish(self) -> None:
        ...

    @property
    def info(self) -> List["ConninfoOption"]:
        ...

    def reset(self) -> None:
        ...

    def reset_start(self) -> None:
        ...

    def reset_poll(self) -> int:
        ...

    @classmethod
    def ping(self, conninfo: bytes) -> int:
        ...

    @property
    def db(self) -> bytes:
        ...

    @property
    def user(self) -> bytes:
        ...

    @property
    def password(self) -> bytes:
        ...

    @property
    def host(self) -> bytes:
        ...

    @property
    def hostaddr(self) -> bytes:
        ...

    @property
    def port(self) -> bytes:
        ...

    @property
    def tty(self) -> bytes:
        ...

    @property
    def options(self) -> bytes:
        ...

    @property
    def status(self) -> int:
        ...

    @property
    def transaction_status(self) -> int:
        ...

    def parameter_status(self, name: bytes) -> Optional[bytes]:
        ...

    @property
    def error_message(self) -> bytes:
        ...

    @property
    def server_version(self) -> int:
        ...

    @property
    def socket(self) -> int:
        ...

    @property
    def backend_pid(self) -> int:
        ...

    @property
    def needs_password(self) -> bool:
        ...

    @property
    def used_password(self) -> bool:
        ...

    @property
    def ssl_in_use(self) -> bool:
        ...

    def exec_(self, command: bytes) -> "PGresult":
        ...

    def send_query(self, command: bytes) -> None:
        ...

    def exec_params(
        self,
        command: bytes,
        param_values: Optional[Sequence[Optional[Buffer]]],
        param_types: Optional[Sequence[int]] = None,
        param_formats: Optional[Sequence[int]] = None,
        result_format: int = Format.TEXT,
    ) -> "PGresult":
        ...

    def send_query_params(
        self,
        command: bytes,
        param_values: Optional[Sequence[Optional[Buffer]]],
        param_types: Optional[Sequence[int]] = None,
        param_formats: Optional[Sequence[int]] = None,
        result_format: int = Format.TEXT,
    ) -> None:
        ...

    def send_prepare(
        self,
        name: bytes,
        command: bytes,
        param_types: Optional[Sequence[int]] = None,
    ) -> None:
        ...

    def send_query_prepared(
        self,
        name: bytes,
        param_values: Optional[Sequence[Optional[Buffer]]],
        param_formats: Optional[Sequence[int]] = None,
        result_format: int = Format.TEXT,
    ) -> None:
        ...

    def prepare(
        self,
        name: bytes,
        command: bytes,
        param_types: Optional[Sequence[int]] = None,
    ) -> "PGresult":
        ...

    def exec_prepared(
        self,
        name: bytes,
        param_values: Optional[Sequence[Buffer]],
        param_formats: Optional[Sequence[int]] = None,
        result_format: int = 0,
    ) -> "PGresult":
        ...

    def describe_prepared(self, name: bytes) -> "PGresult":
        ...

    def send_describe_prepared(self, name: bytes) -> None:
        ...

    def describe_portal(self, name: bytes) -> "PGresult":
        ...

    def send_describe_portal(self, name: bytes) -> None:
        ...

    def get_result(self) -> Optional["PGresult"]:
        ...

    def consume_input(self) -> None:
        ...

    def is_busy(self) -> int:
        ...

    @property
    def nonblocking(self) -> int:
        ...

    @nonblocking.setter
    def nonblocking(self, arg: int) -> None:
        ...

    def flush(self) -> int:
        ...

    def set_single_row_mode(self) -> None:
        ...

    def get_cancel(self) -> "PGcancel":
        ...

    def notifies(self) -> Optional["PGnotify"]:
        ...

    def put_copy_data(self, buffer: Buffer) -> int:
        ...

    def put_copy_end(self, error: Optional[bytes] = None) -> int:
        ...

    def get_copy_data(self, async_: int) -> Tuple[int, memoryview]:
        ...

    def trace(self, fileno: int) -> None:
        ...

    def set_trace_flags(self, flags: Trace) -> None:
        ...

    def untrace(self) -> None:
        ...

    def encrypt_password(
        self, passwd: bytes, user: bytes, algorithm: Optional[bytes] = None
    ) -> bytes:
        ...

    def make_empty_result(self, exec_status: int) -> "PGresult":
        ...

    @property
    def pipeline_status(self) -> int:
        ...

    def enter_pipeline_mode(self) -> None:
        ...

    def exit_pipeline_mode(self) -> None:
        ...

    def pipeline_sync(self) -> None:
        ...

    def send_flush_request(self) -> None:
        ...


class PGresult(Protocol):
    def clear(self) -> None:
        ...

    @property
    def status(self) -> int:
        ...

    @property
    def error_message(self) -> bytes:
        ...

    def error_field(self, fieldcode: int) -> Optional[bytes]:
        ...

    @property
    def ntuples(self) -> int:
        ...

    @property
    def nfields(self) -> int:
        ...

    def fname(self, column_number: int) -> Optional[bytes]:
        ...

    def ftable(self, column_number: int) -> int:
        ...

    def ftablecol(self, column_number: int) -> int:
        ...

    def fformat(self, column_number: int) -> int:
        ...

    def ftype(self, column_number: int) -> int:
        ...

    def fmod(self, column_number: int) -> int:
        ...

    def fsize(self, column_number: int) -> int:
        ...

    @property
    def binary_tuples(self) -> int:
        ...

    def get_value(self, row_number: int, column_number: int) -> Optional[bytes]:
        ...

    @property
    def nparams(self) -> int:
        ...

    def param_type(self, param_number: int) -> int:
        ...

    @property
    def command_status(self) -> Optional[bytes]:
        ...

    @property
    def command_tuples(self) -> Optional[int]:
        ...

    @property
    def oid_value(self) -> int:
        ...

    def set_attributes(self, descriptions: List["PGresAttDesc"]) -> None:
        ...


class PGcancel(Protocol):
    def free(self) -> None:
        ...

    def cancel(self) -> None:
        ...


class Conninfo(Protocol):
    @classmethod
    def get_defaults(cls) -> List["ConninfoOption"]:
        ...

    @classmethod
    def parse(cls, conninfo: bytes) -> List["ConninfoOption"]:
        ...

    @classmethod
    def _options_from_array(cls, opts: Sequence[Any]) -> List["ConninfoOption"]:
        ...


class Escaping(Protocol):
    def __init__(self, conn: Optional[PGconn] = None):
        ...

    def escape_literal(self, data: Buffer) -> bytes:
        ...

    def escape_identifier(self, data: Buffer) -> bytes:
        ...

    def escape_string(self, data: Buffer) -> bytes:
        ...

    def escape_bytea(self, data: Buffer) -> bytes:
        ...

    def unescape_bytea(self, data: Buffer) -> bytes:
        ...
