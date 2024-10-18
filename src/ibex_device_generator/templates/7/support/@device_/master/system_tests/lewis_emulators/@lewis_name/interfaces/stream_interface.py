from lewis.adapters.stream import StreamInterface, Cmd
from lewis.utils.command_builder import CmdBuilder
from lewis.core.logging import has_log
from lewis.utils.replies import conditional_reply


@@has_log
class @{lewis_emulator_device_class_name}StreamInterface(StreamInterface):  #pyright: ignore
    
    in_terminator = "\r\n"
    out_terminator = "\r\n"

    def __init__(self):
        super(@{lewis_emulator_device_class_name}StreamInterface, self).__init__()
        # Commands that we expect via serial during normal operation
        self.commands = {
            CmdBuilder(self.catch_all).arg("^#9.*$").build()  # Catch-all command for debugging
        }

    def handle_error(self, request, error):
        """
        If command is not recognised print and error

        Args:
            request: requested string
            error: problem

        """
        self.log.error("An error occurred at request " + repr(request) + ": " + repr(error))

    def catch_all(self, command):
        pass
