"""
- HDpip: A pip GUI based on maliang
- Copyright © 2025 寒冬利刃.
- License: GPL-3

DPI 与智能缩放工具。
"""

import decimal
import tkinter
from typing import *

_dpi_cache: decimal.Decimal | None = None

def getDpi(use_cache: bool = True) -> decimal.Decimal:
    """
    通过 Tk 根窗口获取系统 DPI。

    :param use_cache: 是否使用缓存，默认 True
    :type use_cache: bool
    :return: 当前系统 DPI，默认返回 96
    :rtype: decimal.Decimal
    """

    global _dpi_cache
    if use_cache and _dpi_cache is not None:
        return _dpi_cache

    try:
        _ = tkinter.Tk()
    except Exception:
        return decimal.Decimal("96.0")

    try:
        _.withdraw()
        _.update_idletasks()
        dpi = _.winfo_fpixels("1i")
        if dpi > 0:
            _dpi_cache = decimal.Decimal(round(dpi, 2))
            return _dpi_cache
    except Exception:
        return decimal.Decimal("96.0")
    finally:
        try:
            _.destroy()
        except Exception:
            pass

    return decimal.Decimal("96.0")

def pxToPt(px: int | decimal.Decimal, dpi: float | decimal.Decimal = getDpi(), *, auto_int: bool = True) -> decimal.Decimal | int:
    """
    将像素大小转换为点数字号。

    :param px: 像素大小
    :type px: int | decimal.Decimal
    :param dpi: 指定 DPI，None 时自动获取系统 DPI
    :type dpi: float | decimal.Decimal
    :param auto_int: 是否自动取整为整数点数字号，默认 True
    :type auto_int: bool
    :return: 对应的点数字号
    :rtype: decimal.Decimal | int
    """

    result = decimal.Decimal(px) * decimal.Decimal("72.0") / decimal.Decimal(dpi)
    result = round(result, 2)
    if auto_int:
        result = result.to_integral_value(rounding = decimal.ROUND_HALF_UP)
    return result

def ptToPx(pt: int | decimal.Decimal, dpi: float | decimal.Decimal = getDpi(), *, auto_int: bool = True) -> decimal.Decimal | int:
    """
    将点数字号转换为像素大小。

    :param pt: 点数字号
    :type pt: int | decimal.Decimal
    :param dpi: 指定 DPI，None 时自动获取系统 DPI
    :type dpi: float | decimal.Decimal
    :param auto_int: 是否自动取整为整数像素大小，默认 True
    :type auto_int: bool
    :return: 对应的像素大小
    :rtype: decimal.Decimal | int
    """

    result = decimal.Decimal(pt) * decimal.Decimal(dpi) / decimal.Decimal("72.0")
    result = round(result, 2)
    if auto_int:
        result = result.to_integral_value(rounding = decimal.ROUND_HALF_UP)
    return result

def getScreenSize() -> tuple[int, int]:
    """
    获取当前屏幕分辨率。

    :return: 当前屏幕分辨率
    :rtype: tuple[int, int]
    """

    _ = tkinter.Tk()
    _.withdraw()
    width = _.winfo_screenwidth()
    height = _.winfo_screenheight()
    _.destroy()
    return (width, height)

_smart_cache: dict[tuple[tuple[int, int], tuple[int, int], bool], decimal.Decimal] = {}

def getSmartScaleValue(
        base_size: tuple[int, int] = (1200, 800),
        screen_size: tuple[int, int] = getScreenSize(),
        *,
        strict_mode: bool = True,
        use_cache: bool = True
    ) -> decimal.Decimal:
    """
    根据屏幕分辨率和基准分辨率计算智能缩放值。

    :param base_size: 基准尺寸
    :type base_size: tuple[int, int]
    :param screen_size: 屏幕尺寸
    :type screen_size: tuple[int, int]
    :param strict_mode: 是否启用严格模式
    :type strict_mode: bool
    :param use_cache: 是否使用缓存
    :type use_cache: bool
    :return: 智能缩放值
    :rtype: decimal.Decimal
    """

    if use_cache:
        if (base_size, screen_size, strict_mode) in _smart_cache:
            return _smart_cache[(base_size, screen_size, strict_mode)]

    if strict_mode:
        x_start = int(decimal.Decimal(screen_size[0]) * decimal.Decimal("0.4") / decimal.Decimal(base_size[0]) * 5)
        x_end = int(decimal.Decimal(screen_size[0]) * decimal.Decimal("0.6") / decimal.Decimal(base_size[0]) * 5)
        y_start = int(decimal.Decimal(screen_size[1]) * decimal.Decimal("0.4") / decimal.Decimal(base_size[1]) * 5)
        y_end = int(decimal.Decimal(screen_size[1]) * decimal.Decimal("0.6") / decimal.Decimal(base_size[1]) * 5)
        start = max(x_start, y_start)
        end = min(x_end, y_end)
    else:
        if (base_size[0] / screen_size[0]) <= (base_size[1] / screen_size[1]):
            start = int(decimal.Decimal(screen_size[1]) * decimal.Decimal("0.4") / decimal.Decimal(base_size[1]) * 5)
            end = int(decimal.Decimal(screen_size[1]) * decimal.Decimal("1") / decimal.Decimal(base_size[1]) * 5)
        else:
            start = int(decimal.Decimal(screen_size[0]) * decimal.Decimal("0.4") / decimal.Decimal(base_size[0]) * 5)
            end = int(decimal.Decimal(screen_size[0]) * decimal.Decimal("1") / decimal.Decimal(base_size[0]) * 5)

    available_list = [decimal.Decimal(i) * decimal.Decimal("0.2") for i in range(start, end + 1)]
    seed_list = [i for i in available_list if i == i.to_integral_value()]

    if len(seed_list) > 0:
        result = max(seed_list)
    elif len(available_list) > 0:
        result = max(available_list)
    if len(available_list) == 0 or result < decimal.Decimal("0.6"):
        if strict_mode:
            result = getSmartScaleValue(base_size, screen_size, strict_mode = False, use_cache = use_cache)
        else:
            result = decimal.Decimal("0.6")

    _smart_cache[(base_size, screen_size, strict_mode)] = result
    return result

def smartScale(value: int | decimal.Decimal | Iterable[int | decimal.Decimal],
    base_size: tuple[int, int] = (1200, 800),
    screen_size: tuple[int, int] = getScreenSize(),
    *,
    strict_mode: bool = True,
    use_cache: bool = True,
    return_type: Literal["Decimal", "float", "int"] = "int"
) -> decimal.Decimal | Iterable[decimal.Decimal] | float | Iterable[float] | int | Iterable[int]:
    """
    对给定的值进行智能缩放。

    :param value: 要缩放的值
    :type value: int | decimal.Decimal | Iterable[int | decimal.Decimal]
    :param base_size: 基准尺寸
    :type base_size: tuple[int, int]
    :param screen_size: 屏幕尺寸
    :type screen_size: tuple[int, int]
    :param strict_mode: 是否启用严格模式
    :type strict_mode: bool
    :param use_cache: 是否使用缓存
    :type use_cache: bool
    :param return_type: 返回类型
    :type return_type: Literal["Decimal", "float", "int"]
    :return: 缩放后的值
    :rtype: decimal.Decimal | Iterable[decimal.Decimal] | float | Iterable[float] | int | Iterable[int]
    """

    scale_value = getSmartScaleValue(base_size, screen_size, strict_mode = strict_mode, use_cache = use_cache)
    if isinstance(value, Iterable) and not isinstance(value, (str, bytes)):
        return type(value)([smartScale(v, base_size, screen_size, strict_mode = strict_mode, use_cache = use_cache, return_type = return_type) for v in value])
    elif isinstance(value, (int, decimal.Decimal)):
        result = decimal.Decimal(value) * scale_value
        if return_type == "Decimal":
            return result
        elif return_type == "float":
            return float(result)
        elif return_type == "int":
            return int(result)
    else:
        raise TypeError(f"不支持的类型：{type(value).__name__}，仅支持 int、decimal.Decimal 或 Iterable[int | decimal.Decimal]。")

ss = smartScale
