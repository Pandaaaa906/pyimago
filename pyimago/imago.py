from ctypes import *

from os import path

from pyimago.decorators import decode_result, ensure_session_id, check_error

_lib = WinDLL(path.join(path.dirname(path.realpath(__file__)), r"imago_x64\imago_c.dll"))


class FILTER:
    prefilter_binarized = b"prefilter_binarized"
    prefilter_basic = b"prefilter_basic"
    prefilter_adaptive = b"prefilter_adaptive"


class Imago(object):
    _sid = None

    def __init__(self):
        _lib.imagoGetVersion.restype = c_char_p
        _lib.imagoGetLastError.restype = c_char_p
        self.get_new_session()

    def get_new_session(self):
        self._sid = _lib.imagoAllocSessionId()
        _lib.imagoSetSessionId(self.sid)

    def set_session_id(self):
        return _lib.imagoSetSessionId(self.sid)

    @property
    def sid(self):
        return self._sid

    @decode_result()
    def version(self):
        return _lib.imagoGetVersion()

    # TODO load from buffer not working
    """
    @check_error
    @ensure_session_id
    def load_image_from_buffer(self, buffer):
        size = c_int(len(buffer))
        buffer = c_char_p(buffer)
        return _lib.imagoLoadImageFromBuffer(buffer, size)
    """

    @check_error
    @ensure_session_id
    def load_image_from_file(self, fp):
        fp = c_char_p(fp.encode('u8'))
        return _lib.imagoLoadImageFromFile(fp)

    @check_error
    def _get_mol_text(self, buffer, size):
        return _lib.imagoSaveMolToBuffer(pointer(buffer), pointer(c_int(size)))

    @decode_result()
    def get_mol_text(self):
        size = 1024
        buffer = c_char_p(size)
        self._get_mol_text(buffer, size)
        self.release_session()
        return buffer.value

    @check_error
    def recognize(self):
        warnings = c_int()
        res = _lib.imagoRecognize(pointer(warnings))
        if warnings.value != 0:
            print(self.get_last_error())
        return res

    def __del__(self):
        self.release_session()

    @decode_result()
    def get_last_error(self):
        return _lib.imagoGetLastError()

    def release_session(self):
        return _lib.imagoReleaseSessionId(self.sid)

    def set_filter(self, name):
        name = c_char_p(name)
        return _lib.imagoSetFilter(name)

    @check_error
    @ensure_session_id
    def filter_image(self):
        return _lib.imagoFilterImage()

    def get_mol_text_from_fp(self, fp, filters=None):
        self.load_image_from_file(fp)
        if filters:
            for filter_name in filters:
                self.set_filter(filter_name)
            self.filter_image()
        self.recognize()
        return self.get_mol_text()
