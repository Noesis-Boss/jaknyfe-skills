import pandas as pd


class ReversalZoneConfirmationStrategy:
    def __init__(self, config, risk, journal):
        cfg = config.get("reversal_zone_confirmation", {})
        self.config, self.risk, self.journal = config, risk, journal
        self.timezone = config.get("timezone", "America/New_York")
        self.session_start = pd.Timestamp(cfg.get("session_start", "09:35")).time()
        self.session_end = pd.Timestamp(cfg.get("session_end", "11:00")).time()
        self.level_lookback = int(cfg.get("level_lookback", 20))
        self.move_lookback = int(cfg.get("move_lookback", 3))
        self.min_move_pct = float(cfg.get("min_move_pct", .004))
        self.move_bars = int(cfg.get("move_bars", self.move_lookback))
        self.max_move_bars = int(cfg.get("max_move_bars", self.move_lookback))
        self.structure_lookback = int(cfg.get("structure_lookback", 3))
        self.confirmation_body_ratio = float(cfg.get("confirmation_body_ratio", .5))
        self.volume_multiplier = float(cfg.get("volume_multiplier", 1))
        self.rr_ratio = float(cfg.get("rr_ratio", 2))
        self.max_holding_bars = int(cfg.get("max_holding_bars", 30))
        self.max_gap_pct = float(cfg.get("max_gap_pct", .08))
        self.max_bar_range_pct = float(cfg.get("max_bar_range_pct", .08))
        self.news_blackout_dates = {str(value) for value in cfg.get("news_blackout_dates", [])}
        self.news_blackout_context = bool(cfg.get("news_blackout_context", True))
        self.scale_out_enabled = bool(cfg.get("scale_out_enabled", True))
        self.scale_out_r = float(cfg.get("scale_out_r", 1.5))
        self.scale_out_fraction = float(cfg.get("scale_out_fraction", .5))
        self._active_trades, self._entry_counts = {}, {}

    def _ny(self, ts):
        ts = pd.Timestamp(ts)
        return (ts.tz_localize("UTC") if ts.tzinfo is None else ts).tz_convert(self.timezone)

    def _atr(self, bars):
        previous = bars.close.shift(1)
        tr = pd.concat([bars.high - bars.low, (bars.high - previous).abs(), (bars.low - previous).abs()], axis=1).max(axis=1)
        return float(tr.tail(14).mean())

    def generate_signal(self, symbol, bars, context=None):
        minimum = max(self.level_lookback + self.move_lookback + 2, self.structure_lookback + 5, 20)
        if len(bars) < minimum or symbol in self._active_trades:
            return None
        ts = self._ny(bars.index[-1])
        context = context or {}
        if ts.date().isoformat() in self.news_blackout_dates or (self.news_blackout_context and context.get("high_impact_news")):
            return None
        if not self.session_start <= ts.time() < self.session_end or self._entry_counts.get((symbol, ts.date()), 0) >= 1:
            return None
        f = bars.copy().tail(max(self.level_lookback + self.move_lookback + 5, 40))
        if any(c not in f for c in ("open", "high", "low", "close", "volume")):
            return None
        bar, prior = f.iloc[-1], f.iloc[:-1]
        close, high, low, open_price = map(float, (bar.close, bar.high, bar.low, bar.open))
        previous_close = float(prior.close.iloc[-1])
        if close <= 0 or previous_close <= 0 or float(bar.volume) <= 0 or abs(open_price / previous_close - 1) > self.max_gap_pct or (high - low) / close > self.max_bar_range_pct:
            return None
        avg_volume = float(prior.volume.tail(20).mean())
        if avg_volume <= 0 or float(bar.volume) < avg_volume * self.volume_multiplier:
            return None
        zone = prior.tail(self.level_lookback)
        support, resistance = float(zone.low.min()), float(zone.high.max())
        move = prior.tail(self.move_bars)
        if len(move) > self.max_move_bars:
            return None
        move_start, move_end = float(move.close.iloc[0]), float(move.close.iloc[-1])
        body_ratio = abs(close - open_price) / max(high - low, 1e-9)
        if body_ratio < self.confirmation_body_ratio or self._atr(f) <= 0:
            return None
        recent = prior.tail(self.structure_lookback).close.astype(float)
        higher_low = float(recent.iloc[-1]) > float(recent.iloc[:-1].min())
        lower_high = float(recent.iloc[-1]) < float(recent.iloc[:-1].max())
        atr = self._atr(f)
        if (move_start - move_end) / move_start >= self.min_move_pct and low <= support * 1.002 and close > open_price and higher_low:
            stop, target = min(low, close - atr), close + self.rr_ratio * (close - min(low, close - atr))
            qty = self.risk.calculate_qty(close, stop)
            if qty > 0: return self._signal(symbol, "long", close, stop, target, qty, ts, "15m support / 1m bullish reversal proxy")
        if (move_end - move_start) / move_start >= self.min_move_pct and high >= resistance * .998 and close < open_price and lower_high:
            stop, target = max(high, close + atr), close - self.rr_ratio * (max(high, close + atr) - close)
            qty = self.risk.calculate_qty(close, stop, allow_fractional=False)
            if qty > 0: return self._signal(symbol, "short", close, stop, target, qty, ts, "15m resistance / 1m bearish reversal proxy")
        return None

    def _signal(self, symbol, direction, entry, stop, target, qty, ts, reason):
        return {"symbol": symbol, "direction": direction, "entry": round(entry, 2), "stop": round(stop, 2), "target": round(target, 2), "qty": qty, "timestamp": ts.isoformat(), "reason": reason}

    def on_trade_entered(self, symbol, signal):
        self._active_trades[symbol] = dict(signal, entry_bar_count=0, initial_qty=signal["qty"], realized_pnl=0.0, scaled_out=False)
        key = (symbol, pd.Timestamp(signal["timestamp"]).date())
        self._entry_counts[key] = self._entry_counts.get(key, 0) + 1

    def check_exit(self, symbol, bars, broker):
        trade = self._active_trades.get(symbol)
        if not trade: return None
        trade["entry_bar_count"] += 1
        bar, ts = bars.iloc[-1], self._ny(bars.index[-1])
        high, low, close = map(float, (bar.high, bar.low, bar.close)); long = trade["direction"] == "long"
        risk_per_share = abs(trade["entry"] - trade["stop"])
        favorable = (high - trade["entry"]) if long else (trade["entry"] - low)
        if self.scale_out_enabled and not trade["scaled_out"] and risk_per_share > 0 and favorable >= self.scale_out_r * risk_per_share and trade["qty"] > 1:
            reduce_qty = max(1, int(trade["qty"] * self.scale_out_fraction))
            reduce_qty = min(reduce_qty, trade["qty"] - 1)
            exit_price = trade["entry"] + self.scale_out_r * risk_per_share if long else trade["entry"] - self.scale_out_r * risk_per_share
            partial_pnl = (exit_price - trade["entry"]) * reduce_qty if long else (trade["entry"] - exit_price) * reduce_qty
            trade["qty"] -= reduce_qty
            trade["realized_pnl"] += partial_pnl
            trade["scaled_out"] = True
            self.risk.update_cash(partial_pnl)
            return {"symbol": symbol, "direction": trade["direction"], "entry": trade["entry"], "exit_price": round(exit_price, 2), "qty": reduce_qty, "pnl": round(partial_pnl, 2), "rr": self.scale_out_r, "reason": "scale_out", "exit_time": ts.isoformat()}
        if long: exit_price, reason = ((trade["stop"], "stop_loss") if low <= trade["stop"] else (trade["target"], "target_hit") if high >= trade["target"] else (None, None))
        else: exit_price, reason = ((trade["stop"], "stop_loss") if high >= trade["stop"] else (trade["target"], "target_hit") if low <= trade["target"] else (None, None))
        if exit_price is None and (trade["entry_bar_count"] >= self.max_holding_bars or ts.time() >= self.session_end): exit_price, reason = close, "session_close" if ts.time() >= self.session_end else "max_holding_bars"
        if exit_price is None: return None
        pnl = (exit_price - trade["entry"]) * trade["qty"] if long else (trade["entry"] - exit_price) * trade["qty"]
        pnl += trade["realized_pnl"]
        result = {"symbol": symbol, "direction": trade["direction"], "entry": trade["entry"], "exit_price": round(exit_price, 2), "qty": trade["qty"], "pnl": round(pnl, 2), "rr": self.rr_ratio, "reason": reason, "exit_time": ts.isoformat()}
        self.risk.update_cash(pnl - trade["realized_pnl"])
        if self.journal: self.journal.log_trade(result)
        del self._active_trades[symbol]
        return result
