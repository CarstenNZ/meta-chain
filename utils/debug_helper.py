import inspect
import logging
import traceback
from typing import Union, List


class DebugHelper:
    @staticmethod
    def logException(msg: str, exc: BaseException):
        """ log given exception as to logging.error, but with custom traceback
            - shows inner exceptions
        """
        if exc.__cause__ is None:       # single exception
            tbSt = '\n\t'.join(DebugHelper._genTracebackLines(exc))
        else:                           # nested exceptions
            tbSt = ""
            while exc:
                tbSt = '\n\t'.join(DebugHelper._genTracebackLines(exc)) + '\n\n\t' + tbSt
                exc = exc.__cause__

        logging.error(f"{msg}\n\t{tbSt}")
        return

    @staticmethod
    def _genTracebackLines(exc: Union[BaseException, None]) -> List[str]:
        """ returns traceback with local variables as list of string
        """

        # extracting differs if we have an exception or not
        if exc is None:
            stack = reversed([t[0] for t in traceback.walk_stack(None)][2:])
        else:
            tb = exc.__traceback__
            stack = []
            while tb:
                stack.append(tb.tb_frame)
                tb = tb.tb_next

        lines = ["Traceback (most recent call last):", "=" * 34]
        for frame in stack:
            lines.append("")
            lines.append(f'File "{frame.f_code.co_filename}", line {frame.f_lineno}, in {frame.f_code.co_name}')
            lines.append(f"> {DebugHelper._getSourceLine(frame).strip()}")

            if not frame.f_code.co_name.startswith('uvloop.loop') and frame.f_code.co_name != '<module>':
                itemsList = list(frame.f_locals.items())  # copy to avoid 'changed during iteration' problems
                for key, value in itemsList:
                    valSt = DebugHelper._getRepr(key, value)
                    if valSt is not None:
                        lines.append(f"\t{key} = {valSt}")

        if exc is not None:
            lines.append(f"exception: {repr(exc)}")

        return lines

    @staticmethod
    def _getSourceLine(frame):
        """ return source code line for given frame
        """
        try:
            sourceLines = inspect.getsource(frame.f_code).split('\n')
            lineNb = frame.f_lineno - frame.f_code.co_firstlineno
            return sourceLines[lineNb] if lineNb < len(sourceLines) else "\t???"
        except (OSError, IndexError):         # no source code avail
            return "\t<no source avail>"

    @staticmethod
    def _getRepr(name, item):
        """ get representation for given item
            - filters methods/functions out and handles errors
        """
        try:
            if inspect.ismethod(item) or inspect.isfunction(item):  # don't care
                return None
            else:
                return str(item)
        except Exception as exc:
            return f"!!! failed to get str for {name}: {exc}"
