import sys
import os
from tkinter import Tk
from tkinter import filedialog


def format_folder_drive_path_backslash(path):
    path = path.strip('"\\/: ')
    if len(path) == 1:
        path = f"{path}:"
    return path


def get_filepath(exefile: str):
    # for py files and compiled nuitka exe (1 file)
    filepath = os.path.dirname(sys.argv[0])
    fpa = os.path.normpath(os.path.join(filepath, exefile))
    if os.path.exists(fpa):
        filepath = fpa
    else:
        filepath = os.path.dirname(__file__)
        fpa = os.path.normpath(os.path.join(filepath, exefile))
        if os.path.exists(fpa):
            filepath = fpa

        else:
            filepath = os.sep.join(os.path.dirname(sys.argv[0]).split(os.sep)[:-1])
            fpa = os.path.normpath(os.path.join(filepath, exefile))
            if os.path.exists(fpa):
                filepath = fpa
            else:
                filepath = os.sep.join(os.path.dirname(__file__).split(os.sep)[:-1])
                fpa = os.path.normpath(os.path.join(filepath, exefile))
                if os.path.exists(fpa):
                    filepath = fpa
                else:
                    fi = sys._getframe(1)
                    dct = fi.f_globals
                    f = dct.get("__file__", "")

                    filepathpu = os.path.dirname(f)
                    fpa = os.path.join(filepathpu, exefile)
                    if os.path.exists(fpa):
                        filepath = fpa
                    else:
                        fpa = os.sep.join(
                            os.path.dirname(filepathpu).split(os.sep)[:-1]
                        )
                        fpa = os.path.normpath(os.path.join(fpa, exefile))
                        if os.path.exists(fpa):
                            filepath = fpa
                        else:
                            filepath = exefile
    return filepath


def get_file_with_tkinter(filetypes=(("clang.exe", "clang.exe"),)):
    Tk().withdraw()
    file = filedialog.askopenfilename(filetypes=filetypes, multiple=False)

    return os.path.normpath(file)


try:
    cfgfi = get_file_with_tkinter(filetypes=(("Config files", "*.ini"),))
    cfgfile = get_filepath(cfgfi)
    from hackycfgparser import add_config, load_config_file_vars

    load_config_file_vars(cfgfile=cfgfile, onezeroasboolean=False)
except Exception as fe:
    print(fe)
    from hackycfgparser import add_config

from tkinter import messagebox
import sys
from collections import deque
import subprocess
from touchtouch import touch
import fabisschomagut
import ctypes
import os
from ctypes import LibraryLoader
from ctypes import WinDLL
from ctypes import wintypes
from ctypes import c_void_p
from ctypes import c_int
from ctypes import byref
from kthread_sleep import sleep
import keyboard
import numpy as np
import kthread


def show_warning(title: str, message: str):
    """
    Displays a warning message box with the given title and message.

    Args:
        title (str): The title of the warning message box.
        message (str): The message to be displayed in the warning message box.

    Returns:
        None: This function does not return anything.

    Raises:
        N/A

    Example:
        >>> show_warning("Warning", "This is a warning message.")
    """
    messagebox.showwarning(title, message)


def show_info(title: str, message: str):
    messagebox.showinfo(title, message)


def show_error(title: str, message: str):
    messagebox.showerror(title, message)


configuration = sys.modules[__name__]
configuration.colorlookup = {}
configuration.colorlookuppassed = {}
configuration.colortodraw = 0x000000
configuration.linethickness = 4
configuration.clearall = False
configuration.thicknessplus = None
configuration.thicknessminus = None
configuration.clearallkey = None
configuration.oldarrays = deque([], 3)

windll = LibraryLoader(WinDLL)
user32 = windll.user32

CreatePen = windll.gdi32.CreatePen
CreatePen.restype = wintypes.HPEN
CreatePen.argtypes = [
    c_int,
    c_int,
    wintypes.COLORREF,
]
CreateBrushIndirect = windll.gdi32.CreateBrushIndirect
CreateBrushIndirect.restype = wintypes.HBRUSH
CreateBrushIndirect.argtypes = [
    c_void_p,
]
CreateDC = windll.gdi32.CreateDCW
CreateDC.restype = wintypes.HDC
CreateDC.argtypes = [
    wintypes.LPCWSTR,
    wintypes.LPCWSTR,
    wintypes.LPCWSTR,
    c_void_p,
]
SelectObject = windll.gdi32.SelectObject
SelectObject.restype = wintypes.HGDIOBJ
SelectObject.argtypes = [
    wintypes.HDC,
    wintypes.HGDIOBJ,
]

Rectangle = windll.gdi32.Rectangle
Rectangle.restype = wintypes.BOOL
Rectangle.argtypes = [
    wintypes.HDC,
    c_int,
    c_int,
    c_int,
    c_int,
]

DeleteObject = windll.gdi32.DeleteObject
DeleteObject.restype = wintypes.BOOL
DeleteObject.argtypes = [
    wintypes.HGDIOBJ,
]

DeleteDC = windll.gdi32.DeleteDC
DeleteDC.restype = wintypes.BOOL
DeleteDC.argtypes = [
    wintypes.HDC,
]
BOOL = wintypes.BOOL
BYTE = wintypes.BYTE
CHAR = ctypes.c_char
DWORD = wintypes.DWORD
HANDLE = wintypes.HANDLE
HBITMAP = HANDLE
LONG = wintypes.LONG
LPVOID = wintypes.LPVOID
PVOID = c_void_p
UINT = wintypes.UINT
WCHAR = wintypes.WCHAR
WORD = wintypes.WORD
LRESULT = wintypes.LPARAM
COLORREF = wintypes.COLORREF
PS_SOLID = 0
BS_NULL = 1
HS_DIAGCROSS = 5
SetPixel = windll.gdi32.SetPixel
SetPixel.argtypes = [wintypes.HDC, ctypes.c_int, ctypes.c_int, wintypes.COLORREF]
SetPixel.restype = wintypes.COLORREF
POINT = wintypes.POINT


def load_so_file():
    def compile_ccp_source(
            save_path="colordrawc.so", clangpath=r"C:\Program Files\LLVM\bin\clang.exe"
    ):
        save_path = os.path.join(os.path.dirname(sys.executable), save_path)
        savepathso = os.path.normpath(save_path)
        touch(savepathso)
        os.remove(savepathso)

        c_source_code = """
#include <windows.h>
#include <omp.h>
#pragma comment(lib, "gdi32.lib")
#pragma comment(lib, "User32.lib")
extern "C" __declspec(dllexport) void draw_image(HDC hdc, HWND hwnd, int coordlen, int *coordx, int *coordy, int *rgbc, unsigned int *breakding)
{
    int i;
    for (i = 0; i < coordlen; i++)
    {
            if (breakding[0] == 0){
            SetPixel(hdc, coordx[i], coordy[i], rgbc[i]);}
    }


}
        """
        commandsub = [
            clangpath,
            "-xc++",
            "-O3",
            "-march=native",
            "-funroll-loops",
            "-fomit-frame-pointer",
            "-fopenmp",
            "-Wl,",
            "-out-implib,libCloop.dll.a",
            "-shared",
            "-o",
            savepathso,
            "-",
        ]

        olddict = os.getcwd()
        os.chdir(os.path.dirname(clangpath))
        paxas = subprocess.run(
            commandsub,
            input=c_source_code.encode(),
            shell=True,
            stderr=subprocess.PIPE,
            stdout=subprocess.PIPE,
        )
        print(paxas)
        os.chdir(olddict)
        return (
            savepathso,
            paxas.stdout.decode("utf-8", "ignore"),
            paxas.stderr.decode("utf-8", "ignore"),
        )

    pixel_drawer = None
    try:
        colordraw = get_filepath("colordrawc.so")
        if os.path.exists(colordraw):
            pixel_drawer = ctypes.CDLL(colordraw)
        else:
            raise ValueError
    except Exception as fe:
        clangpath = r"C:\Program Files\LLVM\bin\clang.exe"
        if not os.path.exists(clangpath):
            show_warning(
                "Warning - could not found Clang.exe",
                "I need clang to compile the C++ code\nYou can download clang here:\nhttps://community.chocolatey.org/packages/llvm",
            )
            clangpath = get_file_with_tkinter(filetypes=(("clang.exe", "clang.exe"),))
        if os.path.exists(clangpath):
            compiledfile, stdoutput, stderrout = compile_ccp_source(
                save_path="colordrawc.so", clangpath=clangpath
            )
            show_info("Clang output", f"{stdoutput}\n{stderrout}")
            if os.path.exists(compiledfile):
                pixel_drawer = ctypes.CDLL(compiledfile)
            else:
                try:
                    sys.exit(1)
                finally:
                    os._exit(1)
    return pixel_drawer


class LOGBRUSH(ctypes.Structure):
    _fields_ = [
        ("lbStyle", UINT),
        ("lbColor", COLORREF),
        ("lbHatch", LONG),
    ]


RedrawScreen = user32.RedrawWindow
RedrawScreen.argtypes = [
    wintypes.HWND,
    ctypes.POINTER(wintypes.RECT),
    wintypes.HRGN,
    wintypes.UINT,
]
RedrawScreen.restype = ctypes.c_bool

VK_LBUTTON = 0x01
VK_RBUTTON = 0x02

GetAsyncKeyState = user32.GetAsyncKeyState

GetCursorPos = user32.GetCursorPos

pixel_drawer = load_so_file()

HDC = wintypes.HDC
pixel_drawer.draw_image.argtypes = [
    HDC,
    wintypes.HWND,
    c_int,
    ctypes.POINTER(c_int),
    ctypes.POINTER(c_int),
    ctypes.POINTER(c_int),
    ctypes.POINTER(c_int),
]
pixel_drawer.draw_image.restype = None

GetKeyState = user32.GetKeyState
GetKeyState.argtypes = (ctypes.c_int,)
GetKeyState.restype = wintypes.USHORT
breakarray = np.zeros(1, dtype=np.int32)
breakarraypoi = breakarray.ctypes.data_as(ctypes.POINTER(ctypes.c_int))

gdi32 = ctypes.WinDLL("gdi32")

HWND = wintypes.HWND
HDC = wintypes.HDC
HBRUSH = wintypes.HBRUSH
HPEN = wintypes.HPEN

GetDC = user32.GetDC
ReleaseDC = user32.ReleaseDC
CreatePen = gdi32.CreatePen
SelectObject = gdi32.SelectObject
DeleteObject = gdi32.DeleteObject
Ellipse = gdi32.Ellipse

hwnd = user32.GetDesktopWindow()


def draw_circle(hwnd, x, y, r, color, freememory=False):
    hdc = GetDC(hwnd)
    color = COLORREF(color)  # green
    hBrush = gdi32.CreateSolidBrush(color)
    hPen = CreatePen(0, 1, color)
    hOldBrush = SelectObject(hdc, hBrush)
    hOldPen = SelectObject(hdc, hPen)

    Ellipse(hdc, x, y, x + r, y + r)

    SelectObject(hdc, hOldBrush)
    SelectObject(hdc, hOldPen)
    DeleteObject(hPen)
    DeleteObject(hBrush)

    if freememory:
        ReleaseDC(hwnd, hdc)
    gc.collect()


def set_new_col(col, freememory=True):
    fab = int(col)
    configuration.colortodraw = fab
    draw_circle(hwnd, 2, 2, 50, fab, freememory)


def clear_all_active():
    configuration.clearall = True
    hwnd = ctypes.windll.user32.GetDesktopWindow()
    hdc = ctypes.windll.user32.GetDC(hwnd)
    clean_screens(hwnd, hdc, color=0xFFFFFF, freememory=True)
    gc.collect()


def thicknessup():
    configuration.linethickness += 1


def thicknessdown():
    newthickness = configuration.linethickness - 1
    if newthickness < 1:
        newthickness = 1
    configuration.linethickness = newthickness


def iskeypressed(virtual_key_code):
    firstr = GetAsyncKeyState(virtual_key_code)
    return firstr & 0x8000


mrleft = lambda: iskeypressed(0x01)
mright = lambda: iskeypressed(0x02)
mmiddle = lambda: iskeypressed(0x04)

mousedict = {"left": mrleft, "right": mright, "middle": mmiddle}


def drawnewcpp(buffer):
    ara = np.array(
        [
            (x[0], x[1], configuration.colorlookup[x])
            for x in buffer
            if x in configuration.colorlookup
        ]
    )
    allx = np.ascontiguousarray(ara[..., 0], dtype=np.int32)
    ally = np.ascontiguousarray(ara[..., 1], dtype=np.int32)
    allco = np.ascontiguousarray(ara[..., 2], dtype=np.int32)
    return allx, ally, allco


def sourroundingpix(x_center, y_center, side_length):
    abstand = side_length // 2
    x = np.arange(x_center - abstand, x_center + abstand + 1, 1, dtype=np.int32)
    y = np.arange(y_center - abstand, y_center + abstand + 1, 1, dtype=np.int32)
    xx, yy = np.meshgrid(x, y)
    return set((q for q in zip(xx.ravel(), yy.ravel())))


def draw_with_cpp(hwnd, hdcc2, allcolors, allxcoords, allycoords):
    width = allxcoords
    coordx = width.ctypes.data_as(ctypes.POINTER(ctypes.c_int))
    height = allycoords
    coordy = height.ctypes.data_as(ctypes.POINTER(ctypes.c_int))
    inputarray = np.array(allcolors, dtype=np.int32)
    coordlenx = len(inputarray)
    coordlen = ctypes.c_int(coordlenx)
    rgbc = inputarray.ctypes.data_as(ctypes.POINTER(ctypes.c_int))
    pixel_drawer.draw_image(hdcc2, hwnd, coordlen, coordx, coordy, rgbc, breakarraypoi)


def show_results_with_cpp(hwnd, hdcc2, buffer, sleep_between_refresh):
    try:
        sleep(sleep_between_refresh)
        x_, y_, allcolors = drawnewcpp(buffer)
        draw_with_cpp(hwnd, hdcc2, allcolors, x_, y_)
    except Exception:
        return


def killme():
    try:
        keyboard.unhook_all_hotkeys()
        hwnd = ctypes.windll.user32.GetDesktopWindow()
        hdc = ctypes.windll.user32.GetDC(hwnd)
        clean_screens(hwnd, hdc, color=0xFFFFFF, freememory=True)
        sys.exit(0)
    finally:
        os._exit(0)


def get_monitors_resolution():
    def _get_monitors_resolution():
        monitors = []
        monitor_enum_proc = ctypes.WINFUNCTYPE(
            ctypes.c_int,
            ctypes.c_ulong,
            ctypes.c_ulong,
            ctypes.POINTER(ctypes.wintypes.RECT),
            ctypes.c_double,
        )

        def callback(hMonitor, hdcMonitor, lprcMonitor, dwData):
            monitors.append(
                (
                    lprcMonitor.contents.right - lprcMonitor.contents.left,
                    lprcMonitor.contents.bottom - lprcMonitor.contents.top,
                )
            )
            return 1

        user32.EnumDisplayMonitors(None, None, monitor_enum_proc(callback), 0)
        return monitors

    resolutions = _get_monitors_resolution()
    allmonitors = {}
    for i, res in enumerate(resolutions):
        allmonitors[i] = {"width": res[0], "height": res[1]}
    return allmonitors


def get_all_mon_dim():
    try:
        monis = get_monitors_resolution().items()
        width, height = (
            sum([x[1]["width"] for x in monis]),
            list(monis)[-1][-1]["height"],
        )
    except Exception:
        width = user32.GetSystemMetrics(0)
        height = user32.GetSystemMetrics(1)
    return width, height


import gc


def clean_screens(hwnd, hdc, color=0xFFFFFF, freememory=False):
    hBrush = windll.gdi32.CreateSolidBrush(color)
    width, height = get_all_mon_dim()
    rect = ctypes.wintypes.RECT(0, 0, width, height)
    user32.FillRect(hdc, ctypes.byref(rect), hBrush)
    if freememory:
        windll.gdi32.DeleteObject(hBrush)
        user32.ReleaseDC(hwnd, hdc)
    gc.collect()


@add_config
def start_ctypesscreendraw(
        colorkeys: tuple
                   | list = (
                (0xFF0000, "ctrl+alt+e"),
                (0xFFFF00, "ctrl+alt+f"),
                (0x00FF00, "ctrl+alt+g"),
        ),  #
        sleep_between_refresh: int | float = 1,
        mousedraw: str = "left",
        keydraw: int = 0x11,
        # 0x11 is the code for the CTRL key (if you press the ctrl key and move the mouse, you can draw on the screen)
        #  https://learn.microsoft.com/en-us/windows/win32/inputdev/virtual-key-codes
        mousedelete: str = "right",
        keydelete: int = 0x11,
        thickness_keys: tuple | list = ("ctrl+alt+p", "ctrl+alt+m"),
        clearallkey: str = "ctrl+alt+t",
        killkey: str = "ctrl+alt+k",
        debug: bool = True,
        dpi_awareness: int = 2,  # valid: 0,1,2
        number_of_threads: int = 1,
) -> None:
    # does nothing for now
    if number_of_threads < 1:
        number_of_threads = os.cpu_count()
    os.environ["OMP_NUM_THREADS"] = str(number_of_threads)

    def draw_outline() -> bool:
        def get_cursor():
            user32.GetPhysicalCursorPos(byrefp)
            return pos.x, pos.y

        buffer = set()

        pos = POINT()
        byrefp = byref(pos)
        windll.shcore.SetProcessDpiAwareness(dpi_awareness)

        configuration.clearall = False
        try:
            if killkey not in keyboard.__dict__["_hotkeys"]:
                configuration.clearallkey = keyboard.add_hotkey(killkey, killme)
            if clearallkey not in keyboard.__dict__["_hotkeys"]:
                configuration.clearallkey = keyboard.add_hotkey(
                    clearallkey, clear_all_active
                )
            if thickness_keys[0] not in keyboard.__dict__["_hotkeys"]:
                configuration.thicknessplus = keyboard.add_hotkey(
                    thickness_keys[0], thicknessup
                )
            if thickness_keys[1] not in keyboard.__dict__["_hotkeys"]:
                configuration.thicknessminus = keyboard.add_hotkey(
                    thickness_keys[1], thicknessdown
                )
        except Exception as fe:
            if debug:
                print(fe)

        pen_handle = CreatePen(PS_SOLID, 4, configuration.colortodraw)
        brush = LOGBRUSH()
        brush.lbStyle = BS_NULL
        brush.lbHatch = HS_DIAGCROSS
        brush_handle = CreateBrushIndirect(ctypes.byref(brush))
        hwnd = user32.GetDesktopWindow()
        hdc = user32.GetDC(hwnd)
        SelectObject(hdc, brush_handle)
        SelectObject(hdc, pen_handle)
        mousedrawfunction = mousedict[mousedraw]
        mousedeletefunction = mousedict[mousedelete]
        restartall = False
        hdcc2 = HDC(hdc)
        for k, i in colorkeys:
            k = int(fabisschomagut.to_rgb_hex(k, "0x", True), base=16)
            try:
                if i not in keyboard.__dict__["_hotkeys"]:
                    configuration.colorlookuppassed[k] = keyboard.add_hotkey(
                        hotkey=i, callback=set_new_col, args=(k,)
                    )
            except Exception as fe:
                if k not in configuration.colorlookuppassed:
                    configuration.colorlookuppassed[k] = {}
                    configuration.colortodraw = k

        t = None
        try:
            while True:
                if mousedrawfunction():
                    randco = configuration.colortodraw
                    while iskeypressed(keydraw):
                        breakarray[0] = 1
                        x0, y0 = get_cursor()
                        x0 = x0 + 4

                        coordtoadd = sourroundingpix(
                            x0, y0, configuration.linethickness
                        )
                        buffer.update(coordtoadd)
                        for coa in coordtoadd:
                            configuration.colorlookup[coa] = randco

                        x1_, y1_, allcolors1 = drawnewcpp(coordtoadd)
                        breakarray[0] = 0
                        draw_with_cpp(hwnd, hdcc2, allcolors1, x1_, y1_)
                        if not iskeypressed(keydraw):
                            break
                    breakarray[0] = 0
                if mousedeletefunction():
                    while iskeypressed(keydelete):
                        breakarray[0] = 1
                        x_center, y_center = get_cursor()
                        pixel_set2 = sourroundingpix(
                            x_center, y_center, configuration.linethickness * 4
                        )
                        buffer = buffer - pixel_set2
                        if not iskeypressed(keydraw):
                            break
                    breakarray[0] = 0
                if configuration.clearall:
                    restartall = True
                    buffer.clear()
                    configuration.colorlookup = {}
                    RedrawScreen(hwnd, None, None, 0)
                    raise KeyboardInterrupt
                if not restartall:
                    try:
                        if not t.is_alive():
                            t = kthread.KThread(
                                target=show_results_with_cpp,
                                args=(hwnd, hdcc2, buffer, sleep_between_refresh),
                            )
                            t.start()
                    except Exception:
                        t = kthread.KThread(
                            target=show_results_with_cpp,
                            args=(hwnd, hdcc2, buffer, sleep_between_refresh),
                        )
                        t.start()

                if restartall:
                    raise KeyboardInterrupt

        except Exception:
            pass
        except KeyboardInterrupt:
            pass
        finally:
            try:
                try:
                    DeleteObject(brush_handle)
                except Exception:
                    pass
                try:
                    DeleteObject(pen_handle)
                except Exception:
                    pass

                try:
                    DeleteDC(hdc)
                except Exception:
                    pass
            except Exception as fe:
                if debug:
                    print(fe)
            if not restartall:
                for co in colorkeys:
                    try:
                        if co[1] in keyboard.__dict__["_hotkeys"]:
                            keyboard.remove_hotkey(co[1])
                    except Exception as fe:
                        if debug:
                            print(fe)
                        continue

                try:
                    if clearallkey in keyboard.__dict__["_hotkeys"]:
                        keyboard.remove_hotkey(clearallkey)
                    if thickness_keys[0] in keyboard.__dict__["_hotkeys"]:
                        keyboard.remove_hotkey(thickness_keys[0])
                    if thickness_keys[1] in keyboard.__dict__["_hotkeys"]:
                        keyboard.remove_hotkey(thickness_keys[1])
                except Exception as fe:
                    if debug:
                        print(fe)
                keyboard.unhook_all_hotkeys()
                return False
        if restartall:
            return True
        return False

    mousedraw = mousedraw.strip().lower()
    try:
        while True:
            _ = draw_outline()
    except KeyboardInterrupt:
        pass
    except Exception as fe:
        if debug:
            print(fe)


if __name__ == "__main__":
    setdata = start_ctypesscreendraw()
