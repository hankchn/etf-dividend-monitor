#!/usr/bin/env python3
"""
红利ETF批量定投机会监测
监控标的:
  - 159307 100红利ETF
  - 563020 红利低波ETF
  - 515450 50红利ETF
  - 515180 中证红利ETF

- 获取当前价格和250日历史数据
- 计算MA250及偏离度
- 价格低于MA250时提醒定投
"""

import json
import sys
import urllib.request
import datetime
import time

# 监控的ETF列表: (市场前缀, 代码, 名称)
ETF_LIST = [
    ("sz", "159307", "100红利ETF"),
    ("sh", "563020", "红利低波ETF"),
    ("sh", "515450", "50红利ETF"),
    ("sh", "515180", "中证红利ETF"),
]


def fetch_current_price(market, code):
    """通过腾讯财经接口获取ETF当前价格"""
    symbol = f"{market}{code}"
    url = f"https://qt.gtimg.cn/q={symbol}"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=10) as resp:
        raw = resp.read().decode("gbk")
    # 格式: v_sh515180="1~中证红利ETF~515180~1.234~..."
    data = raw.split("~")
    if len(data) < 5:
        raise ValueError(f"数据解析失败: {raw[:200]}")
    name = data[1]
    current_price = float(data[3])
    prev_close = float(data[4])
    change_pct = round((current_price - prev_close) / prev_close * 100, 2) if prev_close else 0
    return {
        "name": name,
        "code": code,
        "market": market,
        "price": current_price,
        "prev_close": prev_close,
        "change_pct": change_pct
    }


def fetch_history_klines(market, code, days=300):
    """通过腾讯财经接口获取日K线数据（用于计算MA250）"""
    symbol = f"{market}{code}"
    url = f"https://web.ifzq.gtimg.cn/appstock/app/fqkline/get?param={symbol},day,,,{days},qfq"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=15) as resp:
        raw = resp.read().decode("utf-8")
    result = json.loads(raw)

    # 解析K线数据
    klines = result.get("data", {}).get(symbol, {})
    day_data = klines.get("day", []) or klines.get("qfqday", [])

    if not day_data:
        raise ValueError(f"未获取到K线数据，返回: {json.dumps(result, ensure_ascii=False)[:300]}")

    # 每条格式: [日期, 开盘, 收盘, 最高, 最低, 成交量]
    close_prices = []
    for item in day_data:
        close_prices.append(float(item[2]))  # 收盘价

    return close_prices, len(day_data)


def calculate_ma(prices, period=250):
    """计算移动平均线"""
    if len(prices) < period:
        return None, len(prices)
    ma = sum(prices[-period:]) / period
    return round(ma, 4), period


def check_single_etf(market, code, display_name):
    """检查单只ETF的定投信号"""
    symbol = f"{market}{code}"

    print(f"\n{'─'*50}")
    print(f"📊 {display_name}（{code}）")
    print(f"{'─'*50}")

    # 1. 获取当前价格
    try:
        info = fetch_current_price(market, code)
        print(f"\n  📈 当前信息:")
        print(f"     名称: {info['name']}")
        print(f"     代码: {symbol}")
        print(f"     当前价: {info['price']} 元")
        print(f"     昨收价: {info['prev_close']} 元")
        print(f"     涨跌幅: {info['change_pct']}%")
    except Exception as e:
        print(f"  ❌ 获取当前价格失败: {e}")
        return None

    # 2. 获取历史数据并计算MA250
    try:
        close_prices, total_days = fetch_history_klines(market, code, 350)
        print(f"\n  📉 历史数据:")
        print(f"     获取到 {total_days} 个交易日数据")

        ma250, actual_period = calculate_ma(close_prices, 250)

        if ma250 is None:
            print(f"     ⚠️ 数据不足250个交易日（仅{actual_period}日），无法计算MA250")
            # 使用已有数据计算参考均线
            if len(close_prices) >= 60:
                ma_ref, ref_period = calculate_ma(close_prices, min(len(close_prices), 200))
                if ma_ref:
                    print(f"     📊 参考: MA{ref_period} = {ma_ref} 元")
            return None

        print(f"     MA250 = {ma250} 元")

    except Exception as e:
        print(f"  ❌ 获取历史数据失败: {e}")
        return None

    # 3. 计算偏离度
    current_price = info['price']
    deviation = round((current_price - ma250) / ma250 * 100, 2)

    print(f"\n  📐 偏离度分析:")
    print(f"     当前价 / MA250 = {current_price} / {ma250}")
    print(f"     偏离度 = {deviation}%")

    # 4. 判断并给出建议
    if deviation < 0:
        if deviation <= -10:
            severity = "🔴 严重低估"
            suggestion = "强烈建议加倍定投"
        elif deviation <= -5:
            severity = "🟠 明显低估"
            suggestion = "建议增加定投金额"
        elif deviation <= -2:
            severity = "🟡 轻度低估"
            suggestion = "建议正常定投"
        else:
            severity = "🟢 略低于均线"
            suggestion = "可考虑定投"

        print(f"\n  💰 定投信号: {severity}")
        print(f"     当前价 {current_price} 元 低于 MA250 {ma250} 元")
        print(f"     偏离度: {deviation}%")
        print(f"     建议: {suggestion}")
        signal = f"BUY | {info['name']} | price={current_price} | ma250={ma250} | deviation={deviation}% | {suggestion}"
    else:
        print(f"\n  😴 无定投信号")
        print(f"     当前价 {current_price} 元 高于 MA250 {ma250} 元")
        print(f"     偏离度: +{deviation}%")
        print(f"     建议: 持有观望，等待回调至均线下方")
        signal = f"HOLD | {info['name']} | price={current_price} | ma250={ma250} | deviation=+{deviation}%"

    return {
        "name": info['name'],
        "code": code,
        "market": market,
        "price": current_price,
        "ma250": ma250,
        "deviation": deviation,
        "signal": signal
    }


def main():
    today = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

    print(f"{'='*60}")
    print(f"📊 红利ETF批量定投监测")
    print(f"⏰ 检查时间: {today}")
    print(f"📋 监控标的: {len(ETF_LIST)} 只")
    for mkt, code, name in ETF_LIST:
        print(f"   • {name}（{code}）")
    print(f"{'='*60}")

    results = []
    for i, (market, code, display_name) in enumerate(ETF_LIST):
        result = check_single_etf(market, code, display_name)
        if result:
            results.append(result)
        # 请求间隔，避免被限流
        if i < len(ETF_LIST) - 1:
            time.sleep(0.5)

    # 汇总报告
    print(f"\n\n{'='*60}")
    print(f"📋 汇总报告")
    print(f"{'='*60}")

    if not results:
        print("⚠️ 未获取到有效数据")
        return

    # 按偏离度排序（越低越优先）
    results.sort(key=lambda x: x['deviation'])

    print(f"\n  {'ETF名称':<16} {'代码':<10} {'当前价':>8} {'MA250':>8} {'偏离度':>8}  {'信号'}")
    print(f"  {'─'*80}")

    buy_signals = []
    for r in results:
        dev_str = f"{r['deviation']}%" if r['deviation'] < 0 else f"+{r['deviation']}%"
        if r['deviation'] < 0:
            signal_icon = "💰 定投"
            buy_signals.append(r)
        else:
            signal_icon = "😴 观望"
        print(f"  {r['name']:<14} {r['market']}{r['code']:<8} {r['price']:>8.3f} {r['ma250']:>8.4f} {dev_str:>8}  {signal_icon}")

    print(f"  {'─'*80}")

    # 定投建议汇总
    if buy_signals:
        print(f"\n  🎯 有 {len(buy_signals)} 只ETF出现定投信号:")
        for r in buy_signals:
            if r['deviation'] <= -10:
                level = "🔴 严重低估 → 强烈建议加倍定投"
            elif r['deviation'] <= -5:
                level = "🟠 明显低估 → 建议增加定投金额"
            elif r['deviation'] <= -2:
                level = "🟡 轻度低估 → 建议正常定投"
            else:
                level = "🟢 略低于均线 → 可考虑定投"
            print(f"     • {r['name']}（{r['code']}）偏离 {r['deviation']}% — {level}")
    else:
        print(f"\n  😴 全部高于MA250，暂无定投信号，建议持有观望")

    print(f"\n{'='*60}")

    # 输出结构化结果（方便后续自动化解析）
    for r in results:
        print(f"[SIGNAL] {r['signal']}")


if __name__ == "__main__":
    main()
